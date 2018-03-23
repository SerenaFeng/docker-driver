import logging

LOG = logging.getLogger(__file__)


class Post(object):
    def __init__(self, runner, **kwargs):
        self.runner = runner

    def work(self):
        LOG.info('post process for Functest')
