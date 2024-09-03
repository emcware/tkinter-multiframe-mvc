from typing import Callable

"""
In Python, the Callable type from the typing module is used to indicate that a value 
should be a callable object, such as a function or an object with a __call__ method.
It is a way to specify in type hints that a parameter or return value is expected to be callable.
"""


# usage -
def foo(callback: Callable):
    """
    In this example, foo expects a callback parameter that is a callable.
    """
    callback()


# specifying Arguments and Return type
def bar(func: Callable[[int, str], bool]):
    """
    Here, bar expects a function (func) that takes two arguments, an int and a str,
    and returns a bool.
    """
    result = func(42, 'hello')
    print(result)


# Examples

#########################################################################################
#
#       Example 1.  Function as a Parameter:
#
#########################################################################################

def process_data(data: list[int], processor: Callable[[int], int]) -> list[int]:
    """
    processor: Callable[[int], int]:
    This indicates that processor is a callable that takes an int and returns an int.

    Using Callable in type hints helps with code readability and static type checking,
    ensuring that functions are used correctly according to their intended signatures.
    """
    return [processor(item) for item in data]


def increment(x: int) -> int:
    return x + 1

#########################################################################################
#
#       Example 2.  Callable Object (Class with __call__):
#
#########################################################################################


class Multiplier:
    def __init__(self, factor: int):
        self.factor = factor

    def __call__(self, value: int) -> int:
        return value * self.factor


def process_data_w_class(data: list[int], processor: Callable[[int], int]) -> list[int]:
    """
    Callable[[int, str], bool]: This specifies a callable that takes two arguments,
    an int and a str, and returns a bool.
    """
    return [processor(item) for item in data]



if __name__ == "__main__":
    my_data = [1, 2, 3]
    processed = process_data(my_data, increment)
    print(processed)  # Output: [2, 3, 4]

    multiplier = Multiplier(3)
    # my_data = [1, 2, 3]
    processed = process_data_w_class(my_data, multiplier)
    print(processed)  # Output: [3, 6, 9]
