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
            if get_value(i, argval):
                print(get_value(i, argval))
    elif isinstance(d, dict):
        d = OrderedDict(sorted(d.items(), key=lambda t: t[0]))
        for k, v in d.items():
            if k == argval:
                return d[k]
            elif isinstance(v, list):
                if get_value(v, argval):
                    return get_value(v, argval)
            elif isinstance(v, dict):
                if get_value(v, argval):
                    return get_value(v, argval)


def delete_key(d, argval):
    if isinstance(d, list):
        for i in d:
            d[d.index(i)] = delete_key(i, argval)
        return d
    elif isinstance(d, dict):
        d = OrderedDict(sorted(d.items(), key=lambda t: t[0]))
        for k, v in d.items():
            if k == argval:
                del d[k]
                return d
            elif isinstance(v, list):
                if get_value(v, argval):
                    return delete_key(v, argval)
            elif isinstance(v, dict):
                if get_value(v, argval):
                    d[k] = delete_key(v, argval)
                    return d


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
            d[d.index(i)] = find_key(i, argval)
        return d
    elif isinstance(d, dict):
            d = OrderedDict(sorted(d.items(), key=lambda t: t[0]))
            for k, v in d.items():
                v = str(v)
                if k == val_k and opt(v, val_v):
                    return d
                elif isinstance(v, list):
                    if get_value(v, val_k):
                        return find_key(v, argval)
                elif isinstance(v, dict):
                    if get_value(v, val_k):
                        return find_key(v, argval)


def get_keys(d, argval, shown=list()):
    if isinstance(d, list):
        for i in d:
            get_keys(i, argval, shown)
        return None
    elif isinstance(d, dict):
        d = OrderedDict(sorted(d.items(), key=lambda t: t[0]))
        for k, v in d.items():
            if isinstance(v, dict) or isinstance(v, list):
                get_keys(v, argval, shown)
            else:
                if k not in shown:
                    shown.append(k)
                    print(k)


def parse_index(idx_str):
    try:
        return [int(idx_str)]
    except ValueError:
        r1, r2 = idx_str.split(':')
        return [int(i) for i in range(int(r1), int(r2)+1)]


def get_index(d, argval):
    f = set(itertools.chain.from_iterable([parse_index(i) for i in argval.split(',')]))
    if isinstance(d, list):
        return [i for i in d if d.index(i) in f]


def main():
    res = json.loads(sys.stdin.read())

    parser = argparse.ArgumentParser(description="Pretty print and modify JSON files. "
                                                 "Exclusively reads from standard input")
    parser.add_argument('-g', '--get', dest='get', action='store',
                        help='Display the value of a given key from all entries')
    parser.add_argument('-f', '--find', dest='find', action='store',
                        help='Only display entries where a key has a certain value '
                             '(argformat: key[=<>!]value')
    parser.add_argument('-n', '--index', dest='idx', action='store',
                        help='Display entries with given index only (argformat: 1:10,12)')
    parser.add_argument('-d', '--delete', dest='delete', action='store',
                        help='Delete a given key and display the resulting output of all entries')
    parser.add_argument('-k', '--keys', dest='keys', action='store_true',
                        help='Display the names of the keys')
    args = parser.parse_args()

    res = get_index(res, args.idx) if args.idx else res

    if args.find:
        argval = args.find.split(',')
        for a in argval:
            res = find_key(res, a)

    if args.delete:
        argval = args.delete.split(',')
        for a in argval:
            res = delete_key(res, a)

    if args.get:
        get_value(res, args.get)
        res = None

    if args.keys and res:
        get_keys(res, args.keys)
        res = None

    if res and str(res) != "[None]":
        print(json.dumps(res, indent=4, separators=(',', ': ')))


if __name__ == '__main__':
    main()