import os
import logging
import time

from docker_trigger import constants
from docker_trigger import parser
from docker_trigger import testcase as tc
from docker_trigger import modules

LOG = logging.getLogger(__file__)


def get_file(name):
    return os.path.join(constants.TESTSUITE_PATH, '{}.yaml'.format(name))


class TestSuite(object):
    def __init__(self, name, publish=False):
        self.name = name
        self._publish = publish
        self._file = get_file(name)
        self.content = None
        self.testcase_runners = {}
        self.build_tag = 'experimental'
        self.duration = 1.005
        self.result = None
        self.start = None
        self.stop = None

    def run(self):
        if not os.path.isfile(self._file):
            LOG.error('testsuite {} not supported'.format(self._file))
            return

        LOG.info('run testsuite {}'.format(self._file))
        self.content = parser.YamlParser(self._file).data.get('testsuite')
        self.start = time.time()
        self.testing()
        self.end = time.time()
        if self._publish:
            self.publish()

    def testing(self):
        for testcase in self.testcases:
            testcase_runner = tc.TestCase(testcase)
            self.testcase_runners[testcase] = testcase_runner
            testcase_runner.run()
            if self._publish:
                testcase_runner.publish()

    def publish(self):
        reporter = self.content.get('reporter', None)
        if reporter:
            LOG.info('begin to get report')
            self.report = modules.run_module(self, reporter)
            print self.report

    @property
    def testcases(self):
        return self.content.get('testcases')

    def get_testcase_runner(self, testcase):
        return self.testcase_runners.get(testcase, None)