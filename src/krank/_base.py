import functools


class RepositoryManager:
    _repo = None

    @classmethod
    def init_repository(cls, repository_id):
        from krank import repositories
        # class_name = [x for x in dir(repositories) if x.lower() == repository_id][0]
        cls._repo = getattr(repositories, repository_id)()

    @classmethod
    def get_repository(cls):
        return cls._repo


def repo(repository_id):
    def inner_wrapper(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            RepositoryManager.init_repository(repository_id)
            return func(*args, **kwargs)
        return wrapped
    return inner_wrapper
