from copy import deepcopy

class ConfigMeta(type):
    def __new__(mcls, name, bases, cdict):
        lament = []
        _default = {}
        _export = []

        def _getattr(self, name):
            if name in self.lament:
                return self._config[name]
            else:
                super(object, self).__getattr__(name)

        allowed = set(['__module__', '__metaclass__', '__doc__'])
        for key, value in cdict.items():
            if key not in allowed:
                if hasattr(value, '__lament__'):
                    lament.append(value.__lament__)
                    _default[value.__lament__] = value.__conf__
                    cdict['_%s' % key] = value
                    del cdict[key]
                if hasattr(value, '__export__'):
                    _export.append(value.__export__)
                    cdict['_ex_%s' % value.__export__] = value

        cdict['lament'] = lament
        cdict['_default']  = _default
        cdict['_export']  = _export
        cdict['_config'] = {}
        cdict['__getattr__'] = _getattr

        return super(ConfigMeta, mcls).__new__(mcls, name, bases, cdict)

def config(key, default):
    def _con(func):
        setattr(func, '__lament__', key)
        setattr(func, '__conf__', default)
        return func
    return _con

def export(key):
    def _exp(func):
        setattr(func, '__export__', key)
        return func
    return _exp
