import typing
import unittest
from collections import defaultdict


ResultDict = typing.Dict[typing.Any, 'ResultDict']


def to_tree(source_tree: typing.List[typing.Tuple], root_key: typing.Any = None) -> ResultDict:
    result_map = defaultdict(dict)

    for parent, element in source_tree:
        result_map[parent][element] = result_map[element]

    return result_map[root_key]


class TreeTestCase(unittest.TestCase):

    def test_default_tree(self):
        source_tree = [
            (None, 'a'),
            (None, 'b'),
            (None, 'c'),
            ('a', 'a1'),
            ('a', 'a2'),
            ('a2', 'a21'),
            ('a2', 'a22'),
            ('b', 'b1'),
            ('b1', 'b11'),
            ('b11', 'b111'),
            ('b', 'b2'),
            ('c', 'c1'),
        ]
        expected_result = {
            'a': {'a1': {}, 'a2': {'a21': {}, 'a22': {}}},
            'b': {'b1': {'b11': {'b111': {}}}, 'b2': {}},
            'c': {'c1': {}},
        }
        self.assertEqual(to_tree(source_tree), expected_result)

    def test_shuffled_tree(self):
        source_tree = [
            ('c', 'c1'),
            ('b1', 'b11'),
            (None, 'a'),
            ('a', 'a1'),
            ('a', 'a2'),
            ('a2', 'a22'),
            ('b', 'b1'),
            (None, 'b'),
            ('b11', 'b111'),
            ('b', 'b2'),
            (None, 'c'),
            ('a2', 'a21'),
        ]
        expected_result = {
            'a': {'a1': {}, 'a2': {'a21': {}, 'a22': {}}},
            'b': {'b1': {'b11': {'b111': {}}}, 'b2': {}},
            'c': {'c1': {}},
        }
        self.assertEqual(to_tree(source_tree), expected_result)

    def test_empty_tree(self):
        source_tree = []
        expected_result = {}
        self.assertEqual(to_tree(source_tree), expected_result)

    def test_broken_tree(self):
        source_tree = [
            (None, 'a'),
            (None, 'c'),
            (None, 'b'),
            ('a', 'a1'),
            ('a', 'a2'),
            ('a2', 'a21'),
            ('a2', 'a22'),
            ('b', 'b1'),
            ('b1', 'b11'),
            ('b11', 'b111'),
            ('b', 'b2'),
            ('c', 'c1'),
        ]

        expected_result = {
            'a': {'a1': {}, 'a2': {'a21': {}, 'a22': {}}},
            'b': {'b1': {'b11': {'b111': {}}}, 'b2': {}},
            'c': {'c1': {}},
        }
        self.assertEqual(to_tree(source_tree), expected_result)

    def test_fail_tree(self):
        source_tree = [
            (None, 'a'),
        ]
        expected_result = {
            'a': {'a1': {}, 'a2': {'a21': {}, 'a22': {}}},
            'b': {'b2': {}},
            'c': {'c1': {}},
        }
        self.assertNotEqual(to_tree(source_tree), expected_result)

    def test_custom_branch(self):
        custom_branch = 'b11'
        source_tree = [
            (None, 'a'),
            (None, 'b'),
            (None, 'c'),
            ('a', 'a1'),
            ('a', 'a2'),
            ('a2', 'a21'),
            ('a2', 'a22'),
            ('b', 'b1'),
            ('b1', 'b11'),
            (custom_branch, 'b111'),
            ('b', 'b2'),
            ('c', 'c1'),
        ]
        expected_result = {
            'b111': {},
        }
        self.assertEqual(to_tree(source_tree, root_key=custom_branch), expected_result)

    def test_unexpected_root_key(self):
        source_tree = []
        expected_result = {}
        self.assertEqual(to_tree(source_tree, root_key='--'), expected_result)


if __name__ == '__main__':
    unittest.main()
