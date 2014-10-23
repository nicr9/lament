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

SUPER_MARIO = {'regex_string mario': 'luigi'}
SONIC_HEDGEHOG = {'regex_string sonic': 'tails'}
RES_MARIO = {'mario': 'luigi'}
RES_SONIC = {'sonic': 'tails'}
ALL_VIDEOGAMES = {}
ALL_VIDEOGAMES.update(RES_MARIO)
ALL_VIDEOGAMES.update(RES_SONIC)

GOOGLE = {'regex_tuple www.google.com': 'localhost:443'}
YAHOO = {'regex_tuple www.yahoo.com': 'localhost:80'}
RES_GOOGLE = {'www.google.com': ('localhost', 443)}
RES_YAHOO = {'www.yahoo.com': ('localhost', 80)}
ALL_WEBSITES = {}
ALL_WEBSITES.update(RES_GOOGLE)
ALL_WEBSITES.update(RES_YAHOO)

FIRST_RE_CONF = {}
FIRST_RE_CONF.update(SUPER_MARIO)
FIRST_RE_CONF.update(GOOGLE)

SECOND_RE_CONF = {}
SECOND_RE_CONF.update(SONIC_HEDGEHOG)
SECOND_RE_CONF.update(YAHOO)

STR_W_DEFAULT = "The cake is a lie."

DEFAULT_VALS = {
        'str_type': '',
        'str_w_default': STR_W_DEFAULT,
        'list_type': [],
        'dict_type': {},
        'bool_type': False,
        'list_int_only': [],
        }
DEFAULT_RE_VALS = {
        'regex_string': {},
        'regex_tuple': {},
        }

# Example subclass
class ExampleConfig(LamentConfig):
    @config('str_type', str)
    def str_type(self, config, obj):
        if isinstance(obj, str):
            return obj
        return config

    @config('str_w_default', str, default_value=STR_W_DEFAULT)
    def str_w_default(self, config, obj):
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

    @regex_config('regex_tuple', '.*\..*\.com', tuple)
    def regex_tuple(self, config, obj):
        host, port = obj.split(':')[:2]
        return (host, int(port))

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
        self.assertEqual(config.str_w_default, vals['str_w_default'])
        self.assertEqual(config.list_type, vals['list_type'])
        self.assertEqual(config.dict_type,vals['dict_type'])
        self.assertEqual(config.bool_type, vals['bool_type'])
        self.assertEqual(config.list_int_only, vals['list_int_only'])

        # Check regex keys contain dicts
        self.assertEqual(config.regex_string, re_vals['regex_string'])
        self.assertEqual(config.regex_tuple, re_vals['regex_tuple'])

    def test_create(self):
        # Create with default values
        temp = ExampleConfig()

        self._check_values(temp, DEFAULT_VALS, DEFAULT_RE_VALS)

        # Create with overridden values
        temp = ExampleConfig(
                str_type='hi',
                str_w_default='The cake is not a lie.',
                list_type=5,
                dict_type=ABCD,
                bool_type=True,
                list_int_only=1,
                **FIRST_RE_CONF
                )

        self._check_values(temp, {
            'str_type': 'hi',
            'str_w_default': 'The cake is not a lie.',
            'list_type': [5],
            'dict_type': ABCD,
            'bool_type': True,
            'list_int_only': [1],
            },
            {
                'regex_string': RES_MARIO,
                'regex_tuple': RES_GOOGLE,
                }
            )

    def test_alter(self):
        # Create with default values
        temp = ExampleConfig()

        self._check_values(temp, DEFAULT_VALS, DEFAULT_RE_VALS)

        # Update values
        temp.update(str_type='ello')
        temp.update(str_w_default='Blah!')
        temp.update(list_type='1')
        temp.update(dict_type=EFGH)
        temp.update(bool_type=True)
        temp.update(list_int_only=[1, 2, 3])
        temp.update(**FIRST_RE_CONF)

        self._check_values(temp, {
            'str_type': 'ello',
            'str_w_default': 'Blah!',
            'list_type': ['1'],
            'dict_type': EFGH,
            'bool_type': True,
            'list_int_only': [1, 2, 3],
            },
            {
            'regex_string': RES_MARIO,
            'regex_tuple': RES_GOOGLE,
            })

        # Create with overridden values
        temp = ExampleConfig(
                str_type='hi',
                str_w_default='hello',
                list_type=5,
                dict_type=ABCD,
                bool_type=True,
                **SECOND_RE_CONF
                )

        self._check_values(temp, {
            'str_type': 'hi',
            'str_w_default': 'hello',
            'list_type': [5],
            'dict_type': ABCD,
            'bool_type': True,
            'list_int_only': [],
            },
            {
            'regex_string': RES_SONIC,
            'regex_tuple': RES_YAHOO,
            })

        # Update values
        temp.update(str_type='ello')
        temp.update(str_w_default='Hello darkness my old friend...')
        temp.update(list_type=1)
        temp.update(dict_type=EFGH)
        temp.update(bool_type=True)
        temp.update(**FIRST_RE_CONF)

        self._check_values(temp, {
            'str_type': 'ello',
            'str_w_default': 'Hello darkness my old friend...',
            'list_type': [5, 1],
            'dict_type': ALL_LETTERS,
            'bool_type': True,
            'list_int_only': [],
            },
            {
            'regex_string': ALL_VIDEOGAMES,
            'regex_tuple': ALL_WEBSITES,
            })

    def test_from_file(self):
        with TF(delete=False) as f:
            first = f.name
            temp = {
                'str_type':'foo',
                'str_w_default':'foobar',
                'list_type': [1, 2, 3],
                'dict_type': ABCD,
                'bool_type': True,
                'list_int_only': [],
                }
            temp.update(FIRST_RE_CONF)
            dump(temp, f)

        with TF(delete=False) as f:
            second = f.name
            temp = {
                'str_type':'bar',
                'str_w_default':'fizzbang',
                'list_type': [4, 5, 6],
                'dict_type': EFGH,
                'bool_type': False,
                'list_int_only': [],
                }
            temp.update(SECOND_RE_CONF)
            dump(temp, f)

        temp = ExampleConfig.from_file(first)
        self._check_values(temp, {
            'str_type': 'foo',
            'str_w_default': 'foobar',
            'list_type': [1, 2, 3],
            'dict_type': ABCD,
            'bool_type': True,
            'list_int_only': [],
            },
            {
            'regex_string': RES_MARIO,
            'regex_tuple': RES_GOOGLE,
            })

        temp.update_from_file(second)
        self._check_values(temp, {
            'str_type': 'bar',
            'str_w_default': 'fizzbang',
            'list_type': [4, 5, 6],
            'dict_type': ALL_LETTERS,
            'bool_type': False,
            'list_int_only': [],
            },
            {
            'regex_string': ALL_VIDEOGAMES,
            'regex_tuple': ALL_WEBSITES,
            })

        # Clean up
        remove(first)
        remove(second)

    def test_default(self):
        temp = ExampleConfig()
        self._check_values(temp, DEFAULT_VALS, DEFAULT_RE_VALS)

    def test_wrong_type(self):
        temp = ExampleConfig(
                str_type=10,
                str_w_default=10,
                dict_type=10,
                bool_type=0,
                **{'regex_string badtype': 2}
                )
        self._check_values(temp, DEFAULT_VALS, DEFAULT_RE_VALS)

    def test_export(self):
        temp = ExampleConfig(
                str_type='Blah',
                str_w_default='Moo!',
                list_type=10,
                dict_type=ABCD,
                bool_type=True,
                list_int_only=1,
                **SUPER_MARIO
                )
        self.assertEqual(
                temp.export(),
                {
                    'str_type': 'Blah',
                    'str_w_default': 'Moo!',
                    'list_type': [10],
                    'dict_type': ABCD,
                    'bool_type': True,
                    'list_int_only': [1],
                    'regex_string mario': 'luigi',
                    }
                )

        # Update values
        temp.update(str_type='ello')
        temp.update(str_w_default='goodbye')
        temp.update(list_type=1)
        temp.update(dict_type=EFGH)
        temp.update(bool_type=False)
        temp.update(list_int_only='b')
        temp.update(**SONIC_HEDGEHOG)
        self.assertEqual(
                temp.export(),
                {
                    'str_type': 'ello',
                    'str_w_default': 'goodbye',
                    'list_type': [10, 1],
                    'dict_type': ALL_LETTERS,
                    'bool_type': False,
                    'list_int_only': [1],
                    'regex_string mario': 'luigi',
                    'regex_string sonic': 'tails',
                    }
                )

    def test_to_file(self):
        before = ExampleConfig(
                str_type='Blah',
                str_w_default='Moo!',
                list_type=10,
                dict_type=ABCD,
                bool_type=True,
                list_int_only=1,
                **SUPER_MARIO
                )

        with TF(delete=False) as f:
            first = f.name
            before.export_to_file(first)

        after = ExampleConfig.from_file(first)
        self._check_values(after, {
            'str_type': 'Blah',
            'str_w_default': 'Moo!',
            'list_type': [10],
            'dict_type': ABCD,
            'bool_type': True,
            'list_int_only': [1],
            },
            {
            'regex_string': RES_MARIO,
            'regex_tuple': {},
            })

        before2 = ExampleConfig(
                str_type='bar',
                str_w_default='foo',
                list_type=[4, 5, 6],
                dict_type=EFGH,
                bool_type=False,
                list_int_only='b',
                **SONIC_HEDGEHOG
                )

        with TF(delete=False) as f:
            second = f.name
            before2.export_to_file(second)

        after2 = ExampleConfig.from_file(second)
        self._check_values(after2, {
            'str_type':'bar',
            'str_w_default':'foo',
            'list_type': [4, 5, 6],
            'dict_type': EFGH,
            'bool_type': False,
            'list_int_only': [],
            },
            {
            'regex_string': RES_SONIC,
            'regex_tuple': {},
            })

        # Clean up
        remove(first)
        remove(second)
