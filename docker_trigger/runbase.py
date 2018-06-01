import functools
import os.path
import logging
from docker_trigger import modules
from docker_trigger import worker


def file_check(message):
    def _check(run):
        @functools.wraps(run)
        def wrapper(self):
            if not os.path.isfile(self._file):
                self.log.error('{} {} not exist'.format(message, self._file))
                return
            run(self)
        return wrapper
    return _check

class Base(object):
    def __init__(self):
        self.log = logging.getLogger(__file__)
        self.conf = None
        self.name = None

    def run_tasks(self, field):
        tasks = self.conf.get(field, None)
        if tasks:
            return worker.Tasks(self, tasks).walk()
        return None

    def run_module(self, field):
        module = self.conf.get(field, None)
        if module:
            return modules.run_module(self, module)

        return None

    def run(self):
        pass
