from re import match
from config import ConfigFile
from meta import ConfigMeta
from collections import defaultdict

def _get_instances(types, values):
    # Each option should start with an instance of it's type
    defaults = {key: val() for key, val in types.iteritems()}

    # This may be replaced with a user specified instance of that type
    overrides = {key: val
            for key, val in values.iteritems()
            if isinstance(val, types[key])}
    defaults.update(overrides)

    return defaults

class LamentConfig(object):
    __metaclass__ = ConfigMeta

    def __init__(self, **kwargs):
        self._config = _get_instances(self._defaults, self._default_values)
        self._re_config = defaultdict(dict)
        self.update(**kwargs)

    @classmethod
    def from_file(cls, file_path):
        temp = cls()
        temp.update_from_file(file_path)
        return temp

    def update_from_file(self, file_path):
        try:
            with ConfigFile(file_path) as inp:
                self.update(**inp)
        except Exception:
            pass

    def update(self, **kwargs):
        for key, val in kwargs.iteritems():
            # JSON produces unicode instead of str
            if isinstance(val, unicode):
                val = str(val)

            # Regular key
            if key in self._config_keys:
                self._config[key] = getattr(self, '_con_%s' % key)(
                        self._config[key],
                        val
                        )
                continue

            # Regex key
            split_key = key.split()
            if len(split_key) == 2:
                key, sub = split_key
                if self._re_match(key, sub):
                    new = getattr(self, '_re_con_%s' % key)(
                            self._re_oldval(key, sub),
                            val
                            )

                    # If new val is None, take it out of config
                    if new is None and sub in self._re_config[key]:
                        del self._re_config[key][sub]
                    elif new is not None:
                        self._re_config[key][sub] = new

    def _re_match(self, key, sub):
        return key in self._re_keys and match(self._re_patterns[key], sub)

    def _re_oldval(self, key, sub):
        return self._re_config[key].get(sub, None)

    def export_to_file(self, file_path):
        with ConfigFile(file_path, True) as outp:
            outp.clear() # We want to overwrite the file, not update
            outp.update(self.export())

    def export(self):
        temp = {}
        for key in self._config_keys:
            if key in self._export_keys:
                temp[key] = getattr(self, '_ex_%s' % key)(
                        self._config[key]
                        )
            else:
                temp[key] = self._config[key]

        for key in self._re_keys:
            for sub in self._re_config[key].iterkeys():
                full_key = '%s %s' % (key, sub)
                if key in self._export_keys:
                    temp[full_key] = getattr(self, '_ex_%s' % key)(
                            self._re_config[key][sub]
                            )
                else:
                    temp[full_key] = self._re_config[key][sub]

        return temp
