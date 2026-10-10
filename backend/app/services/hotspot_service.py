from collections import Counter
import git


def get_file_change_counts(commits: list) -> Counter:
    """
    Counts how many times each file was changed across all commits.

    Args:
        commits: A list of commit objects (from git_service.get_all_commits)

    Returns:
        A Counter mapping file_path -> number of times changed
    """
    file_change_counter = Counter()

    for commit in commits:
        for file_path in commit.stats.files:
            file_change_counter[file_path] += 1

    return file_change_counter


def get_top_hotspots(commits: list, top_n: int = 10) -> list:
    """
    Finds the most frequently changed files (the "hotspots").

    Args:
        commits: A list of commit objects
        top_n: How many top files to return (default 10)

    Returns:
        A list of tuples: [(file_path, change_count), ...]
        sorted from most changed to least changed
    """
    file_change_counter = get_file_change_counts(commits)
    return file_change_counter.most_common(top_n)