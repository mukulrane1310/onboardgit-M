from collections import Counter


def get_file_ownership(commits: list) -> dict:
    """
    For each file, tracks which authors changed it and how many times.

    Args:
        commits: A list of commit objects

    Returns:
        A dict mapping file_path -> Counter of {author_name: change_count}
        Example: {"main.py": Counter({"Alice": 5, "Bob": 2})}
    """
    file_ownership = {}

    for commit in commits:
        author_name = commit.author.name
        for file_path in commit.stats.files:
            if file_path not in file_ownership:
                file_ownership[file_path] = Counter()
            file_ownership[file_path][author_name] += 1

    return file_ownership


def get_owner_info(file_path: str, file_ownership: dict) -> dict:
    """
    Given a single file, finds its main owner and ownership percentage.

    Args:
        file_path: The file to check
        file_ownership: The dict returned by get_file_ownership()

    Returns:
        A dict with owner name, ownership percentage, and all contributors
    """
    owner_counts = file_ownership[file_path]
    owner_name, owner_commits = owner_counts.most_common(1)[0]
    total_changes = sum(owner_counts.values())
    ownership_percent = round((owner_commits / total_changes) * 100, 1)

    return {
        "file_path": file_path,
        "owner_name": owner_name,
        "ownership_percent": ownership_percent,
        "all_contributors": dict(owner_counts),
    }


def get_bus_factor_risks(
    top_hotspots: list, file_ownership: dict, threshold: float = 70.0
) -> list:
    """
    Flags files where one person owns a very high percentage of changes.
    This is risky because if that person leaves, no one else knows the file well.

    Args:
        top_hotspots: List of (file_path, change_count) tuples
        file_ownership: The dict returned by get_file_ownership()
        threshold: Ownership percentage above which a file is flagged (default 70%)

    Returns:
        A list of owner_info dicts (from get_owner_info) that exceed the threshold
    """
    risky_files = []

    for file_path, _ in top_hotspots:
        owner_info = get_owner_info(file_path, file_ownership)
        if owner_info["ownership_percent"] >= threshold:
            risky_files.append(owner_info)

    return risky_files