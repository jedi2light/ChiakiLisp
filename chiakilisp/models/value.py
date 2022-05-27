# pylint: disable=line-too-long
# pylint: disable=missing-module-docstring

from typing import Any
from chiakilisp.utils import ASSERT  # our lovely custom assert funct
from chiakilisp.models.token import Token  # Value needs Token    :*)


class NotFound:  # pylint: disable=too-few-public-methods  # shut up!

    """
    Stub class to display that there is no such a name in environment
    """


class Value:

    """
    Value is the class that encapsulates single Token, and meant to be a part of Expression (but not always)
    """

    _token: Token

    def __init__(self, token: Token) -> None:

        """Initialize Value instance"""

        self._token = token

    def token(self) -> Token:

        """Returns related token"""

        return self._token

    def lint(self, _: dict, rule: str, storage: dict) -> None:

        """React to the builtin linter visit"""

        if rule == 'UnusedGlobalVariables' and self.token().type() == Token.Identifier:
            name = self.token().value()
            if name in storage:
                storage[name] += 1  # <- if there is such a global variable, increment its referencing count

    def generate(self, _e: dict, name: str, inline: bool):  # pylint: disable=inconsistent-return-statements

        """Generate C++ representation of value"""

        token = self.token()  # to refer it for multimple times

        if token.type() == Token.Nil:
            return 'NULL' if inline else f'void* {name} = NULL;'
        if token.type() == Token.Number:
            return token.value() if inline else f'unsigned int {name} = {token.value()};'
        if token.type() == Token.String:
            return f'"{token.value()}"' if inline else f'std::string {name} = "{token.value()}";'
        if token.type() == Token.Boolean:
            return token.value() if inline else f'bool {name} = {token.value()};'

    def execute(self, environment: dict, __=False) -> Any:  # pylint: disable=inconsistent-return-statements

        """Execute, here, is the return Python value related to the value: string, number, and vice versa"""

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

            if '/' in name:
                obj_name, member_name = name.split('/')  # <---------- syntax is <object name>/<member name>
                obj_object = environment.get(obj_name, NotFound)  # <------- assign found object or NotFound
                ASSERT(obj_object is not NotFound, NameError, f"NameError: '{obj_name}' has not been found")
                member_object = getattr(obj_object, member_name, NotFound)  # <-------- assign member object
                ASSERT(member_object is not NotFound, NameError, f"NameError: no'{obj_name}/{member_name}'")
                return member_object  # <------------------ thus we return found module/object member object

            found = environment.get(name, NotFound)

            # TODO: maybe implement simple fuzzy-matching algorithm to suggest known variable names in scope
            ASSERT(found is not NotFound, NameError, f'NameError: there is no \'{name}\' in current scope.')

            return found  # <- return found Python 3 value (from the current environment) or raise NameError
