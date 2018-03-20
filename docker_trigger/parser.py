import yaml


__all__ = ['YamlParser']

class YamlParser(object):
    def __init__(self, path):
        self.data = {}
        self.testcases = []
        self.path = path
        self.load_files()

    def load_files(self):
        with open(self.path, 'r') as fd:
            self.data = yaml.safe_load(fd)
