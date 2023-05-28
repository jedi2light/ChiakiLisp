import random

import chiakilisp.features.core as core  # import ChiakiLisp core library
import chiakilisp.features.forms as forms  # import ChiakiLisp various forms


def _bubble_sort(ls: list) -> list:

    x, y, tail = forms.bindings.let({
        forms.destructurings.list([
            'x', 'y'
        ]): ls
    }, ['x', 'y', 'tail'])

    return ls if not x or y \
        else [y, x, *_bubble_sort(tail)] if x > y else [x, *_bubble_sort(ls[1:])]


def bubble_sort(ls: list) -> list:

    bubbled = _bubble_sort(ls)
    return ls if ls == bubbled else _bubble_sort(bubbled)


source_list = [random.randint(i, i + 5) for i in range(10)]

print("Source list (randomly populated, length of the 10 numbers) =>", source_list)
print("Result list (sorted using recursive bubble sort algorithm) =>", bubble_sort(source_list))
