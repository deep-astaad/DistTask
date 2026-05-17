TASK_REGISTRY = {}


def task(name: str):
    def decorator(func):
        TASK_REGISTRY[name] = func
        return func

    return decorator
