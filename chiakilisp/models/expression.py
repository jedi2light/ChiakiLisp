from typing import List, Any, Callable
from chiakilisp.models.token import Token
from chiakilisp.models.operand import Operand, NotFound

Child = Operand or 'Expression'  # define a type for a single child
Children = List[Child]  # define a type describing list of children


class Expression:

    """
    Expression is the class that indented to be used to calculate something
    """

    _children: List[Operand or "Expression"]

    def __init__(self, children: List[Operand or 'Expression']) -> None:

        """Initialize Expression instance"""

        self._children = children

    def children(self) -> Children:

        """Returns expression children"""

        return self._children

    def execute(self, environ: dict, top: bool = True) -> Any:

        """Execute here, is the return Python value related to the expression: string, number and vice versa"""

        head: Operand
        tail: Children
        head, *tail = self.children()
        assert head.token().type() == Token.Identifier, 'Expression::execute(): head of expression !== identifier'

        if head.token().value().startswith('.'):
            assert len(tail) >= 1, 'Expression::execute(): dot-special-form: expected at least one argument there'
            object_name: Operand
            method_args: Children
            object_name, *method_args = head
            method_name: str = head.token().value()[1:]  # cutting . character from the beginning, gives us a name
            object_instance = object_name.execute(environ, False)
            method_handler: Callable = getattr(object_instance, method_name, NotFound)  # NotFound is a stub class
            assert method_handler is not NotFound, 'Expression::execute(): dot-special-form: can\'t find a method'
            return method_handler(*(child.execute(environ, False) for child in method_args))  # execute method !!!

        if head.token().value() == 'if':
            assert len(tail) == 3, 'Expression::execute(): if-special-form: expected exactly three arguments here'
            cond, true, false = tail
            return true.execute(environ, False) if cond.execute(environ, False) else false.execute(environ, False)

        if head.token().value() == 'let':
            assert len(tail) >= 1, 'Expression::execute(): let-special-form: expected at least one argument there'
            bindings, *body = tail
            assert isinstance(bindings, Expression), 'Expression::execute() let-special-form: wrong bindings type'
            let = {}
            items = bindings.children()  # once again, lexically, this sounds a bit weird, we have to deal with it
            assert len(items) % 2 == 0, 'Expression::execute() let-special-form: bindings should have even length'
            let.update(environ)  # we can't just bootstrap 'let' environ, because we do not want instances linking
            for name, value in (items[i:i + 2] for i in range(0, len(items), 2)):
                assert name.token().type() == Token.Identifier, 'Expression::execute() let-special-form: is wrong'
                let.update({name.token().value(): value.execute(let, False)})
            return [child.execute(let, False) for child in body][-1]  # #  then return the last calculation result

        if head.token().value() == 'fn':
            assert len(tail) >= 1, "Expression::execute(): fn-special-form: expected at least two arguments there"
            parameters, *body = tail
            assert isinstance(parameters, Expression), 'Expression::execute(): fn-special-form: wrong parameters!'
            names = []
            for parameter in parameters.children():  # lexically, it sounds a bit weird, but have to deal with it.
                assert parameter.token().type() == Token.Identifier, 'Expression::execute(): fn-special-form: !!!'
                names.append(parameter.token().value())

            def handle(*c_arguments):

                """User-function handle"""

                arity = len(names)
                assert len(c_arguments) == len(names), f'fn: wrong arity, expected exactly {arity} arguments here'

                closure = {}
                closure.update(environ)  # #       update (not bootstrap!) closure environment with the global one
                closure.update(dict(zip(names, c_arguments)))  # #          update closure environ with parameters
                return [child.execute(closure, False) for child in body][-1]  # return the last calculation result

            return handle

        if head.token().value() == 'def':
            assert top, 'Expression::execute(); def-special-form: unable to use (def) on current scope, use (let)'
            assert len(tail) == 2, 'Expression::execute(): def-special-form: incorrect arity, exactly 2 args here'
            name, value = tail
            assert name.token().type() == Token.Identifier, 'Expression:execute(): def-special-form: ! Identifier'
            executed = value.execute(environ, False)
            environ.update({name.token().value(): executed})
            return executed

        if head.token().value() == 'defn':
            assert top, 'Expression::execute(): defn-special-form, unable to use (defn ) there, use (fn)  instead'
            assert len(tail) >= 2, 'Expression::execute(): defn-special-form: wrong arity, at least two args here'
            name, parameters, *body = tail
            assert isinstance(parameters, Expression), 'Expression::execute(): defn-special-form: is invalid type'
            assert name.token().type() == Token.Identifier, 'Expression::execute(): defn-special-form: wrong type'
            names = []
            for parameter in parameters.children():  # lexically, it sounds a bit weird, but have to deal with it.
                assert parameter.token().type() == Token.Identifier, 'Expression::execute(): defn-special-form: !'
                names.append(parameter.token().value())

            def handle(*c_arguments):  # pylint: disable=E0102  # ...this handle() function could not be redefined

                """User-function handle"""

                arity = len(names)
                assert len(c_arguments) == len(names), f'fn: wrong arity, expected exactly {arity} arguments here'

                closure = {}
                closure.update(environ)  # #    _update_ closure environment with global, and not bootstrapping it
                closure.update(dict(zip(names, c_arguments)))  # #  update closure dictionary with parameter names
                return [child.execute(closure, False) for child in body][-1]  # #   return last calculation result

            environ.update({name.token().value(): handle})  # in case of 'defn', we also need to update global env
            return handle

        handle = head.execute(environ, False)
        arguments = tuple(map(lambda argument: argument.execute(environ, False), tail))
        return handle(*arguments)  # return handle execution result (which is Python 3 value) to the callee object
