import os

import yaml

from docker_trigger import cli
from docker_trigger import constants
from docker_trigger import testcase as tc
from docker_trigger import parser


class TestCaseList(cli.Lister):
    def take_action(self, parsed_args):
        cases = []
        for root, _, files in os.walk(constants.TESTDEF_PATH):
            for file in files:
                with open(os.path.join(root, file), 'r') as fd:
                    content = yaml.safe_load(fd)
                    try:
                        if content.has_key('testcase'):
                            cases.append(content.get('testcase'))
                    except:
                        pass
        columns = ['name', 'objective']
        return self.format_output(columns, cases)


class TestCaseShow(cli.Show):
    def get_parser(self, prog_name):
        parser = super(TestCaseShow, self).get_parser(prog_name)
        parser.add_argument('testcase',
                            metavar='<testcase>',
                            help='Search test case using name')
        return parser

    def take_action(self, parsed_args):
        testcase = parsed_args.testcase
        self.get_file = tc.get_file
        self.read_file(testcase)
        # yaml_parser = parser.YamlParser(constants.TESTDEF_PATH)
        # yaml_parser.load_files(tc.get_file(testcase))
        # print yaml_parser.data


class TestCaseRun(cli.Command):
    def get_parser(self, prog_name):
        parser = super(TestCaseRun, self).get_parser(prog_name)
        parser.add_argument('name',
                            metavar='<name>',
                            help='Search test case using name')
        return parser

    def take_action(self, parsed_args):
        name = parsed_args.name
        self.log.info('begin to run testcase {}'.format(name))
        tc.TestCase(name).run()
