from config import ConfigFile
from meta import ConfigMeta
from copy import deepcopy

def _get_instances(types):
    return {key: val() for key, val in types.iteritems()}

class LamentConfig(object):
    __metaclass__ = ConfigMeta

    def __init__(self, **kwargs):
        self._config = _get_instances(self._default)
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

            if key in self.lament:
                self._config[key] = getattr(self, '_%s' % key)(
                        self._config[key],
                        val
                        )

    def export_to_file(self, file_path):
        with ConfigFile(file_path) as outp:
            outp.update(self.export)

    def export(self):
        temp = {}
        for key in self.lament:
            if key in self._export:
                temp[key] = getattr(self, '_ex_%s' % key)(
                        self._config[key]
                        )
            else:
                temp[key] = self._config[key]

        return temp
