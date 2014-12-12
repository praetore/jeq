#!/usr/bin/env python3
import argparse
import fileinput
import json

__author__ = 'darryl'


def printdict(d):
    for k, v in d.items():
        if isinstance(v, list):
            for i in v:
                printdict(i)
        elif isinstance(v, dict):
            printdict(v)
        else:
            print("Key: %s\nValue: %s" % (k, v))

def find_key(d, ke):
    for k, v in d.items():
        if k == ke:
            return v
        elif isinstance(v, list):
            for i in v:
                find_key(i, ke)
        elif isinstance(v, dict):
            find_key(v, ke)


def main():
    parser = argparse.ArgumentParser(description="Pretty print and modify JSON files")
    parser.add_argument(dest='find', )
    with fileinput.input() as f_input:
        l = json.loads(f_input.readline())
        # print(json.dumps(l, indent=4, separators=(',', ': ')))
        find_key(l, "name")
        find_key(l, "email")

if __name__ == '__main__':
    main()