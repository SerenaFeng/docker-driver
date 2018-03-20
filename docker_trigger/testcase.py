import os
import logging

from docker_trigger import constants
from docker_trigger import parser
from docker_trigger import trigger
from docker_trigger.publish import functest

LOG = logging.getLogger(__file__)


def get_file(name):
    return os.path.join(constants.TESTDEF_PATH, '{}.yaml'.format(name))


class TestCase(object):
    def __init__(self, name, publish=False):
        self.__name = name
        self.__publish = publish
        self.__file = get_file(name)
        self.__testcase = None

    def run(self):
        if not os.path.isfile(self.__file):
            LOG.error('testcase {} not supported'.format(self.__file))
            return

        LOG.info('run testcase {}'.format(self.__file))
        self.__testcase = parser.YamlParser(self.__file).data.get('testcase')
        self.testing()

    def testing(self):
        trigger.Trigger(self.__testcase.get('trigger')).run()

    def publish(self):
        publisher = self.__testcase.get('publisher', [])
        return getattr(functest, publisher)().parse()
