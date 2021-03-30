from git import Repo

_repo_cache = {}


def _get_repo(path: str) -> Repo:
    if path not in _repo_cache:
        _repo_cache[path] = Repo(path)

    return _repo_cache[path]


def checkout(path: str, refspec: str):
    _get_repo(path).git.checkout(refspec)


def fetch(path: str, remote: str, refspec: str = None):
    _get_repo(path).remote(remote).fetch(refspec)


def pull(path: str, remote: str, refspec: str = None):
    _get_repo(path).remote(remote).pull(refspec)
