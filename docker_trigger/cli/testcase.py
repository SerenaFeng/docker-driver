import os

from docker_trigger import cli
from docker_trigger import constants
from docker_trigger import parser
from docker_trigger import trigger


def get_testcase_path(name):
    return os.path.join(constants.TESTDEF_PATH, '{}.yaml'.format(name))


class TestCaseList(cli.Command):
    def get_parser(self, prog_name):
        parser = super(TestCaseList, self).get_parser(prog_name)
        parser.add_argument('-family',
                            default = '',
                            help='Search test case using name')
        return parser

    def take_action(self, parsed_args):
        family = parsed_args.family
        for _, _, files in os.walk(constants.TESTDEF_PATH):
            for file in files:
                if not family or file.startswith(family):
                    print file


class TestCaseShow(cli.Command):
    def get_parser(self, prog_name):
        parser = super(TestCaseShow, self).get_parser(prog_name)
        parser.add_argument('testcase',
                            metavar='<testcase>',
                            help='Search test case using name')
        return parser

    def take_action(self, parsed_args):
        testcase = parsed_args.testcase
        testcase_file = get_testcase_path(testcase)
        if os.path.isfile(testcase_file):
            with open(testcase_file, 'r') as tc_file:
                try:
                    print tc_file.read()
                except Exception as exc:
                    print exc
        else:
            self.log.error('testcase {} not supported'.format(testcase))


class TestCaseRun(cli.Command):
    def get_parser(self, prog_name):
        parser = super(TestCaseRun, self).get_parser(prog_name)
        parser.add_argument('name',
                            metavar='<name>',
                            help='Search test case using name')
        return parser

    def take_action(self, parsed_args):
        name = parsed_args.name
        _path = get_testcase_path(name)
        if os.path.isfile(_path):
            print 'run testcase {}'.format(_path)
            testcase = parser.YamlParser(_path).get_testcase()
            # print testcase
            trigger.Trigger(testcase).run()
        else:
            print 'testcase {} not supported'.format(_path)
