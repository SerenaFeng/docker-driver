from datetime import datetime
import logging

from pbr import version

LOG = logging.getLogger(__file__)


class Reporter(object):
    def __init__(self, runner):
        self.runner = runner

    def parse(self):
        report_data = self.generate_json()
        report_txt = ''
        report_txt += '\n\nDovetail Report\n'
        report_txt += 'Version: %s\n' % report_data['version']
        report_txt += 'TestSuite: %s\n' % report_data['testsuite']
        report_txt += 'Result Dashboard: %s\n' % report_data['dashboard']
        report_txt += 'Build Tag: %s\n' % report_data['build_tag']
        report_txt += 'Upload Date: %s\n' % report_data['upload_date']
        if report_data['duration'] == 0:
            report_txt += 'Duration: %s\n\n' % 'N/A'
        else:
            report_txt += 'Duration: %.2f s\n\n' % report_data['duration']

        total_num = 0
        pass_num = 0
        sub_report = {}
        testcase_num = {}
        testcase_passnum = {}
        tc_area = set((self.get_testcase_area(tc)
                       for tc in self.runner.content.get('testcases')))

        for area in tc_area:
            sub_report[area] = ''
            testcase_num[area] = 0
            testcase_passnum[area] = 0

        testarea_scope = []
        for testcase in report_data['testcases_list']:
            area = self.get_testcase_area(testcase.get('name'))
            testarea_scope.append(area)
            sub_report[area] += '-%-25s %s\n' %\
                (testcase['name'], testcase['result'])
            if 'sub_testcase' in testcase:
                for sub_test in testcase['sub_testcase']:
                    sub_report[area] += '\t%-110s %s\n' %\
                        (sub_test['name'], sub_test['result'])
            testcase_num[area] += 1
            total_num += 1
            if testcase['result'] == 'PASS':
                testcase_passnum[area] += 1
                pass_num += 1
            elif testcase['result'] == 'SKIP':
                testcase_num[area] -= 1
                total_num -= 1

        if total_num != 0:
            pass_rate = pass_num / total_num
            report_txt += 'Pass Rate: %.2f%% (%s/%s)\n' %\
                (pass_rate * 100, pass_num, total_num)
            report_txt += 'Assessed test areas:\n'
        else:
            report_txt += \
                'no testcase or all testcases are skipped in this testsuite'

        for key in sub_report:
            if testcase_num[key] != 0:
                pass_rate = testcase_passnum[key] / testcase_num[key]
                report_txt += '-%-25s pass %.2f%%\n' %\
                    (key + ' results:', pass_rate * 100)
            elif key in testarea_scope:
                report_txt += '-%-25s all skipped\n' % key
        for key in sub_report:
            if testcase_num[key] != 0:
                pass_rate = testcase_passnum[key] / testcase_num[key]
                report_txt += '%-25s  pass rate %.2f%%\n' %\
                    (key + ':', pass_rate * 100)
                report_txt += sub_report[key]
            elif key in testarea_scope:
                report_txt += '%-25s  all skipped\n' % key
                report_txt += sub_report[key]

        return report_txt

    def generate_json(self):
        report_obj = {}
        report_obj['version'] = \
            version.VersionInfo('dovetail').version_string()
        report_obj['testsuite'] = self.runner.name
        report_obj['dashboard'] = None
        report_obj['build_tag'] = self.runner.build_tag
        report_obj['upload_date'] =\
            datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        report_obj['duration'] = self.runner.end - self.runner.start

        report_obj['testcases_list'] = []
        for testcase_name in self.runner.testcases:
            testcase_runner = self.runner.get_testcase_runner(testcase_name)
            testcase_inreport = {}
            testcase_inreport['name'] = testcase_name
            if not testcase_runner:
                testcase_inreport['result'] = 'Undefined'
                testcase_inreport['objective'] = ''
                testcase_inreport['sub_testcase'] = []
                report_obj['testcases_list'].append(testcase_inreport)
                continue

            testcase_inreport['result'] = testcase_runner.result.get('criteria')
            testcase_inreport['objective'] = testcase_runner.content.get('objective')
            testcase_inreport['sub_testcase'] = []
            report_obj['testcases_list'].append(testcase_inreport)
        return report_obj

    def get_testcase_area(self, testcase):
        return testcase[: testcase.find('.')]

