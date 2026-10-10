from datetime import datetime, timezone
from uuid import uuid4

from app.db.collections import (
    analysis_reports_collection,
    file_hotspots_collection,
    file_ownership_collection,
    temporal_coupling_collection,
)


def create_analysis_report(
    project_id: str,
    total_commits: int,
    total_contributors: int,
):
    report = {
        "id": str(uuid4()),
        "project_id": project_id,
        "total_commits": total_commits,
        "total_contributors": total_contributors,
        "overall_health_score": None,
        "analyzed_at": datetime.now(timezone.utc).isoformat(),
    }

    analysis_reports_collection.insert_one(report)

    return report


def create_hotspot(report_id: str, file_path: str, change_frequency: int):
    file_hotspots_collection.insert_one({
        "id": str(uuid4()),
        "report_id": report_id,
        "file_path": file_path,
        "change_frequency": change_frequency,
    })


def create_ownership(
    report_id: str,
    file_path: str,
    owner_name: str,
    ownership_percentage: float,
    is_bus_factor_risk: bool,
):
    file_ownership_collection.insert_one({
        "id": str(uuid4()),
        "report_id": report_id,
        "file_path": file_path,
        "owner_name": owner_name,
        "ownership_percentage": ownership_percentage,
        "is_bus_factor_risk": is_bus_factor_risk,
    })


def create_coupling(
    report_id: str,
    file_a: str,
    file_b: str,
    co_change_count: int,
):
    temporal_coupling_collection.insert_one({
        "id": str(uuid4()),
        "report_id": report_id,
        "file_a": file_a,
        "file_b": file_b,
        "co_change_count": co_change_count,
    })