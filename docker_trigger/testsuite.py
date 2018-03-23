import os
import time

from docker_trigger import constants
from docker_trigger import modules
from docker_trigger import parser
from docker_trigger import runbase
from docker_trigger import testcase as tc


def get_file(name):
    return os.path.join(constants.TESTSUITE_PATH, '{}.yaml'.format(name))


class TestSuite(runbase.Base):
    def __init__(self, name, publish=False):
        super(TestSuite, self). __init__()
        self.name = name
        self._publish = publish
        self._file = get_file(name)
        self.conf = None
        self.testcase_runners = {}
        self.build_tag = 'experimental'
        self.duration = 0.0
        self.result = None
        self.start = None
        self.stop = None

    @runbase.file_check('testsuite')
    def run(self):
        self.log.info('run testsuite {}'.format(self._file))
        self.conf = parser.YamlParser(self._file).data.get('testsuite')
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
        self.report = self.run_module('reporter')
        print self.report

    @property
    def testcases(self):
        return self.conf.get('testcases')

    def get_testcase_runner(self, testcase):
        return self.testcase_runners.get(testcase, None)