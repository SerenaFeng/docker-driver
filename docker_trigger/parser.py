import yaml


__all__ = ['YamlParser']

class YamlParser(object):
    def __init__(self, path):
        self.data = {}
        self.testcases = []
        self.path = path

    def load_files(self):
        pass

    def get_testcase(self):
        with open(self.path, 'r') as fd:
            return yaml.safe_load(fd)
