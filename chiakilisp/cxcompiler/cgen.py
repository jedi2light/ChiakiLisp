# pylint: disable=line-too-long
# pylint: disable=missing-module-docstring

from chiakilisp.models.token import Token     # :)
from chiakilisp.utils import get_assertion_closure


class CompileError(AssertionError):

    """Stub class just for the name"""


ASSERT = get_assertion_closure(CompileError)


class CPPCodeGenerator:

    """Helps to complete CPP code generation"""

    _source: list

    def __init__(self, source: list) -> None:

        """Initializes a CPPCodeGenerator instance"""

        self._source = source

    def source(self) -> list:

        """Returns holding source instance"""

        return self._source

    def generate(self, config: dict) -> str:

        """Actually returns a complete CPP code string"""

        last = self._source[-1] if self._source else '0;'

        body = self._source[:-1]

        return '\n'.join([
            '#include <string>',  # <----- include string
            '#include <chiakilisp.hpp>',  # <---- runtime
            *self._process_defs(config),  # <-- variables
            'int main(int argc, char* argv[])',  # main()
            '{',  # <------- block starting marker in CPP
            *body,  # <----------- include generated code
            f'return {last}',  # <-- return last expr res
            '}\n'  # <----- block finishing marker in CPP
        ])

    @staticmethod
    def _process_defs(config: dict) -> list:

        """This function generates the global-defs loc"""

        retval = []

        for name, value in config['DEFS'].items():
            n_value: str = name.token().value()
            v_token: Token = value.token()
            v_value: str = v_token.value()
            formatted = (f'"{v_value}"'
                         if v_token.is_string()
                         else v_value)
            retval.append(
                f'auto {n_value} = {formatted};'
            )

        return retval  # <------- return the compiled body
