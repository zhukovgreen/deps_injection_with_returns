import attr
import pytest
from returns.context import RequiresContext

from config import App, Config, Dataset, c
from some_module import super_sum


def test_config():
    """Check various aspects of the config.

    - it was loaded from yaml
    - it is frozen
    """
    assert c.app.string == "this is a string"
    assert c.app.integer == 99
    with pytest.raises(attr.exceptions.FrozenInstanceError):
        c.app.string = "another string"  # type: ignore[misc]
    assert c.app.string == "this is a string"


def test_returns_way_of_deps_injection():
    """Check how returns libs helps in handling deps injection.

    To see that the function explicitly depends on a context (so the context affects the
        function execution).
    This approach is clean, and keep the logic implementation pure
        and testing a way more accurate!
    """
    # Since config is a context I'd like to create two different configs to see
    #   how context affects the function execution
    config1 = Config(
        App(string="", integer=0),
        Dataset(string="", integer=1),
        secret_number=1,
    )
    config2 = Config(
        App(string="", integer=0),
        Dataset(string="", integer=1),
        secret_number=2,
    )

    some_result = super_sum(1, 2, 3)
    assert isinstance(some_result, RequiresContext)

    # fmt: off

    # let's do some operations with our function
    new_result = some_result\
        .map(lambda res: res + 1)\
        .map(lambda res: res + 2)\
        .map(str)

    # fmt: on

    # now see how context affects our function and
    #   how easy to test a function with different context

    #   origin config (secret number = 0)
    assert new_result(c) == "9"

    #   secret number = 1
    assert new_result(config1) == "10"

    #   secret number = 2
    assert new_result(config2) == "11"
