#!/usr/bin/env python3
import argparse
from collections import OrderedDict
import json
from operator import eq, ne
import re
import sys
import itertools

__author__ = 'darryl'


def get_value(d, argval):
    if isinstance(d, list):
        for i in d:
            d[d.index(i)] = get_value(i, argval)
        li = [i for i in d if i]
        if len(li) > 1:
            return sorted(li)
        else:
            try:
                return li[0]
            except IndexError:
                return []
    elif isinstance(d, dict):
        for k, v in d.items():
            if k == argval:
                return v
            elif isinstance(v, list) or isinstance(v, dict):
                return get_value(v, argval)


def remove_key(d, argval, single=True):
    if isinstance(d, list):
        return [i for i in d if remove_key(i, argval, False)]
    elif isinstance(d, dict):
        if not single:
            d = OrderedDict(sorted(d.items(), key=lambda t: t[0]))
        for k, v in d.items():
            if k == argval:
                if single:
                    del d[k]
                    return d
                return True
            elif isinstance(v, list) or isinstance(v, dict):
                return remove_key(v, argval, False)


def find_key(d, argval):
    opts = {
        '=': eq,
        '<': lambda a, b: int(a) < int(b),
        '>': lambda a, b: int(a) > int(b),
        '!': ne
    }
    pattern = re.compile('(\w+)([=><!])(\w+)')
    argvalre = re.match(pattern, argval)
    val_k = argvalre.group(1)
    val_v = argvalre.group(3)
    opt = opts[argvalre.group(2)]
    if isinstance(d, list):
        for i in d:
            d[d.index(i)] = i if find_key(i, argval) else None
        return sorted([i for i in d if i])
    elif isinstance(d, dict):
        d = OrderedDict(sorted(d.items(), key=lambda t: t[0]))
        for k, v in d.items():
            if k == val_k and opt(str(v), val_v):
                return d
            elif isinstance(v, list) or isinstance(v, dict):
                return find_key(v, argval)


def get_keys(d, keys=list()):
    if isinstance(d, list):
        for i in d:
            get_keys(i, keys)
        return sorted(keys)
    elif isinstance(d, dict):
        for k, v in d.items():
            if isinstance(v, dict) or isinstance(v, list):
                get_keys(v, keys)
            if k not in keys:
                keys.append(k)
        return sorted(keys)


def parse_index(idx_str):
    try:
        return [int(idx_str) - 1]
    except ValueError:
        r1, r2 = idx_str.split(':')
        return [int(i) for i in range(int(r1) - 1, int(r2))]


def get_index(d, argval):
    f = set(itertools.chain.from_iterable([parse_index(i) for i in argval.split(',')]))
    if isinstance(d, list):
        return [i for i in d if d.index(i) in f]


def display_values(d, argval, vals=list()):
    arg_list = argval.split(',')
    if isinstance(d, list):
        for i in d:
            return display_values(i, argval, vals)
    elif isinstance(d, dict):
        d = OrderedDict(sorted(d.items(), key=lambda t: t[0]))
        for k, v in d.items():
            if isinstance(v, dict) or isinstance(v, list):
                return display_values(v, argval, vals)
            else:
                if k not in vals and k not in arg_list:
                    vals.append(k)

    display = True
    for i in arg_list:
        if i in vals:
            display = False

    if display:
        str_keys = ','.join(vals)
        return remove_key(d, str_keys)


def main():
    global res, parser, args, argval, a
    res = dict()
    if '-h' not in sys.argv and '--help' not in sys.argv:
        res = json.loads(sys.stdin.read())
    if not isinstance(res, list):
        res = [res]
    parser = argparse.ArgumentParser(description="Pretty print and modify JSON files. "
                                                 "Exclusively reads from standard input")
    parser.add_argument('-g', '--get', dest='get', action='store',
                        help='Display the value of a given key from all entries')
    parser.add_argument('-f', '--find', dest='find', action='store',
                        help='Only display entries where a key has a certain value '
                             '(argformat: key[=<>!]value)')
    parser.add_argument('-n', '--index', dest='idx', action='store',
                        help='Display entries with given index only (argformat: 1:10,12)')
    parser.add_argument('-r', '--remove', dest='remove', action='store',
                        help='Delete a given key and display the resulting output of all entries')
    parser.add_argument('-k', '--keys', dest='keys', action='store_true',
                        help='Display the names of the keys')
    parser.add_argument('-d', '--display', dest='display', action='store',
                        help='Display output with only the given keys')
    args = parser.parse_args()

    if args.display:
        argval = args.display.split(',')
        for a in argval:
            res = display_values(res, a)

    if args.find:
        argval = args.find.split(',')
        for a in argval:
            res = find_key(res, a)

    res = get_index(res, args.idx) if args.idx else res

    if args.remove:
        argval = args.remove.split(',')
        for a in argval:
            res = remove_key(res, a)

    res = get_value(res, args.get) if args.get and not args.keys else res
    res = get_value(res, args.keys) if args.keys and not args.get else res

    if res and len(res) and str(res) != "[None]":
        print(json.dumps(res, indent=4, separators=(',', ': ')))


if __name__ == '__main__':
    main()