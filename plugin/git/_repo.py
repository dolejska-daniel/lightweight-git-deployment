from git import Repo

_repo_cache = {}


def _get_repo(path: str) -> Repo:
    if path not in _repo_cache:
        _repo_cache[path] = Repo(path)

    return _repo_cache[path]
