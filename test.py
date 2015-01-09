from unittest import TestCase
import unittest
from jeq import get_keys, get_value, find_key, get_index, remove_key

__author__ = 'darryl'


class JeqTest(TestCase):
    def setUp(self):
        self.foo = {"res": [{"name": "darryl", "location": "dordrecht"}], "username": "praetore"}
        self.bar = [{"key": "foo", "value": 1}, {"key": "bar", "value": 2}, {"key": "baz", "value": 3}]

    def test_get(self):
        found = get_value(self.foo, "name")
        expected = "darryl"
        self.assertEqual(found, expected)

        found = get_value(self.bar, "value")
        expected = [1, 2, 3]
        self.assertListEqual(found, expected)

    def test_find_eq(self):
        found = find_key(self.foo, "name=darryl")
        expected = self.foo
        self.assertEqual(found, expected)

        found = find_key(self.bar, "value=1")
        expected = self.bar[0]
        self.assertEqual(found, expected)

    def test_index(self):
        found = get_index(self.bar, "1:2,3")
        expected = self.bar
        self.assertListEqual(found, expected)

    def test_remove(self):
        found = remove_key(self.foo, "username")
        expected = {"res": [{"name": "darryl", "location": "dordrecht"}]}
        self.assertEqual(found, expected)

        found = remove_key(self.bar, "value")
        expected = [{"value": 1}, {"value": 2}, {"value": 3}]
        self.assertListEqual(found, expected)

    def test_keys(self):
        found = get_keys(self.foo)
        expected = sorted(["res", "name", "location", "username"])
        self.assertListEqual(found, expected)

        found = sorted(list(set(get_keys(self.bar)) - set(found)))  # wtf unittest
        expected = sorted(["key", "value"])
        self.assertListEqual(found, expected)

    def test_display(self):
        pass


if __name__ == '__main__':
    unittest.main()
