import os

from docker_trigger import constants
from docker_trigger import parser
from docker_trigger import runbase
from docker_trigger import trigger
from docker_trigger import worker

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
        self.before()
        self.testing()
        self.after()

    def before(self):
        self.run_tasks('before_trigger')

    def testing(self):
        trigger.Trigger(self.conf.get('trigger')).run()

    def after(self):
        self.run_tasks('after_trigger')

    def publish(self):
        self.result = self.run_tasks('publisher')
