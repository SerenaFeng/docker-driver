import os
import logging

from docker_trigger import constants
from docker_trigger import parser
from docker_trigger import trigger
from docker_trigger import modules

LOG = logging.getLogger(__file__)


def get_file(name):
    return os.path.join(constants.TESTDEF_PATH, '{}.yaml'.format(name))


class TestCase(object):
    def __init__(self, name):
        self._name = name
        self._file = get_file(name)
        self.content = None
        self.result = None

    def run(self):
        if not os.path.isfile(self._file):
            LOG.error('testcase {} not supported'.format(self._file))
            return

        LOG.info('run testcase {}'.format(self._file))
        self.content = parser.YamlParser(self._file).data.get('testcase')
        self.prepare()
        self.testing()
        self.post()

    def prepare(self):
        self._run_module('tc_prepare')

    def testing(self):
        trigger.Trigger(self.content.get('trigger')).run()

    def post(self):
        self._run_module('tc_post')

    def publish(self):
        self.result = self._run_module('publisher')

    def _run_module(self, field):
        module = self.content.get(field, None)
        if module:
            return modules.run_module(self, module)

        return None
