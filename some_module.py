from returns.context import RequiresContext

from config import Config


# See how the dependency on the context explicitly declared
def super_sum(*args: int) -> RequiresContext[int, Config]:
    """Sums all args + adds a secret number from the config.

    RequiresContext here is even not needed the real value of the config,
    it just declares that the function depends on the the Config context.
    """

    def factory(c: Config) -> int:
        return sum(args) + c.secret_number

    return RequiresContext(factory)
