from ._repo import _get_repo


def checkout(path: str, refspec: str):
    _get_repo(path).git.checkout(refspec)


def fetch(path: str, remote: str, refspec: str = None):
    _get_repo(path).remote(remote).fetch(refspec)


def pull(path: str, remote: str, refspec: str = None):
    _get_repo(path).remote(remote).pull(refspec)
