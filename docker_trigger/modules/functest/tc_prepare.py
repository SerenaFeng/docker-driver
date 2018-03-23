import logging

LOG = logging.getLogger(__file__)


class Prepare(object):
    def __init__(self, runner, **kwargs):
        self.runner = runner

    def work(self):
        LOG.info('prepare for Functest')
