import os.path
from datetime import datetime

import logging
import json
from docker_trigger import constants


class Publish(object):
    def __init__(self):
        self.file = os.path.join(constants.RESULTS_PATH, 'result.json')
        self.logger = logging.getLogger(__file__)

    def parse(self):
        with open(self.file, 'r') as f:
            try:
                data = json.loads(f.read())
            except Exception as exc:
                self.logger.error('load result failed: {}'.format(exc))
                return None

            try:
                criteria = data['criteria']
                timestart = data['start_date']
                timestop = data['stop_date']
                details = data['details']
                duration = self.get_duration(timestart, timestop)
            except KeyError as e:
                self.logger.error("Result data don't have key {}.".format(e))
                return None
            except Exception as exc:
                self.logger.error("parse result failed: {}.".format(exc))
                return None

            return {
                'criteria': criteria,
                'timestart': timestart,
                'timestop': timestop,
                'duration': duration,
                'details': details
            }

    def get_duration(self, start_date, stop_date):
        fmt = '%Y-%m-%d %H:%M:%S'
        try:
            datetime_start = datetime.strptime(start_date, fmt)
            datetime_stop = datetime.strptime(stop_date, fmt)
            delta = (datetime_stop - datetime_start).seconds
            res = "%sm%ss" % (delta / 60, delta % 60)
            return res
        except ValueError as e:
            self.logger.exception("ValueError: {}".format(e))
            return None
