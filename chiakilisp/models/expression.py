# pylint: disable=fixme
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=missing-module-docstring
# pylint: disable=too-many-locals
# pylint: disable=arguments-renamed
# pylint: disable=too-many-branches
# pylint: disable=too-many-statements
# pylint: disable=too-many-return-statements

from copy import deepcopy
from typing import List, Any, Callable
import chiakilisp.spec as s
from chiakilisp.spec import rules
from chiakilisp.models.literal import\
    Literal, NotFound, Nil
from chiakilisp.models.forward import\
    ExpressionType, CommonType
from chiakilisp.utils import get_assertion_closure, pairs


class ArityError(SyntaxError):

    """ArityError (just for name)"""


NE_ASSERT = get_assertion_closure(NameError)  # <-------- raises NameError
TE_ASSERT = get_assertion_closure(TypeError)  # <-------- raises TypeError
SE_ASSERT = get_assertion_closure(SyntaxError)  # <---- raises SyntaxError
RE_ASSERT = get_assertion_closure(RuntimeError)  # <-- raises RuntimeError


def IDENTIFIER_ASSERT(lit: Literal, message: str) -> None:

    """Handy shortcut to make assertion that Literal is Identifier"""

    SE_ASSERT(lit.token().position(), lit.token().is_identifier(), message)


def TAIL_IS_VALID(tail: list, rule: str, where: tuple, m_tmpl: str) -> int:

    """
    Validates tail with a certain rule, throws SyntaxError or returns arity
    """

    valid, arity, why = rules.get(rule).valid(tail)
    SE_ASSERT(where, valid, m_tmpl.format(why=why))
    return arity


class Expression(ExpressionType):

    """
    Expression is the class that indented to be used to calculate something
    """

    _children: list

    def __init__(self, children: list) -> None:

        """Initialize Expression instance"""

        self._children = children

    def children(self) -> list:

        """Returns expression children"""

        return self._children

    def dump(self, indent: int) -> None:

        """Dumps an entire expression with all its children"""

        # There is no need to annotate types, or assert() them

        children = self.children()
        if children:
            first, *rest = children
            first.dump(indent)
            for argument in rest:
                argument.dump(indent + 1)   # increment indent

    def execute(self, environ: dict, top: bool = True) -> Any:

        """Execute here, is the return Python value 3 related to the expression: string, number, and vice versa"""

        head: Literal

        assert self.children(),           'Expression[execute]: current expression is empty, unable to execute it'

        head, *tail = self.children()

        assert isinstance(head, Literal),        'Expression[execute]: head of the expression should be a Literal'
        IDENTIFIER_ASSERT(head,             'Expression[execute]: head of the expression should be an Identifier')

        where = head.token().position()  # <------------ when make assertions on expression head, this can be used

        if head.token().value() == 'or':
            if not tail:
                return None  # <-------------------------- if there are no arguments given to the form, return nil
            result = None  # <----------------------------------------------- set result to the null pointer first
            for cond in tail:  # <-------------------------------------------- for each condition in the arguments
                result = cond.execute(environ, False)  # <------------------------------------- compute the result
                if result:
                    return result  # <------------------------------------ and if there is truthy value, return it
            return result  # <------- if all conditions have been evaluated to falsy ones, return the last of them

        if head.token().value() == 'and':
            if not tail:
                return True  # <------------------------- if there are no arguments given to the form, return true
            result = None  # <----------------------------------------------- set result to the null pointer first
            for cond in tail:  # <-------------------------------------------- for each condition in the arguments
                result = cond.execute(environ, False)  # <------------------------------------- compute the result
                if not result:
                    return result  # <------------------------------------- and if there is falsy value, return it
            return result  # <------ if all conditions have been evaluated to truthy ones, return the last of them

        if head.token().value() == 'try':
            TAIL_IS_VALID(tail, 'try', where,                                   'Expression[execute]: try: {why}')
            main: CommonType = tail[0]  # <----------------------------------- assign main as a type of CommonType
            catch: Expression = tail[1]  # <--------------------------------- assign catch as a type of Expression
            TAIL_IS_VALID(catch.children(), 'catch', where,                   'Expression[execute]: catch: {why}')
            klass: Literal = catch.children()[1]  # <--------------------------- assign klass as a type of Literal
            alias: Literal = catch.children()[2]  # <--------------------------- assign alias as a type of Literal
            block: List[CommonType] = catch.children()[3:]  # <------------- assign block as a list of CommonTypes
            obj = klass.execute(environ, False)  # <---------------------------------- get actual exception object
            closure = {}  # <--------------------------------------------------- initialize a try-form environment
            closure.update(environ)  # <-------------------------------------------- update it with the global one
            try:
                return main.execute(environ, False)  # <-------------------------------- try to execute main block
            except obj as exception:  # <------------------------------------------ if exception has been occurred
                closure[alias.token().value()] = exception  # <-- associate exception instance with a chosen alias
                return [expr.execute(closure, False) for expr in block][-1]  # <- return exception handling result

        if head.token().value() == '->':
            if not tail:
                return None  # <------------------------------------------------- if there are no tail, return nil

            if len(tail) == 1:
                return tail[-1].execute(environ, False)  # <------------ if there is only one argument, execute it

            tail = deepcopy(tail)  # <--------- it could be slow when tail if really complex nested data structure

            target, *rest = tail  # <------- split tail for the first time to initialize target and rest variables
            while len(tail) > 1:  # <-- do not leave the loop while there is at least one element left in the tail
                _ = rest[0]
                if isinstance(_, Literal):
                    rest[0] = Expression([_])  # <-------- each argument except first should be cast to Expression
                rest[0].children().insert(1, target)  # <- in case of first-threading-macro, insert as the 1st arg
                tail = [rest[0]] + rest[1:]  # <- override tail: modified expression and the tail rest with offset
                target, *rest = tail  # <--------------------------- do the same we did before entering while-loop

            return target.execute(environ, False)  # <----- at the end, return target' expression execution result

        if head.token().value() == '->>':
            if not tail:
                return None  # <------------------------------------------------- if there are no tail, return nil

            if len(tail) == 1:
                return tail[-1].execute(environ, False)  # <------------ if there is only one argument, execute it

            tail = deepcopy(tail)  # <--------- it could be slow when tail if really complex nested data structure

            target, *rest = tail  # <------- split tail for the first time to initialize target and rest variables
            while len(tail) > 1:  # <-- do not leave the loop while there is at least one element left in the tail
                _ = rest[0]
                if isinstance(_, Literal):
                    rest[0] = Expression([_])  # <-------- each argument except first should be cast to Expression
                rest[0].children().append(target)  # <- in case of last-threading-macro, append to the end of args
                tail = [rest[0]] + rest[1:]  # <- override tail: modified expression and the tail rest with offset
                target, *rest = tail  # <--------------------------- do the same we did before entering while-loop

            return target.execute(environ, False)  # <----- at the end, return target' expression execution result

        if head.token().value().startswith('.') and not head.token().value() == '...':   # it could be an Ellipsis
            SE_ASSERT(where,
                      len(head.token().value()) > 1,    'Expression[execute]: dot-form: method name is mandatory')
            TAIL_IS_VALID(tail,                         'dot-form', where, 'Expression[execute]: dot-form: {why}')
            object_name: Literal  # <------------------------------------- assign object name as a type of Literal
            object_name, *method_args = tail  # <--------------- get the object name and method args from the tail
            method_alias = head.token().value()[1:]  # <------------------------------ get the method name (alias)
            object_instance = object_name.execute(environ, False)  # <--- get the object instance from environment
            SE_ASSERT(where,
                      hasattr(object_instance, '__class__'),
                      'Expression[execute]: dot-form: use object/method, module/method to invoke a static method')
            object_alias = object_instance.__class__.__name__  # <-------------- get an actual instance class name
            object_method: Callable = getattr(object_instance, method_alias, NotFound)  # <--- get a method object
            NE_ASSERT(where,
                      object_method is not NotFound,
                      f"Expression[execute]: dot-form: an '{object_alias}' object has no method '{method_alias}'")
            return object_method(*(child.execute(environ, False) for child in method_args))  # <-- return a result

        if head.token().value() == 'if':
            arity = TAIL_IS_VALID(tail, 'if', where,                             'Expression[execute]: if: {why}')
            cond, true, false = (tail if arity == 3 else tail + [Nil])  # <-- tolerate missing false-branch for if
            return true.execute(environ, False) if cond.execute(environ, False) else false.execute(environ, False)

        if head.token().value() == 'when':
            TAIL_IS_VALID(tail, 'when', where,                                 'Expression[execute]: when: {why}')
            cond, *extras = tail  # <-------------------------- false branch is always equals to nil for when-form
            return [true.execute(environ, False) for true in extras][-1] if cond.execute(environ, False) else None

        if head.token().value() == 'cond':
            if not tail:
                return None  # <------------------------------------------ if nothing has been passed, return None
            TAIL_IS_VALID(tail, 'cond', where,                                 'Expression[execute]: cond: {why}')
            for cond, expr in pairs(tail):
                if cond.execute(environ, False):
                    return expr.execute(environ, False)
            return None  # <------------------------------------------------------ if nothing is true, return None

        if head.token().value() == 'let':
            TAIL_IS_VALID(tail, 'let', where,                                   'Expression[execute]: let: {why}')
            bindings: Expression  # <------------------------------------- assign bindings as a type of Expression
            bindings, *body = tail  # <--------------------------------------- assign body as a list of CommonType
            let = {}  # <---------------------------------------------- initialize a new environment for let-block
            let.update(environ)  # <------------------------------------------------ update it with the global one
            for raw, value in pairs(bindings.children()):  # <--------------------------------- for each next pair
                if isinstance(raw, Expression):  # <------------------------ if a left-hand-side seems like a coll
                    get = environ.get('get')  # <--------------- using handy 'get' from the ChiakiLisp corelib ...
                    RE_ASSERT(where, get,    "Expression[execute]: let: destructuring requires core/get function")
                    executed = value.execute(let, False)  # <------------- and stored a value execution result ...
                    for idx, alias in enumerate(map(lambda v: v.token().value(), raw.children())):  # iterate coll
                        let.update({alias: get(executed, idx, None)})  # <---- assign nil, or indexed item of coll
                else:  # <---------------------------------------------------- the left-hand-side is an identifier
                    let.update({raw.token().value(): value.execute(let, False)})  # <- assign value to its binding
            if not body:
                body = [Nil]  # <----------- let the ... let have an empty body, in this case, result would be nil
            return [child.execute(let, False) for child in body][-1]  # <------ return the last calculation result

        if head.token().value() == 'fn':
            TAIL_IS_VALID(tail, 'fn', where,                                     'Expression[execute]: fn: {why}')
            parameters: Expression  # <--------------------------------- assign parameters as a type of Expression
            parameters, *body = tail  # <---------------------------------- assign body as the list of CommonTypes
            names = []  # <------------------------------------------------------ define a list of parameter names
            children = parameters.children()  # <---- assign children as the reference to the parameter form items
            ampersand_found = tuple(filter(lambda p: p[1].token().value() == '&', enumerate(children)))   # find &
            ampersand_position: int = ampersand_found[0][0] if ampersand_found else -1  # get '&' position (or -1)
            positional_parameters = children[:ampersand_position] if ampersand_found else children   # positionals
            positional_parameters_length = len(positional_parameters)  # <------------ remember positionals length
            for parameter in positional_parameters:  # <---------------------------- for each positional parameter
                parameter: Literal  # <------------------------------------- assign parameter as a type of Literal
                names.append(parameter.token().value())  # <--------------- append parameter name to the name list
            can_take_extras = False  # <-------------------- by default, function can not take any extra arguments
            if ampersand_found:  # <---------------- if user have specified that function can take extra arguments
                can_take_extras = True  # <- now we set this to true, as the function can now take extra arguments
                SE_ASSERT(where,
                          len(children) - 1 != ampersand_position,
                          'Expression[execute]: fn: you can only mention one alias for the extra arguments tuple')
                SE_ASSERT(where,
                          len(children) - 2 == ampersand_position,
                          'Expression[execute]: fn: you have to mention alias name for the extra arguments tuple')
                names.append(children[-1].token().value())   # append extra args param name to all parameter names
            if not body:
                body = [Nil]  # <-- let a function be defined with empty body, in such a case, it will return None
            integrity_spec_rule = s.Rule(s.Arity(s.AtLeast(positional_parameters_length)
                                                 if can_take_extras else s.Exactly(positional_parameters_length)))

            def handle(*c_arguments, **kwargs):

                """User-function handle object"""

                fn_valid, _, fn_why = integrity_spec_rule.valid(c_arguments)  # first, validate function integrity
                SE_ASSERT(where, fn_valid,                                    f'<anonymous function..>: {fn_why}')

                if can_take_extras:
                    if len(c_arguments) > positional_parameters_length:
                        e_arguments = c_arguments[positional_parameters_length:]
                        c_arguments = c_arguments[:positional_parameters_length] + (e_arguments,)  # new args list
                    else:
                        c_arguments = c_arguments + (tuple(),)  # <- if extras are possible but missing, set to ()

                fn = {}  # <------------------------------------------------- initialize new execution environment
                fn.update(environ)  # <--------------------------------------------- update it with the global one
                fn.update(dict(zip(names, c_arguments)))  # <-------------- associate parameters with their values
                fn.update({'kwargs': kwargs})  # <-------- update it with keyword arguments passed from a callback
                return [child.execute(fn, False) for child in body][-1]  # <--- return the last calculation result

            handle.x__custom_name__x = '<anonymous function>'  # <-- set function name to the <anonymous function>
            return handle  # <------------------------------------------------- return the function handler object

        if head.token().value() == 'def':
            SE_ASSERT(where, top,   'Expression[execute]: def: can only use (def) form at the top of the program')
            TAIL_IS_VALID(tail, 'def', where,                                   'Expression[execute]: def: {why}')
            name: Literal  # <--------------------------------------------------- assign name as a type of Literal
            name, value = tail  # <-------------------------------------------------- assign value as a CommonType
            executed = value.execute(environ, False)  # <-------------------------------- store the executed value
            environ.update({name.token().value(): executed})  # <------------------- assign it to its binding name
            return executed   # <----------------------------------------------------------- return executed value

        if head.token().value() == 'def?':
            SE_ASSERT(where, top, 'Expression[execute]: def?: can only use (def?) form at the top of the program')
            TAIL_IS_VALID(tail, 'def?', where,                                 'Expression[execute]: def?: {why}')
            name: Literal  # <--------------------------------------------------- assign name as a type of Literal
            name, value = tail  # <-------------------------------------------------- assign value as a CommonType
            from_env = environ.get(name.token().value()) if (name.token().value() in environ.keys()) else NotFound
            executed = value.execute(environ, False) if from_env is NotFound else from_env  # try to find existing
            environ.update({name.token().value(): executed})  # assign existing/executed value to its binding name
            return executed   # <----------------------------------------------------------- return executed value

        if head.token().value() == 'defn':
            SE_ASSERT(where, top, 'Expression[execute]: defn: can only use (defn) form at the top of the program')
            TAIL_IS_VALID(tail, 'defn', where,                                 'Expression[execute]: defn: {why}')
            name: Literal  # <--------------------------------------------------- assign name as a type of Literal
            parameters: Expression  # <--------------------------------- assign parameters as a type of Expression
            name, parameters, *body = tail  # <---------------------------- assign body as the list of CommonTypes
            names = []  # <------------------------------------------------------ define a list of parameter names
            children = parameters.children()  # <---- assign children as the reference to the parameter form items
            ampersand_found = tuple(filter(lambda p: p[1].token().value() == '&', enumerate(children)))   # find &
            ampersand_position: int = ampersand_found[0][0] if ampersand_found else -1  # get '&' position (or -1)
            positional_parameters = children[:ampersand_position] if ampersand_found else children   # positionals
            positional_parameters_length = len(positional_parameters)  # <------------ remember positionals length
            for parameter in positional_parameters:  # <---------------------------- for each positional parameter
                parameter: Literal  # <------------------------------------- assign parameter as a type of Literal
                names.append(parameter.token().value())  # <--------------- append parameter name to the name list
            can_take_extras = False  # <-------------------- by default, function can not take any extra arguments
            if ampersand_found:  # <---------------- if user have specified that function can take extra arguments
                can_take_extras = True  # <- now we set this to true, as the function can now take extra arguments
                SE_ASSERT(where,
                          len(children) - 1 != ampersand_position,
                          'Expression[execute]: defn: you can only mention one alias for the extra args\' tuple.')
                SE_ASSERT(where,
                          len(children) - 2 == ampersand_position,
                          'Expression[execute]: defn: you have to mention alias name for the extra args\' tuple.')
                names.append(children[-1].token().value())   # append extra args param name to all parameter names
            if not body:
                body = [Nil]  # <-- let a function be defined with empty body, in such a case, it will return None
            integrity_spec_rule = s.Rule(s.Arity(s.AtLeast(positional_parameters_length)
                                                 if can_take_extras else s.Exactly(positional_parameters_length)))

            def handle(*c_arguments, **kwargs):  # pylint: disable=E0102  # <- handle object couldn't be redefined

                """User-function handle object"""

                fn_valid, _, fn_why = integrity_spec_rule.valid(c_arguments)  # first, validate function integrity
                SE_ASSERT(where, fn_valid,                                    f'{name.token().value()}: {fn_why}')

                if can_take_extras:
                    if len(c_arguments) > positional_parameters_length:
                        e_arguments = c_arguments[positional_parameters_length:]
                        c_arguments = c_arguments[:positional_parameters_length] + (e_arguments,)  # new args list
                    else:
                        c_arguments = c_arguments + (tuple(),)  # <- if extras are possible but missing, set to ()

                defn = {}  # <----------------------------------------------- initialize new execution environment
                defn.update(environ)  # <------------------------------------------- update it with the global one
                defn.update(dict(zip(names, c_arguments)))  # <------------ associate parameters with their values
                defn.update({'kwargs': kwargs})  # <------ update it with keyword arguments passed from a callback
                return [child.execute(defn, False) for child in body][-1]  # <- return the last calculation result

            handle.x__custom_name__x = name.token().value()  # set function name to the user-defined function name
            environ.update({name.token().value(): handle})   # in case of 'defn' we also need to update global env
            return handle  # <------------------------------------------------- return the function handler object

        if head.token().value() == 'import':
            SE_ASSERT(where, top,    'Expression[execute]: import: you should place all the (import)s at the top')
            TAIL_IS_VALID(tail, 'import', where,                             'Expression[execute]: import: {why}')
            alias: str = tail[0].token().value()  # <------------------------------- assign alias a type of string
            parts = alias.split('.')  # <---------------- split the importable module name into a list by '.' char
            unqualified = parts[-1]  # <----------------- store the unqualified name of importable Python 3 module
            identifiers = iter(parts[1:])  # <----------------- make it possible to iterate over parts with next()
            module = __import__(alias)  # <---------------------- import the Python 3 module by its qualified name
            while module.__name__.split('.')[-1] != unqualified:  # while unqualified doesn't match an object name
                module = getattr(module, next(identifiers), None)  # lookup for an object inside of current object
            environ[unqualified] = module  # <--------------------------- assign module object to unqualified name
            return None  # <----------------------------------------------------------------------- and return nil

        if head.token().value() == 'require':
            SE_ASSERT(where, top,  'Expression[execute]: require: you should place all the (require)s at the top')
            TAIL_IS_VALID(tail, 'require', where,                           'Expression[execute]: require: {why}')
            name: Literal = tail[0]  # <----------------------------------------- assign name as a type of Literal
            module = type(name.token().value(),  (object,),  environ.get('require')(name.token().value() + '.cl'))
            environ[name.token().value().split('/')[-1]] = module  # <--- assign module object to unqualified name
            return None  # <----------------------------------------------------------------------- and return nil

        handle = head.execute(environ, False)  # resolve handle object by its name, this could raise a 'NameError'

        return handle(*tuple(map(lambda argument: argument.execute(environ,  False),  tail)))  # return the result
