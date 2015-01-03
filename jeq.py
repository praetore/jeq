#!/usr/bin/env python3
import argparse
import json
import sys

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
                for i in v:
                    print(get_value(i, argval))
                return None
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
                for i in v:
                    v[v.index(i)] = delete_key(i, argval)
                return v
            elif isinstance(v, dict):
                if get_value(v, argval):
                    d[k] = delete_key(v, argval)
                    return d


def find_key(d, argval):
    val_k, val_v = argval.split(':')
    if isinstance(d, list):
        for i in d:
            d[d.index(i)] = find_key(i, argval)
        return d
    else:
        for k, v in d.items():
            if k == val_k and v == val_v:
                return d
            elif isinstance(v, list):
                for i in v:
                    v[v.index(i)] = find_key(i, argval)
                return v
            elif isinstance(v, dict):
                if get_value(v, val_v):
                    return find_key(v, argval)


def get_index(d, argval):
    pass


def main():
    res = json.loads(sys.stdin.read())

    parser = argparse.ArgumentParser(description="Pretty print and modify JSON files")
    parser.add_argument('-g', '--get', dest='get', action='store',
                        help='Display the value of a given key from all entries')
    parser.add_argument('-d', '--delete', dest='delete', action='store',
                        help='Delete a given key and display the resulting output of all entries')
    parser.add_argument('-f', '--find', dest='find', action='store',
                        help='Only display entries where key has certain value')
    parser.add_argument('-n', '--index', dest='idx', action='store',
                        help='Display entries with given index only')
    args = parser.parse_args()

    if args.get:
        res = get_value(res, args.get)

    if args.find:
        res = find_key(res, args.find)

    if args.idx:
        res = get_index(res, args.idx)

    if args.delete:
        res = delete_key(res, args.delete)

    if res:
        print(json.dumps(res, indent=4, separators=(',', ': ')))


if __name__ == '__main__':
    main()