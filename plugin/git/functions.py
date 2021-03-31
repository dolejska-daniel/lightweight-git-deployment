from ._repo import _get_repo


def describe(path: str, tags: bool = True, always: bool = True) -> str:
    return _get_repo(path).git.describe(tags=tags, always=always)
