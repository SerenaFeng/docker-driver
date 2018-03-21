'''
put all the publisers under this repo
'''
from datetime import datetime
import importlib


def publish(runner, publisher):
    parser = publisher.get('parser')
    if parser.count(':') != 1:
        return None
    cls = load_publisher(publisher.get('parser'))
    args = publisher.get('args')
    clz = cls(runner, **args) if args else cls(runner)
    return clz.parse()


def load_publisher(parser):
    (modulename, clsname) = tuple(filter(None, parser.split(':')))
    module = importlib.import_module(modulename)
    return getattr(module, clsname)


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
