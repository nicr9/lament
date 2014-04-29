import json
import os
import os.path

class ConfigFile(object):
    def __init__(self, config_path, create=False):
        self.head = os.path.dirname(config_path)
        if self.head == '': self.head = '.'

        self.create = create
        self.config = None

        if os.path.isdir(self.head):
            self.path = config_path
        else:
            raise Exception("%s doesn't exist" % self.head)

    def __enter__(self):
        self.config = {}

        if os.path.isfile(self.path):
            with open(self.path, 'r') as inp:
                try:
                    self.config.update(json.load(inp))
                except:
                    pass

        return self.config

    def __exit__(self, a, b, c):
        if os.path.isfile(self.path) or self.create:
            with open(self.path, 'w') as outp:
                json.dump(self.config, outp, indent=4)
