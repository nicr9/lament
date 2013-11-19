import unittest

from tempfile import NamedTemporaryFile as TF
from json import load
from os import remove, getcwd
from os.path import join, isfile

from config import ConfigFile

class TestConfigFile(unittest.TestCase):
    def test_no_dir(self):
        # Dir doesn't exist, create = false
        with self.assertRaises(Exception):
            with ConfigFile('/not/a/real.config') as x:
                pass

        # Dir doesn't exist, create = true
        with self.assertRaises(Exception):
            with ConfigFile('/not/a/real.config', True) as x:
                pass

    def test_no_file(self):
        not_a_file = join(getcwd(), 'not_a.file')
        self.assertFalse(isfile(not_a_file))

        # If create = false
        with ConfigFile(not_a_file) as config:
            self.assertEqual(config, {})
            config['something'] = "something else"
        self.assertFalse(isfile(not_a_file))

        # if create = true
        with ConfigFile(not_a_file, True) as config:
            self.assertEqual(config, {})
            config['something'] = "something else"
        self.assertTrue(isfile(not_a_file))
        with open(not_a_file, 'r') as inp:
            self.assertEqual(
                    load(inp),
                    {'something': 'something else'}
                    )
        remove(not_a_file)

    def test_saving(self):
        with TF(delete=False) as f:
            temp_name = f.name

        with ConfigFile(temp_name) as config:
            config['something'] = "something else"

        with open(temp_name, 'r') as inp:
            self.assertEqual(
                    load(inp),
                    {'something': 'something else'}
                    )

        # Clean up
        remove(temp_name)

    def test_update(self):
        with TF(delete=False) as f:
            temp_name = f.name

        with ConfigFile(temp_name) as config:
            temp = {'something': 'something else'}
            config.update(temp)

        with open(temp_name, 'r') as inp:
            self.assertEqual(
                    load(inp),
                    {'something': 'something else'}
                    )

        # Clean up
        remove(temp_name)
