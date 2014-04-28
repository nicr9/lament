import unittest

from tempfile import NamedTemporaryFile as TF
from json import dump
from os import remove

from meta import config, regex_config, export
from base import LamentConfig

# Constants
ABCD = {'a': 'b', 'c': 'd'}
EFGH = {'e': 'f', 'g': 'h'}

ALL_LETTERS = {}
ALL_LETTERS.update(ABCD)
ALL_LETTERS.update(EFGH)

# Example subclass
class ExampleConfig(LamentConfig):
    @config('str_type', str)
    def str_type(self, config, obj):
        if isinstance(obj, str):
            return obj
        return config

    @config('list_type', list)
    def list_type(self, config, obj):
        if isinstance(obj, list):
            return obj
        config.append(obj)
        return config

    @config('dict_type', dict)
    def dict_type(self, config, obj):
        if isinstance(obj, dict):
            config.update(obj)
        return config

    @config('bool_type', bool)
    def bool_type(self, config, obj):
        return obj

    @config('list_int_only', list)
    def list_int_only(self, config, obj):
        if isinstance(obj, list):
            config.extend(obj)
        else:
            config.append(obj)
        return config

    @regex_config('regex_string', '.*', str)
    def regex_string(self, config, obj):
        if isinstance(obj, str):
            return obj
        else:
            return config

    @export('list_int_only')
    def export_int_only(self, obj):
        return [z for z in obj if isinstance(z, int)]

class TestLamentConfig(unittest.TestCase):
    def _check_values(self, config, vals, re_vals):
        # Check all keys are there
        self.assertEqual(
                set(config._config_keys),
                set(vals.keys())
                )

        # Check all regex keys are there
        self.assertEqual(
                set(config._re_keys),
                set(re_vals.keys())
                )

        # Check key values
        self.assertEqual(config.str_type, vals['str_type'])
        self.assertEqual(config.list_type, vals['list_type'])
        self.assertEqual(config.dict_type,vals['dict_type'])
        self.assertEqual(config.bool_type, vals['bool_type'])
        self.assertEqual(config.list_int_only, vals['list_int_only'])

        # Check regex keys contain dicts
        self.assertEqual(config.regex_string, re_vals['regex_string'])

    def test_create(self):
        # Create with default values
        temp = ExampleConfig()

        self._check_values(temp, {
            'str_type': '',
            'list_type': [],
            'dict_type': {},
            'bool_type': False,
            'list_int_only': [],
            },
            {
            'regex_string': {},
            })

        # Create with overridden values
        temp = ExampleConfig(
                str_type='hi',
                list_type=5,
                dict_type=ABCD,
                bool_type=True,
                list_int_only=1,
                )

        self._check_values(temp, {
            'str_type': 'hi',
            'list_type': [5],
            'dict_type': ABCD,
            'bool_type': True,
            'list_int_only': [1],
            },
            {
            'regex_string': {},
            })

    def test_alter(self):
        # Create with default values
        temp = ExampleConfig()

        self._check_values(temp, {
            'str_type': '',
            'list_type': [],
            'dict_type': {},
            'bool_type': False,
            'list_int_only': [],
            },
            {
            'regex_string': {},
            })

        # Update values
        temp.update(str_type='ello')
        temp.update(list_type='1')
        temp.update(dict_type=EFGH)
        temp.update(bool_type=True)
        temp.update(list_int_only=[1, 2, 3])
        temp.update(**{'regex_string mario': 'luigi'})

        self._check_values(temp, {
            'str_type': 'ello',
            'list_type': ['1'],
            'dict_type': EFGH,
            'bool_type': True,
            'list_int_only': [1, 2, 3],
            },
            {
            'regex_string': {
                'mario': 'luigi',
                },
            })

        # Create with overridden values
        temp = ExampleConfig(
                str_type='hi',
                list_type=5,
                dict_type=ABCD,
                bool_type=True,
                **{'regex_string mario': 'luigi'}
                )

        self._check_values(temp, {
            'str_type': 'hi',
            'list_type': [5],
            'dict_type': ABCD,
            'bool_type': True,
            'list_int_only': [],
            },
            {
            'regex_string': {
                'mario': 'luigi',
                },
            })

        # Update values
        temp.update(str_type='ello')
        temp.update(list_type=1)
        temp.update(dict_type=EFGH)
        temp.update(bool_type=True)
        temp.update(**{'regex_string sonic': 'tails'})

        self._check_values(temp, {
            'str_type': 'ello',
            'list_type': [5, 1],
            'dict_type': ALL_LETTERS,
            'bool_type': True,
            'list_int_only': [],
            },
            {
            'regex_string': {
                'mario': 'luigi',
                'sonic': 'tails',
                },
            })

    def test_from_file(self):
        with TF(delete=False) as f:
            first = f.name
            dump({
                'str_type':'foo',
                'list_type': [1, 2, 3],
                'dict_type': ABCD,
                'bool_type': True,
                'list_int_only': [],
                'regex_string mario': 'luigi',
                }, f)

        with TF(delete=False) as f:
            second = f.name
            dump({
                'str_type':'bar',
                'list_type': [4, 5, 6],
                'dict_type': EFGH,
                'bool_type': False,
                'list_int_only': [],
                'regex_string sonic': 'tails',
                }, f)

        temp = ExampleConfig.from_file(first)
        self._check_values(temp, {
            'str_type': 'foo',
            'list_type': [1, 2, 3],
            'dict_type': ABCD,
            'bool_type': True,
            'list_int_only': [],
            },
            {
            'regex_string': {
                'mario': 'luigi',
                },
            })

        temp.update_from_file(second)
        self._check_values(temp, {
            'str_type': 'bar',
            'list_type': [4, 5, 6],
            'dict_type': ALL_LETTERS,
            'bool_type': False,
            'list_int_only': [],
            },
            {
            'regex_string': {
                'mario': 'luigi',
                'sonic': 'tails',
                },
            })

        # Clean up
        remove(first)
        remove(second)

    def test_default(self):
        temp = ExampleConfig()
        self._check_values(temp, {
            'str_type': '',
            'list_type': [],
            'dict_type': {},
            'bool_type': False,
            'list_int_only': [],
            },
            {
            'regex_string': {},
            })

    def test_wrong_type(self):
        temp = ExampleConfig(
                str_type=10,
                dict_type=10,
                bool_type=0,
                **{'regex_string badtype': 2}
                )
        self._check_values(temp, {
            'str_type': '',
            'list_type': [],
            'dict_type': {},
            'bool_type': False,
            'list_int_only': [],
            },
            {
            'regex_string': {},
            })

    def test_export(self):
        temp = ExampleConfig(
                str_type='Blah',
                list_type=10,
                dict_type=ABCD,
                bool_type=True,
                list_int_only=1
                )
        self.assertEqual(
                temp.export(),
                {
                    'str_type': 'Blah',
                    'list_type': [10],
                    'dict_type': ABCD,
                    'bool_type': True,
                    'list_int_only': [1],
                    }
                )

        # Update values
        temp.update(str_type='ello')
        temp.update(list_type=1)
        temp.update(dict_type=EFGH)
        temp.update(bool_type=False)
        temp.update(list_int_only='b')
        self.assertEqual(
                temp.export(),
                {
                    'str_type': 'ello',
                    'list_type': [10, 1],
                    'dict_type': ALL_LETTERS,
                    'bool_type': False,
                    'list_int_only': [1],
                    }
                )

    def test_to_file(self):
        before = ExampleConfig(
                str_type='Blah',
                list_type=10,
                dict_type=ABCD,
                bool_type=True,
                list_int_only=1
                )

        with TF(delete=False) as f:
            first = f.name
            before.export_to_file(first)

        after = ExampleConfig.from_file(first)
        self._check_values(after, {
            'str_type': 'Blah',
            'list_type': [10],
            'dict_type': ABCD,
            'bool_type': True,
            'list_int_only': [1],
            },
            {
            'regex_string': {},
            })

        before2 = ExampleConfig(
                str_type='bar',
                list_type=[4, 5, 6],
                dict_type=EFGH,
                bool_type=False,
                list_int_only='b'
                )

        with TF(delete=False) as f:
            second = f.name
            before2.export_to_file(second)

        after2 = ExampleConfig.from_file(second)
        self._check_values(after2, {
            'str_type':'bar',
            'list_type': [4, 5, 6],
            'dict_type': EFGH,
            'bool_type': False,
            'list_int_only': [],
            },
            {
            'regex_string': {},
            })

        # Clean up
        remove(first)
        remove(second)
