import unittest

from tempfile import NamedTemporaryFile as TF
from json import dump
from os import remove

from meta import config, export
from base import LamentConfig

# Constants
ABCD = {'a': 'b', 'c': 'd'}
EFGH = {'e': 'f', 'g': 'h'}

ALL_LETTERS = {}
ALL_LETTERS.update(ABCD)
ALL_LETTERS.update(EFGH)

# Example subclass
class Example(LamentConfig):
    @config('hello', str)
    def hello(self, config, obj):
        if isinstance(obj, str):
            return obj
        return config

    @config('goodbye', list)
    def goodbye(self, config, obj):
        if isinstance(obj, list):
            return obj
        config.append(obj)
        return config

    @config('other', dict)
    def other(self, config, obj):
        if isinstance(obj, dict):
            config.update(obj)
        return config

    @config('is_false', bool)
    def is_false(self, config, obj):
        return obj

    @config('numbers', list)
    def numbers(self, config, obj):
        if isinstance(obj, list):
            config.extend(obj)
        else:
            config.append(obj)
        return config

    @export('numbers')
    def export_numbers(self, obj):
        return [z for z in obj if isinstance(z, int)]

class TestLamentConfig(unittest.TestCase):
    def _check_values(self, config, vals):
        # Check all keys are there
        self.assertEqual(
                set(config._config_keys),
                set(vals.keys())
                )

        # Check key values
        self.assertEqual(config.hello, vals['hello'])
        self.assertEqual(config.goodbye, vals['goodbye'])
        self.assertEqual(config.other,vals['other'])
        self.assertEqual(config.is_false, vals['is_false'])
        self.assertEqual(config.numbers, vals['numbers'])

    def test_create(self):
        # Create with default values
        temp = Example()

        self._check_values(temp, {
            'hello': '',
            'goodbye': [],
            'other': {},
            'is_false': False,
            'numbers': [],
            })

        # Create with overridden values
        temp = Example(
                hello='hi',
                goodbye=5,
                other=ABCD,
                is_false=True,
                numbers=1,
                )

        self._check_values(temp, {
            'hello': 'hi',
            'goodbye': [5],
            'other': ABCD,
            'is_false': True,
            'numbers': [1],
            })

    def test_alter(self):
        # Create with default values
        temp = Example()

        self._check_values(temp, {
            'hello': '',
            'goodbye': [],
            'other': {},
            'is_false': False,
            'numbers': [],
            })

        # Update values
        temp.update(hello='ello')
        temp.update(goodbye='1')
        temp.update(other=EFGH)
        temp.update(is_false=True)
        temp.update(numbers=[1, 2, 3])

        self._check_values(temp, {
            'hello': 'ello',
            'goodbye': ['1'],
            'other': EFGH,
            'is_false': True,
            'numbers': [1, 2, 3],
            })

        # Create with overridden values
        temp = Example(
                hello='hi',
                goodbye=5,
                other=ABCD,
                is_false=True
                )

        self._check_values(temp, {
            'hello': 'hi',
            'goodbye': [5],
            'other': ABCD,
            'is_false': True,
            'numbers': [],
            })

        # Update values
        temp.update(hello='ello')
        temp.update(goodbye=1)
        temp.update(other=EFGH)
        temp.update(is_false=True)

        self._check_values(temp, {
            'hello': 'ello',
            'goodbye': [5, 1],
            'other': ALL_LETTERS,
            'is_false': True,
            'numbers': [],
            })

    def test_from_file(self):
        with TF(delete=False) as f:
            first = f.name
            dump({
                'hello':'foo',
                'goodbye': [1, 2, 3],
                'other': ABCD,
                'is_false': True,
                'numbers': [],
                }, f)

        with TF(delete=False) as f:
            second = f.name
            dump({
                'hello':'bar',
                'goodbye': [4, 5, 6],
                'other': EFGH,
                'is_false': False,
                'numbers': [],
                }, f)

        temp = Example.from_file(first)
        self._check_values(temp, {
            'hello': 'foo',
            'goodbye': [1, 2, 3],
            'other': ABCD,
            'is_false': True,
            'numbers': [],
            })

        temp.update_from_file(second)
        self._check_values(temp, {
            'hello': 'bar',
            'goodbye': [4, 5, 6],
            'other': ALL_LETTERS,
            'is_false': False,
            'numbers': [],
            })

        # Clean up
        remove(first)
        remove(second)

    def test_default(self):
        temp = Example()
        self._check_values(temp, {
            'hello': '',
            'goodbye': [],
            'other': {},
            'is_false': False,
            'numbers': [],
            })

    def test_wrong_type(self):
        temp = Example(
                hello=10,
                other=10,
                is_false=0
                )
        self._check_values(temp, {
            'hello': '',
            'goodbye': [],
            'other': {},
            'is_false': False,
            'numbers': [],
            })

    def test_export(self):
        temp = Example(
                hello='Blah',
                goodbye=10,
                other=ABCD,
                is_false=True,
                numbers=1
                )
        self.assertEqual(
                temp.export(),
                {
                    'hello': 'Blah',
                    'goodbye': [10],
                    'other': ABCD,
                    'is_false': True,
                    'numbers': [1],
                    }
                )

        # Update values
        temp.update(hello='ello')
        temp.update(goodbye=1)
        temp.update(other=EFGH)
        temp.update(is_false=False)
        temp.update(numbers='b')
        self.assertEqual(
                temp.export(),
                {
                    'hello': 'ello',
                    'goodbye': [10, 1],
                    'other': ALL_LETTERS,
                    'is_false': False,
                    'numbers': [1],
                    }
                )

    def test_to_file(self):
        before = Example(
                hello='Blah',
                goodbye=10,
                other=ABCD,
                is_false=True,
                numbers=1
                )

        with TF(delete=False) as f:
            first = f.name
            before.export_to_file(first)

        after = Example.from_file(first)
        self._check_values(after, {
            'hello': 'Blah',
            'goodbye': [10],
            'other': ABCD,
            'is_false': True,
            'numbers': [1],
            })

        before2 = Example(
                hello='bar',
                goodbye=[4, 5, 6],
                other=EFGH,
                is_false=False,
                numbers='b'
                )

        with TF(delete=False) as f:
            second = f.name
            before2.export_to_file(second)

        after2 = Example.from_file(second)
        self._check_values(after2, {
            'hello':'bar',
            'goodbye': [4, 5, 6],
            'other': EFGH,
            'is_false': False,
            'numbers': [],
            })

        # Clean up
        remove(first)
        remove(second)
