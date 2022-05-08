from typing import Any
from chiakilisp.models.token import Token


class NotFound:

    """
    Stub class to display that there is no such a name in environment
    """


class Operand:

    """
    Operand is the class that encapsulates single Token and meant to be a prt of Expression (but not always)
    """

    _token: Token

    def __init__(self, token: Token) -> None:

        """Initialize Operand instance"""

        self._token = token

    def token(self) -> Token:

        """Returns related token"""

        return self._token

    def execute(self, environment: dict, top: bool = True) -> Any:

        """Execute here, is the return Python value related to the operand: string, number and vice versa"""

        if self.token().type() == Token.Nil:

            return None

        if self.token().type() == Token.Number:

            return int(self.token().value())

        if self.token().type() == Token.String:

            return self.token().value()

        if self.token().type() == Token.Boolean:

            return self.token().value() == 'true'

        if self.token().type() == Token.Identifier:

            name = self.token().value()
            found = environment.get(name, NotFound)

            assert found is not NotFound, f'Operand::execute(): no {name} in the current environment, typo?'

            return found  # return found Python 3 value (from the current environment), if not found, raise!
