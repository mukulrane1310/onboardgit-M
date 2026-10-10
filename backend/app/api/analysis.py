from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import git

from app.services.git_service import clone_repository, get_all_commits, cleanup_repository
from app.services.hotspot_service import get_top_hotspots
from app.services.ownership_service import (
    get_file_ownership,
    get_bus_factor_risks,
    get_owner_info,
)
from app.services.coupling_service import get_top_coupled_pairs
from app.services.project_repository import (
    create_project,
    find_project_by_id,
    get_all_projects,
    update_project_status,
    delete_project,
)
from app.services.analysis_repository import (
    create_analysis_report,
    create_hotspot,
    create_ownership,
    create_coupling,
)
from app.core.auth import get_current_user
from app.db.collections import (
    analysis_reports_collection,
    file_hotspots_collection,
    file_ownership_collection,
    temporal_coupling_collection,
)

router = APIRouter()


class AnalyzeRequest(BaseModel):
    repo_url: str


@router.post("/analyze")
def analyze_repository(
    request: AnalyzeRequest,
    current_user=Depends(get_current_user),
):
    if not request.repo_url or not request.repo_url.strip():
        raise HTTPException(
            status_code=400,
            detail="Repo URL cannot be empty",
        )

    if not request.repo_url.startswith("https://github.com/"):
        raise HTTPException(
            status_code=400,
            detail="Please provide a valid GitHub repo URL (must start with https://github.com/)",
        )

    project = create_project(
    repo_url=request.repo_url,
    user_id=current_user["id"],
)

    try:
        repo = clone_repository(request.repo_url)
    except git.exc.GitCommandError:
        update_project_status(project["id"], "failed")
        raise HTTPException(
            status_code=404,
            detail="Could not access this repository. It may not exist, or it may be private.",
        )

    try:
        commits = get_all_commits(repo)

        if len(commits) == 0:
            update_project_status(project["id"], "failed")
            raise HTTPException(
                status_code=400,
                detail="This repository has no commits to analyze",
            )

        top_hotspots = get_top_hotspots(commits)
        file_ownership = get_file_ownership(commits)
        risky_files = get_bus_factor_risks(
            top_hotspots,
            file_ownership,
        )
        top_coupled = get_top_coupled_pairs(commits)
        all_authors = set(
            commit.author.name for commit in commits
        )

        report = create_analysis_report(
            project_id=project["id"],
            total_commits=len(commits),
            total_contributors=len(all_authors),
        )

        for file_path, change_count in top_hotspots:
            create_hotspot(
                report_id=report["id"],
                file_path=file_path,
                change_frequency=change_count,
            )

        for file_path, _ in top_hotspots:
            owner_info = get_owner_info(
                file_path,
                file_ownership,
            )

            create_ownership(
                report_id=report["id"],
                file_path=file_path,
                owner_name=owner_info["owner_name"],
                ownership_percentage=owner_info["ownership_percent"],
                is_bus_factor_risk=(
                    owner_info["ownership_percent"] >= 70.0
                ),
            )

        for (file_a, file_b), co_change_count in top_coupled:
            create_coupling(
                report_id=report["id"],
                file_a=file_a,
                file_b=file_b,
                co_change_count=co_change_count,
            )

        update_project_status(project["id"], "completed")

        return {
            "project_id": project["id"],
            "total_commits": len(commits),
            "hotspots": [
                {
                    "file_path": path,
                    "change_count": count,
                }
                for path, count in top_hotspots
            ],
            "bus_factor_risks": risky_files,
            "coupled_files": [
                {
                    "file_a": pair[0],
                    "file_b": pair[1],
                    "co_change_count": count,
                }
                for pair, count in top_coupled
            ],
        }

    finally:
        cleanup_repository(repo)



@router.get("/projects")
def get_projects(current_user=Depends(get_current_user)):
    projects = get_all_projects()

    return [
        {
            "id": project["id"],
            "repo_url": project["repo_url"],
            "status": project["status"],
            "created_at": project["created_at"],
        }
        for project in projects
        if project.get("user_id") == current_user["id"]
    ]


@router.get("/projects/{project_id}")
def get_project_details(
    project_id: str,
    current_user=Depends(get_current_user),
):
    project = find_project_by_id(project_id)

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    if project.get("user_id") != current_user["id"]:
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this project",
        )

    report = (
        analysis_reports_collection.find_one(
            {"project_id": project_id},
            {"_id": 0},
        )
    )

    if not report:
        raise HTTPException(
            status_code=404,
            detail="No analysis found for this project",
        )

    hotspots = list(
        file_hotspots_collection.find(
            {"report_id": report["id"]},
            {"_id": 0},
        )
    )

    ownerships = list(
        file_ownership_collection.find(
            {"report_id": report["id"]},
            {"_id": 0},
        )
    )

    coupled = list(
        temporal_coupling_collection.find(
            {"report_id": report["id"]},
            {"_id": 0},
        )
    )

    return {
        "project_id": project["id"],
        "repo_url": project["repo_url"],
        "total_commits": report["total_commits"],
        "hotspots": [
            {
                "file_path": h["file_path"],
                "change_count": h["change_frequency"],
            }
            for h in hotspots
        ],
        "bus_factor_risks": [
            {
                "file_path": o["file_path"],
                "owner_name": o["owner_name"],
                "ownership_percent": o["ownership_percentage"],
            }
            for o in ownerships
            if o.get("is_bus_factor_risk")
        ],
        "coupled_files": [
            {
                "file_a": c["file_a"],
                "file_b": c["file_b"],
                "co_change_count": c["co_change_count"],
            }
            for c in coupled
        ],
    }

@router.delete("/projects/{project_id}")
def delete_project_route(
    project_id: str,
    current_user=Depends(get_current_user),
):
    project = find_project_by_id(project_id)

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    if project.get("user_id") != current_user["id"]:
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this project",
        )

    report = analysis_reports_collection.find_one(
        {"project_id": project_id},
        {"_id": 0, "id": 1},
    )

    if report:
        report_id = report["id"]

        file_hotspots_collection.delete_many(
            {"report_id": report_id}
        )
        file_ownership_collection.delete_many(
            {"report_id": report_id}
        )
        temporal_coupling_collection.delete_many(
            {"report_id": report_id}
        )
        analysis_reports_collection.delete_one(
            {"id": report_id}
        )

    delete_project(project_id)

    return {
        "message": "Project deleted successfully"
    }