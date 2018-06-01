import logging

LOG = logging.getLogger(__file__)


class Before(object):
    def __init__(self, runner, **kwargs):
        self.runner = runner

    def work(self):
        LOG.info('prepare for Functest')
