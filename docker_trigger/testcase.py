import os
import logging

from docker_trigger import constants
from docker_trigger import parser
from docker_trigger import trigger
from docker_trigger import publishers

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
        self.testing()

    def testing(self):
        trigger.Trigger(self.content.get('trigger')).run()

    def publish(self):
        publisher = self.content.get('publisher', [])
        self.result = publishers.publish(self, publisher)
