import docker


class Trigger(object):
    def __init__(self, testcase):
        self.testcase = testcase
        self.client = docker.from_env()

    def prepares(self):
        pass

    def run(self):
        image = self.get_property('image')
        entry = self.get_property('entry')
        if not image:
            raise Exception('image is not provided')
        print self.client.containers.run(image,
                                         command=entry,
                                         privileged=True,
                                         tty=True,
                                         detach=True,
                                         volumes=self._dict_volumes())

    def posts(self):
        pass

    def get_property(self, property):
        tc = self.testcase.get('testcase')
        trigger_type = tc.get('trigger-type')
        trigger = tc.get(trigger_type)
        value = trigger.get(property, '')
        return value

    def _dict_volumes(self):
        return {
            v.split(':')[0]: {
                'bind': v.split(':')[1],
                'mode': 'rw'
            } for v in (self.get_property('volumes'))
        }
