# pylint: disable=fixme
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=arguments-renamed
# pylint: disable=missing-module-docstring
# pylint: disable=too-many-return-statements
# pylint: disable=unnecessary-lambda-assignment

from functools import partial
from typing import Any, Callable
from chiakilisp.utils import get_assertion_closure  # <- for ASSERT()
from chiakilisp.models.token import Token  # Literal needs Token  :*)
from chiakilisp.models.forward import LiteralType  # forward declared

_ASSERT: Callable = get_assertion_closure(NameError)  # for NameError


class NotFound:  # pylint: disable=too-few-public-methods  # its okay

    """
    Stub class to display that there is no such a name in environment
    """


class Literal(LiteralType):

    """
    Literal is the class that encapsulates single Token and meant to be a part of Expression, but not always
    """

    _token: Token

    def __init__(self, token: Token) -> None:

        """Initialize Literal instance"""

        self._token = token

    def token(self) -> Token:

        """Returns Token instance"""

        return self._token

    def dump(self, indent: int) -> None:

        """Dumps a single (expression) literal"""

        token_value = self.token().value()  # <- store literal token value to refer it later

        print(' ' * indent, (f'"{token_value}"' if self.token().is_string() else token_value))

    def execute(self, environment: dict, __=False) -> Any:  # pylint: disable=inconsistent-return-statements

        """Execute, here, is to return Python value tied to the literal: number, string, boolean, etc ..."""

        if self.token().type() == Token.Nil:

            return None

        if self.token().type() == Token.Number:

            return float(self.token().value()) if '.' in self.token().value() else int(self.token().value())

        if self.token().type() == Token.String:

            return self.token().value()

        if self.token().type() == Token.Boolean:

            return self.token().value() == 'true'

        if self.token().type() == Token.Identifier:

            name = self.token().value()  # <------------- because we reference token().value() so many times
            where = self.token().position()  # <------------------------------------ remember token position

            ASSERT = partial(_ASSERT, where)  # <-------------- create partial function to simplify ASSERT()

            if not name.startswith('/') and not name.endswith('/') and '/' in name:  # <--------- be careful
                obj_name, member_name, *_ = name.split('/')  # <-------- syntax: <object name>/<member name>
                obj_object = environment.get(obj_name, NotFound)  # <-- assign as a found object or NotFound
                ASSERT(obj_object is not NotFound,                 f"no '{obj_name}' symbol in this scope.")
                member_object = getattr(obj_object, member_name, NotFound)  # <--- assign as a member object
                ASSERT(member_object is not NotFound,
                       f"object (or module) named '{obj_name}' has no such a member named '{member_name}'.")
                return member_object  # <------------------ thus we return found module/object member object

            found = environment.get(name, NotFound)  # <--- handle case when identifier name isn't qualified

            ASSERT(found is not NotFound,                              f"no '{name}' symbol in this scope.")

            return found  # <- return found Python 3 value (from the current environment) or raise NameError


Nil = Literal(Token(Token.Nil, 'nil', ()))  # predefined Nil Literal; useful for empty defn, fn and let body
