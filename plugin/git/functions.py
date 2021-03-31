from ._repo import _get_repo


def describe(path: str) -> str:
    return _get_repo(path).git.describe(always=True)
