#!/usr/bin/env python3

import os
import sys
import traceback
from chiakilisp.utils import pprint
from chiakilisp.lexer import Lexer
from chiakilisp.parser import Parser
from chiakilisp.environment import ENVIRONMENT

BUILTINS = globals()['__builtins__']
ENVIRONMENT.update({name: getattr(BUILTINS, name, None)
                    for name in dir(BUILTINS)})


def wood(source: str) -> list:  # sadly, no exact types

    """
    wood() method converts source to a wood of children

    :param source: str instance, containing source code
    :return: this method will return a wood of children
    """

    lexer = Lexer(source)
    lexer.lex()
    parser = Parser(lexer.tokens())
    parser.parse()
    return parser.wood()  # return wood of the Children


def require(path: str, merge: bool = False) -> dict:

    """
    require() method takes path as string, opens it,
    takes it to the parser, then returns module environ

    :param path: ChiakiLisp source path
    :param merge: whether to merge with global environ?
    :return: an executed module environment (as a dict)
    """

    with open(path, 'r', encoding='utf-8') as r:
        environment = {} if not merge else ENVIRONMENT
        if not merge:
            environment.update(ENVIRONMENT)  # then do this
        for child in wood(r.read()):
            child.execute(environment)
        return environment  # <---- return ready to use env


def execute(source: str, silent: bool = False) -> None:

    """
    execute() method convert source to AST and executes its

    :param source: ChiakiLisp valid source code as a string
    :param silent: whether print executed expression or not
    :return: returns _nothing_, only prints each result out
    """

    for child in wood(source):
        result = child.execute(ENVIRONMENT)
        if not silent:
            pprint(result)  # with the custom formatting :D


def repl() -> None:

    """Starts a REPL-like environment"""

    while True:
        try:
            source: str = input('LISP> ')  # later, it may be changed to the currently _active_ namespace' name
        except KeyboardInterrupt:  # handle Ctrl+D (exit the REPL)
            print()  # print an empty line to prevent Python 3 from printing next LISP> prompt on the same line
            continue
        except EOFError:  # handle Ctrl+C (cancel a current input)
            print()  # print an empty line to prevent host' shell to print their prompt string on the same line
            return
        if not source:  # if there is no source code for execute()
            continue
        try:
            execute(source)  # execute function also prints result
        except (Exception,) as exception:  # pylint: disable=W0703   # try to catch any possible exception here
            traceback.print_exc()  # have to manually print errors


if __name__ == '__main__':

    ENVIRONMENT['require'] = require  # <-- make it possible to require ChiakiLisp modules

    try:
        import readline  # pylint: disable=W0611                                     (>_<)
    except ImportError:
        class readline:  # pylint: disable=C0103                                     (>_<)
            """readline stub class"""

            def set_completer(self, _) -> None:
                """readline::set_completer stub method"""

            def parse_and_bind(self, _) -> None:
                """readline::parse_and_bind stub method"""
                # <------------------------------- this is for MS Windows NT compatibility

    readline.parse_and_bind("tab: complete")  # <--- allows user to complete binding names
    readline.parse_and_bind('set: blink-matching-paren on')  # <- extremely needed feature

    def completer(text, state) -> str or None:

        """Handle completions shown by GNU Readline library when the user press Tab key"""

        names = tuple(ENVIRONMENT.keys())

        return (tuple(filter(lambda name: name.startswith(text), names)) + (None,))[state]

    readline.set_completer(completer)

    if os.path.exists('corelib/core.cl'):
        require('corelib/core.cl', merge=True)  # - corelib

    if len(sys.argv) > 1:
        self: str = sys.argv[0]
        assert len(sys.argv) == 2, f'Usage: {self} [source]'
        file_path: str = sys.argv[1]
        assert os.path.exists(file_path), f'{self}: {file_path}: no such file or directory'
        assert os.path.isfile(file_path) or os.path.islink(file_path), f'{self}: {file_path}: invalid pathnode'
        with open(file_path, 'r', encoding='utf-8') as r:
            execute(r.read(), silent=True)  # <- when silent is set to True, only intentional (prn..) will work
    else:
        print('Press Ctrl+C to cancel input, press Ctrl+D to exit REPL, press Tab to see all global functions')
        repl()
