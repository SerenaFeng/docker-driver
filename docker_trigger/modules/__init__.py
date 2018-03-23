from datetime import datetime
import importlib


def run_module(runner, module):
    parser = module.get('worker')
    if parser.count(':') != 1:
        return None
    cls = load_module(module.get('worker'))
    args = module.get('args')
    clz = cls(runner, **args) if args else cls(runner)
    return clz.work()


def load_module(module):
    (modulename, clsname) = tuple(filter(None, module.split(':')))
    return getattr(importlib.import_module(modulename), clsname)


def get_duration(start_date, stop_date):
    fmt = '%Y-%m-%d %H:%M:%S'
    try:
        datetime_start = datetime.strptime(start_date, fmt)
        datetime_stop = datetime.strptime(stop_date, fmt)
        delta = (datetime_stop - datetime_start).seconds
        res = "%sm%ss" % (delta / 60, delta % 60)
        return res
    except Exception as exc:
        raise Exception("get duration failed: {}".format(exc))
