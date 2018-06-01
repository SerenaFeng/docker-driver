import logging

import docker

LOG = logging.getLogger(__file__)


class Trigger(object):
    def __init__(self, trigger_conf):
        self.trigger_conf = trigger_conf
        self.client = docker.from_env()

    def run(self):
        self.create()
        self.prepare()
        self.testing()
        self.post()

    def prepare(self):
        for pre in self._get_trigger_property('prepare'):
            LOG.info('begin to prepare: {}'.format(pre))
            self._exec_run(pre)

    def create(self):
        image = self._get_trigger_property('image')
        entry = self._get_trigger_property('entry')
        if not image:
            raise Exception('image is not provided')
        self.container = self.client.containers.run(
            image,
            command=entry,
            privileged=True,
            tty=True,
            detach=True,
            volumes=self._dict_volumes())

    def testing(self):
        for cmd in self._get_trigger_property('run'):
            LOG.info('begin to execute: {}'.format(cmd))
            self._exec_run(cmd)

    def post(self):
        for pos in self._get_trigger_property('post'):
            LOG.info('begin to post: {}'.format(pos))
            self._exec_run(pos)

    def _exec_run(self, cmd):
        (exec_code, output) = self.container.exec_run(cmd)
        if exec_code:
            raise Exception('Failed with: \n{}'.format(output))

    def _get_trigger_property(self, property):
        value = self.trigger_conf.get(property, None)
        return value

    def _dict_volumes(self):
        return {
            v.split(':')[0]: {
                'bind': v.split(':')[1],
                'mode': 'rw'
            } for v in (self._get_trigger_property('volumes'))
        }
