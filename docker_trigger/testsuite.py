import os
import logging

from docker_trigger import constants
from docker_trigger import parser
from docker_trigger import testcase as tc


LOG = logging.getLogger(__file__)


def get_file(name):
    return os.path.join(constants.TESTSUITE_PATH, '{}.yaml'.format(name))


class TestSuite(object):
    def __init__(self, name):
        self.name = name
        self.file = get_file(name)
        self.testsuite = None

    def run(self):
        if not os.path.isfile(self.file):
            LOG.error('testsuite {} not supported'.format(self.file))
            return

        LOG.info('run testsuite {}'.format(self.file))
        self.testsuite = parser.YamlParser(self.file).data.get('testsuite')
        self.testing()
        self.post()

    def testing(self):
        for testcase in self.testsuite.get('testcases'):
            tc.TestCase(testcase).run()

    def post(self):
        for pos in self.testsuite.get('posts', []):
            os.system(pos)
