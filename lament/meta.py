class ConfigMeta(type):
    def __new__(mcls, name, bases, cdict):
        _config_keys = []
        _defaults = {}
        _default_values = {}
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
                raise AttributeError(
                        "Couldn't find '%s' in schema definition." % name
                        )

        ignored_keys = set(['__module__', '__metaclass__', '__doc__'])
        for key, value in cdict.items():
            if key not in ignored_keys:

                if hasattr(value, '__lament_con__'):
                    _config_keys.append(key)
                    _defaults[key] = value.__lament_df__
                    if value.__lament_dv__ is not None:
                        _default_values[key] = value.__lament_dv__
                    cdict['_con_%s' % key] = value
                    del cdict[key]

                if hasattr(value, '__lament_re_con__'):
                    _re_keys.append(key)
                    _re_patterns[key] = value.__lament_re_pattern__
                    _re_defaults[key] = value.__lament_re_df__
                    cdict['_re_con_%s' % key] = value
                    del cdict[key]

                if hasattr(value, '__lament_ex__'):
                    _export_keys.append(value.__lament_ex__)
                    cdict['_ex_%s' % value.__lament_ex__] = value

        cdict['_config_keys'] = _config_keys
        cdict['_defaults']  = _defaults
        cdict['_default_values']  = _default_values

        cdict['_re_keys'] = _re_keys
        cdict['_re_patterns'] = _re_patterns
        cdict['_re_defaults'] = _re_defaults

        cdict['_export_keys']  = _export_keys

        cdict['_config'] = {}
        cdict['_re_config'] = {key: {} for key in _re_keys}
        cdict['__getattr__'] = _getattr

        return super(ConfigMeta, mcls).__new__(mcls, name, bases, cdict)

def config(default_type, default_value=None):
    def _con(func):
        setattr(func, '__lament_con__', None)
        setattr(func, '__lament_df__', default_type)
        setattr(func, '__lament_dv__', default_value)
        return func
    return _con

def regex_config(pattern, default_type):
    def _con(func):
        setattr(func, '__lament_re_con__', None)
        setattr(func, '__lament_re_pattern__', pattern)
        setattr(func, '__lament_re_df__', default_type)
        return func
    return _con

def export(key):
    def _exp(func):
        setattr(func, '__lament_ex__', key)
        return func
    return _exp
