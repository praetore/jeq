#!/usr/bin/env python3
import argparse
import json
from operator import eq, lt, gt, ne
import re
import sys
import itertools

__author__ = 'darryl'


def get_value(d, argval):
    if isinstance(d, list):
        for i in d:
            print(get_value(i, argval))
        return None
    else:
        for k, v in d.items():
            if k == argval:
                return d[k]
            if isinstance(v, list):
                return get_value(v, argval)
            elif isinstance(v, dict):
                if get_value(v, argval):
                    return get_value(v, argval)


def delete_key(d, argval):
    if isinstance(d, list):
        for i in d:
            d[d.index(i)] = delete_key(i, argval)
        return d
    else:
        for k, v in d.items():
            if k == argval:
                del d[k]
                return d
            elif isinstance(v, list):
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
    else:
        for k, v in d.items():
            if k == val_k and opt(v, val_k):
                return d
            elif isinstance(v, list):
                    return find_key(v, argval)
            elif isinstance(v, dict):
                if get_value(v, val_v):
                    return find_key(v, argval)


def parse_index(idx_str):
    try:
        return int(idx_str)
    except ValueError:
        r1, r2 = idx_str.split(':')
        return [int(i) for i in range(int(r1), int(r2)+1)]


def get_index(d, argval):
    f = set(itertools.chain([parse_index(i) for i in argval.split(',')]))
    if isinstance(d, list):
        return [i for i in d if d.index(i) in f]


def main():
    res = json.loads(sys.stdin.read())

    parser = argparse.ArgumentParser(description="Pretty print and modify JSON files")
    parser.add_argument('-g', '--get', dest='get', action='store',
                        help='Display the value of a given key from all entries')
    parser.add_argument('-f', '--find', dest='find', action='store',
                        help='Only display entries where a key has a certain value '
                             '(argformat: key[=<>!]value')
    parser.add_argument('-n', '--index', dest='idx', action='store',
                        help='Display entries with given index only (argformat: 1:10)')
    parser.add_argument('-d', '--delete', dest='delete', action='store',
                        help='Delete a given key and display the resulting output of all entries')
    parser.add_argument('-m', '--merge', dest='merge', action='store',
                        help='Merge output with other JSON file')
    parser.add_argument()
    args = parser.parse_args()

    res = find_key(res, args.find) if args.find else res
    res = delete_key(res, args.delete) if args.delete else res
    res = get_index(res, args.idx) if args.idx else res
    res = get_value(res, args.get) if args.get else res

    if res and isinstance(res, dict):
        print(json.dumps(res, indent=4, separators=(',', ': ')))


if __name__ == '__main__':
    main()