from itertools import accumulate
import time
import logging
import icecream as ic

from matplotlib import pyplot as plt
from functools import wraps, partial

plt.set_loglevel("error")


def execution_time(
    _func=None,
    *,
    logging_level=logging.DEBUG,
):

    if _func is None:
        return partial(execution_time, logging_level=logging_level)

    logname = _func.__module__
    log = logging.getLogger(logname)
    logmsg = _func.__name__

    def decorator(func):
        @wraps(func)
        def wrapper_timer(*args, **kwargs):
            log.log(logging_level, logmsg)
            start_time = time.perf_counter()
            value = func(*args, **kwargs)
            end_time = time.perf_counter()
            run_time = end_time - start_time
            ic(f"Finished {func.__name__}() in {run_time:.4f} secs")
            return value

        return wrapper_timer

    return decorator


def counter(_func):

    @wraps(_func)
    def counter_wrapper(*args, **kwargs):
        counter_wrapper.num_calls += 1
        return _func(*args, **kwargs)

    counter_wrapper.num_calls = 0
    return counter_wrapper


def plot_history(history):
    plt.figure(figsize=(14, 8))
    plt.plot(
        range(len(history)),
        list(accumulate(history, min)),
        color="red",
    )
    plt.scatter(range(len(history)), history, marker=".")


def get_console_logger(name: str, level: int):
    logger = logging.getLogger(name)
    logger.setLevel(level=level)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level=level)
    formatter = logging.Formatter("{levelname} - {message}", style="{")
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger
