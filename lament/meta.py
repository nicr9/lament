from copy import deepcopy

class ConfigMeta(type):
    def __new__(mcls, name, bases, cdict):
        _config_keys = []
        _defaults = {}
        _re_keys = []
        _re_patterns = {}
        _re_defaults = {}
        _export_keys = []

        def _getattr(self, name):
            if name in self._config_keys:
                return self._config[name]
            if name in self._re_keys:
                return self._re_config[name]
            else:
                super(object, self).__getattr__(name)

        allowed = set(['__module__', '__metaclass__', '__doc__'])
        for key, value in cdict.items():
            if key not in allowed:

                if hasattr(value, '__lament_con__'):
                    _config_keys.append(value.__lament_con__)
                    _defaults[value.__lament_con__] = value.__lament_df__
                    cdict['_con_%s' % key] = value
                    del cdict[key]

                if hasattr(value, '__lament_re_con__'):
                    _re_keys.append(value.__lament_re_con__)
                    _re_patterns[value.__lament_re_con__] = value.__lament_re_pattern__
                    _re_defaults[value.__lament_re_con__] = value.__lament_re_df__
                    cdict['_re_con_%s' % key] = value
                    del cdict[key]

                if hasattr(value, '__lament_ex__'):
                    _export_keys.append(value.__lament_ex__)
                    cdict['_ex_%s' % value.__lament_ex__] = value

        cdict['_config_keys'] = _config_keys
        cdict['_defaults']  = _defaults

        cdict['_re_keys'] = _re_keys
        cdict['_re_patterns'] = _re_patterns
        cdict['_re_defaults'] = _re_defaults

        cdict['_export_keys']  = _export_keys

        cdict['_config'] = {}
        cdict['_re_config'] = {key: {} for key in _re_keys}
        cdict['__getattr__'] = _getattr

        return super(ConfigMeta, mcls).__new__(mcls, name, bases, cdict)

def config(key, default):
    def _con(func):
        setattr(func, '__lament_con__', key)
        setattr(func, '__lament_df__', default)
        return func
    return _con

def regex_config(key, pattern, default):
    def _con(func):
        setattr(func, '__lament_re_con__', key)
        setattr(func, '__lament_re_pattern__', pattern)
        setattr(func, '__lament_re_df__', default)
        return func
    return _con

def export(key):
    def _exp(func):
        setattr(func, '__lament_ex__', key)
        return func
    return _exp
