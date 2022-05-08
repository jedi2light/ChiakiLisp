from functools import reduce
from chiakilisp.utils import pprint

ENVIRONMENT = {
    '+': lambda *args: reduce(lambda acc, cur: acc+cur,  args),
    '*': lambda *args: reduce(lambda acc, cur: acc*cur,  args),
    '/': lambda *args: reduce(lambda acc, cur: acc/cur,  args),
    '-': lambda *args: reduce(lambda acc, cur: acc-cur,  args),
    'mod': lambda *args: reduce(lambda ac, cr: ac % cr,  args),
    'listy': lambda *args: list(args),    # cast them to list()
    'dicty': lambda *args: {args[idx]: args[idx+1]
                            for idx in range(0, len(args), 2)},
    'prn': pprint,
    'print': pprint,
    'println': pprint,  # we need more aliases for _print!  \O/
}
