import docker
import os


class Trigger(object):
    def __init__(self, testcase):
        self.testcase = testcase
        self.client = docker.from_env()

    def prepares(self):
        pass

    def run(self):
        opts = self.get_property('opts')
        volumes = self.get_property('volumes')
        volumes = ' -v '.join(self.get_property('volumes'))
        image = self.get_property('image')
        entry = self.get_property('entry')
        if not image:
            raise Exception('image is not provided')

        cmd = 'sudo docker run {opts} -v {volumes} {image} {entry}'.format(**locals())
        os.system(cmd)

    def posts(self):
        pass

    def get_property(self, property):
        tc = self.testcase.get('testcase')
        trigger_type = tc.get('trigger-type')
        trigger = tc.get(trigger_type)
        value = trigger.get(property, '')
        return value
