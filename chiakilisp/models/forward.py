# pylint: disable=arguments-renamed
# pylint: disable=too-few-public-methods

"""Forward declaration of some models"""

from chiakilisp.models.token import Token


class CommonType:

    """Forward declaration for both models"""

    _properties: dict

    def dump(self, indent: int) -> None:

        """Just to define 'dump()' method signature"""

    def execute(self, env: dict, top: bool):

        """Just to define 'execute()' method signature"""


class LiteralType(CommonType):

    """Forward declaration for Literal model"""

    def token(self) -> Token:

        """Just to define 'token()' method signature"""


class ExpressionType(CommonType):

    """Forward declaration for Expression model"""

    def children(self) -> list:

        """Just to define 'children()' method signature"""
