#!/usr/bin/env python3
import argparse
import json
import sys

__author__ = 'darryl'


def find_key(d, keyfind):
    if isinstance(d, list):
        for i in d:
            print(find_key(i, keyfind))
        return None
    else:
        for k, v in d.items():
            if k == keyfind:
                return d[k]
            if isinstance(v, list):
                for i in v:
                    print(find_key(i, keyfind))
                return None
            elif isinstance(v, dict):
                if find_key(v, keyfind):
                    return find_key(v, keyfind)


def delete_key(d, keyfind):
    if isinstance(d, list):
        for i in d:
            d[d.index(i)] = delete_key(i, keyfind)
        return d
    else:
        for k, v in d.items():
            if k == keyfind:
                del d[k]
                return d
            elif isinstance(v, list):
                for i in v:
                    v[v.index(i)] = delete_key(i, keyfind)
                return v
            elif isinstance(v, dict):
                if find_key(v, keyfind):
                    d[k] = delete_key(v, keyfind)
                    return d


def no_args(args):
    for k in args.__dict__:
        if args.__dict__[k]:
            return False
    return True


def main():
    l = json.loads(sys.stdin.read())

    parser = argparse.ArgumentParser(description="Pretty print and modify JSON files")
    parser.add_argument('-g', '--get', dest='get', action='store', help='Display the value of a given key')
    parser.add_argument('-d', '--delete', dest='delete', action='store',
                        help='Delete a given key and display the resulting output')
    args = parser.parse_args()

    if no_args(args):
        print(json.dumps(l, indent=4, separators=(',', ': ')))

    if args.get:
        res = find_key(l, args.get)
        if res:
            print(json.dumps(res, indent=4, separators=(',', ': ')))

    if args.delete:
        res = delete_key(l, args.delete)
        print(json.dumps(res, indent=4, separators=(',', ': ')))


if __name__ == '__main__':
    main()