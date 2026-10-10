from collections import Counter
from itertools import combinations


def get_file_pair_counts(commits: list) -> Counter:
    """
    Counts how often each pair of files changes together in the same commit.
    This reveals "hidden dependencies" between files that aren't obvious
    from imports or direct references.

    Args:
        commits: A list of commit objects

    Returns:
        A Counter mapping (file_a, file_b) -> number of times they changed together
    """
    file_pair_counter = Counter()

    for commit in commits:
        files_in_commit = list(commit.stats.files.keys())

        # Only look at commits that touched more than 1 file
        if len(files_in_commit) > 1:
            for file_a, file_b in combinations(sorted(files_in_commit), 2):
                file_pair_counter[(file_a, file_b)] += 1

    return file_pair_counter


def get_top_coupled_pairs(commits: list, top_n: int = 10) -> list:
    """
    Finds the file pairs that change together most often.

    Args:
        commits: A list of commit objects
        top_n: How many top pairs to return (default 10)

    Returns:
        A list of tuples: [((file_a, file_b), co_change_count), ...]
    """
    file_pair_counter = get_file_pair_counts(commits)
    return file_pair_counter.most_common(top_n)