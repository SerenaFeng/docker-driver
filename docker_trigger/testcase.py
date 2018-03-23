import os

from docker_trigger import constants
from docker_trigger import parser
from docker_trigger import runbase
from docker_trigger import trigger


def get_file(name):
    return os.path.join(constants.TESTDEF_PATH, '{}.yaml'.format(name))


class TestCase(runbase.Base):
    def __init__(self, name):
        super(TestCase, self).__init__()
        self._name = name
        self._file = get_file(name)
        self.conf = None
        self.result = None

    @runbase.file_check('testcase')
    def run(self):
        self.log.info('run testcase {}'.format(self._file))
        self.conf = parser.YamlParser(self._file).data.get('testcase')
        self.prepare()
        self.testing()
        self.post()

    def prepare(self):
        self.run_module('tc_prepare')

    def testing(self):
        trigger.Trigger(self.conf.get('trigger')).run()

    def post(self):
        self.run_module('tc_post')

    def publish(self):
        self.result = self.run_module('publisher')

    # def _run_module(self, field):
    #     module = self.conf.get(field, None)
    #     if module:
    #         return modules.run_module(self, module)
    #
    #     return None
