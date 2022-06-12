# pylint: disable=arguments-renamed
# pylint: disable=too-few-public-methods

"""Forward declaration of some models"""

from chiakilisp.models.token import Token


class CommonType:

    """Forward declaration for both models"""

    def execute(self, env: dict, top: bool):

        """Just to define 'execute()' signature"""


class LiteralType(CommonType):

    """Forward declaration for Literal model"""

    def token(self) -> Token:

        """Just to define 'token()' signature"""


class ExpressionType(CommonType):

    """Forward declaration for Expression model"""

    def children(self) -> list:

        """Just to define 'children()' signature"""
