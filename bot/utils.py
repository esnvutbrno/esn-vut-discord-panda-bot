import contextlib
import random


@contextlib.contextmanager
def local_seed(seed):
    """
    Sets specific seed for random module only for inner code.
    """
    state = random.getstate()
    random.seed(seed)
    try:
        yield
    finally:
        random.setstate(state)
