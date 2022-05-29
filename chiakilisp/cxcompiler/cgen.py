# pylint: disable=line-too-long
# pylint: disable=missing-module-docstring


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
            'int main()',  # <----- wrap source in main()
            '{',  # <------- block starting marker in CPP
            *body,  # <----------- include generated code
            f'return {last}',  # <-- return last expr res
            '}\n'  # <----- block finishing marker in CPP
        ])
