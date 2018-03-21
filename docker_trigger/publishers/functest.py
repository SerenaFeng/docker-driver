import json
import logging
import os.path

from docker_trigger import constants
from docker_trigger import publishers

LOG = logging.getLogger(__file__)


class Simple(object):
    def __init__(self, runner, result_file=None):
        self.runner = runner
        self.result_file = result_file
            #if file else os.path.join(constants.RESULTS_PATH, 'result.json')

    def parse(self):
        with open(self.result_file, 'r') as f:
            try:
                data = json.loads(f.read())
            except Exception as exc:
                LOG.error('load result failed: {}'.format(exc))
                return None
            try:
                start = data['start_date']
                stop = data['stop_date']
                return {
                    'criteria': data['criteria'],
                    'timestart': start,
                    'timestop': stop,
                    'duration': publishers.get_duration(start, stop),
                    'details': data['details']
                }
            except Exception as exc:
                LOG.error("parse result failed: {}.".format(exc))
                return None
