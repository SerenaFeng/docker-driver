import importlib
import os


class BaseWorker(object):
    def __init__(self, runner, task):
        self.runner = runner
        self.task_type = task.keys()[0]
        self.task = task.get(self.task_type)

    def execute(self):
        raise NotImplementedError(
            'Not Implemented executor {}'.format(self.task_type))


class PythonWorker(BaseWorker):
    def execute(self):
        module = self.task.get('worker')
        args = self.task.get('args')
        if module.count(':') != 1:
            return None
        cls = self.load_module(module)
        clz = cls(self.runner, **args) if args else cls(self.runner)
        return clz.work()

    @staticmethod
    def load_module(module):
        (modulename, clsname) = tuple(filter(None, module.split(':')))
        return getattr(importlib.import_module(modulename), clsname)

class ShellWorker(BaseWorker):
    def execute(self):
        os.system(self.task)

class Tasks(object):
    def __init__(self, runner, tasks):
        self.runner = runner
        self.tasks = tasks

    def walk(self):
        print 'began to run tasks: {}'.format(self.tasks)

        if isinstance(self.tasks, list):
            return [self.get_worker(task)(self.runner, task).execute()
                    for task in self.tasks]
        else:
            return self.get_worker(self.tasks)(self.runner, self.tasks).execute()

    def get_worker(self, task):
        task_type = task.keys()[0]
        cls = '{}Worker'.format(task_type.capitalize())
        if cls in globals():
            return globals()[cls]
        else:
            return globals()['BaseWorker']
