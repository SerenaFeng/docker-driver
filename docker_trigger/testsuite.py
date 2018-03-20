import os
import logging

from docker_trigger import constants
from docker_trigger import parser
from docker_trigger import testcase as tc


LOG = logging.getLogger(__file__)


def get_file(name):
    return os.path.join(constants.TESTSUITE_PATH, '{}.yaml'.format(name))


class TestSuite(object):
    def __init__(self, name, publish=False):
        self.__name = name
        self.__publish = publish
        self.__file = get_file(name)
        self.__testsuite = None
        self.results = {}

    def run(self):
        if not os.path.isfile(self.__file):
            LOG.error('testsuite {} not supported'.format(self.__file))
            return

        LOG.info('run testsuite {}'.format(self.__file))
        self.__testsuite = parser.YamlParser(self.__file).data.get('testsuite')
        self.testing()
        if self.__publish:
            self.publish()

    def testing(self):
        for testcase in self.__testsuite.get('testcases'):
            instance = tc.TestCase(testcase)
            instance.run()
            if self.__publish:
                result = instance.publish()
                print testcase
                self.results[testcase] = result

    def publish(self):
        print self.results
        # for pub in self.__testsuite.get('publisher', []):
        #     os.system(pub)
