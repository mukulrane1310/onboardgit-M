import git
import shutil
import os
import stat


def remove_readonly(func, path, excinfo):
    """
    Windows sometimes marks .git files as read-only, which blocks deletion.
    This function removes that restriction before deleting.
    """
    os.chmod(path, stat.S_IWRITE)
    func(path)


def clone_repository(repo_url: str, clone_path: str = "temp_repo") -> git.Repo:
    """
    Clones a git repository to a local temp folder.
    If a folder from a previous run already exists, it deletes it first.

    Args:
        repo_url: The GitHub URL of the repo to analyze
        clone_path: Local folder name to clone into

    Returns:
        A GitPython Repo object, ready to be analyzed
    """
    if os.path.exists(clone_path):
        shutil.rmtree(clone_path, onerror=remove_readonly)

    repo = git.Repo.clone_from(repo_url, clone_path)
    return repo


def get_all_commits(repo: git.Repo) -> list:
    """
    Returns a list of all commits in the repo, newest first.

    Args:
        repo: A GitPython Repo object

    Returns:
        A list of commit objects
    """
    return list(repo.iter_commits())

def cleanup_repository(repo: git.Repo = None, clone_path: str = "temp_repo"):
    """
    Closes the repo connection (important on Windows) and deletes
    the cloned repo folder after analysis is done.

    Args:
        repo: The GitPython Repo object to close (optional but recommended)
        clone_path: Local folder to delete
    """
    if repo is not None:
        repo.close()  # Release Windows file locks before deleting

    if os.path.exists(clone_path):
        shutil.rmtree(clone_path, onerror=remove_readonly)