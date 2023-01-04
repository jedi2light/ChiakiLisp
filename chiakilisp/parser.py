# pylint: disable=line-too-long
# pylint: disable=unnecessary-dunder-call
# pylint: disable=missing-module-docstring

from typing import List
from chiakilisp.models.token import Token
from chiakilisp.models.literal import Literal
from chiakilisp.models.expression import Expression


Child = Literal or Expression  # define the type for a single child
Children = List[Child]  # define a type describing list of children


class Parser:

    """Parser is the class that takes a list of tokens and produces a wood of Expressions/Literals"""

    _wood: Children
    _tokens: List[Token]

    def __init__(self, tokens: List[Token]) -> None:

        """Initialize Parser instance"""

        self._tokens = tokens
        self._wood = []

    def wood(self) -> Children:

        """Its a getter for private _wood field"""

        return self._wood

    def parse(self) -> None:

        """Process a list of tokens in order to populate complete wood"""

        self._wood = read(self._tokens)  # utilizes dedicated read() func


def find_nearest_closing_brace(filtered: list, visited: list) -> tuple:

    """This function takes a token collection list and finds the nearest closing brace position"""

    _all = tuple(filter(lambda p: p not in visited and p[1].type() == Token.ClosingBrace, filtered))
    if not _all:
        raise SyntaxError('Parser::find_nearest_closing_brace() there is no nearest ClosingBrace token')
    return _all[0]


def find_nearest_opening_brace(filtered: list, visited: list) -> tuple:

    """This function takes a token collection list and finds the nearest opening brace position"""

    _all = tuple(filter(lambda p: p not in visited and p[1].type() == Token.OpeningBrace, filtered))
    if not _all:
        raise SyntaxError('Parser::find_nearest_closing_brace() there is no nearest OpeningBrace token')
    return _all[0]


def boundary(lst: List[Token]) -> int:

    """This function takes a token collection listing and finds actual boundary to starting expression"""

    assert len(lst) >= 2 and lst[0].type() == Token.OpeningBrace  # non-empty tokens list, first should match '('.

    filtered: list  # for some reason, pylint confuses about filtered type assuming it is the same type as the lst

    filtered = list(filter(lambda _pr: _pr[1].type() in [Token.OpeningBrace, Token.ClosingBrace], enumerate(lst)))

    starting_opening_brace = filtered[0]
    starting_opening_brace_position = starting_opening_brace[0]

    visited = []  # define list of brace tokens we've already visited

    while True:
        if not filtered:
            return -1  # return '-1' if there are no more brace tokens

        nearest_closing_brace = find_nearest_closing_brace(filtered, visited)
        nearest_closing_brace_position = nearest_closing_brace[0]

        reversed_filtered = list(reversed(filtered[:filtered.index(nearest_closing_brace) + 1]))

        nearest_opening_brace_to_that_closing = find_nearest_opening_brace(reversed_filtered, visited)
        nearest_opening_brace_to_that_closing_position = nearest_opening_brace_to_that_closing[0]

        if nearest_opening_brace_to_that_closing_position == starting_opening_brace_position:
            return nearest_closing_brace_position  # if matches exact same position, its valid expression boundary

        visited.append(nearest_closing_brace)
        visited.append(nearest_opening_brace_to_that_closing)  # then, append these two tokens to the visited list


def read(tokens: List[Token]) -> Children:

    """This function produces wood of Expressions/Literals"""

    if not tokens:
        return []  # allow empty expressions, useful for empty function parameters like: (defn my-function () ...)

    children: Children = []
    idx: int = 0

    while idx < len(tokens):
        current_token = tokens[idx]
        if current_token.type() == Token.OpeningBrace:  # <- if read() function has encountered OpeningBrace token
            left_boundary, right_boundary = idx + 1, boundary(tokens[idx:]) + idx  # <---------- define boundaries
            children.append(Expression(read(tokens[left_boundary:right_boundary])))  # <-------- append expression
            idx = right_boundary + 1  # and then let the read() function to advance to the next one token instance
        else:
            children.append(Literal(current_token))  # <------------------------------------------- append literal
            idx += 1  # <-------------- and then let the read() function to advance to the next one token instance

    return children   # <-------------- so at the end of the day, return a list of Expression or Literal instances
