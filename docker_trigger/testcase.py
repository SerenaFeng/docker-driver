import os
import logging

from docker_trigger import constants
from docker_trigger import parser
from docker_trigger import trigger


LOG = logging.getLogger(__file__)


def get_file(name):
    return os.path.join(constants.TESTDEF_PATH, '{}.yaml'.format(name))


class TestCase(object):
    def __init__(self, name):
        self.name = name
        self.file = get_file(name)
        self.testcase = None

    def run(self):
        if not os.path.isfile(self.file):
            LOG.error('testcase {} not supported'.format(self.file))
            return

        LOG.info('run testcase {}'.format(self.file))
        self.testcase = parser.YamlParser(self.file).data.get('testcase')
        self.testing()
        self.post()

    def testing(self):
        trigger.Trigger(self.testcase.get('trigger')).run()

    def post(self):
        for pos in self.testcase.get('posts', []):
            os.system(pos)
