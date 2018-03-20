import os

import yaml

from docker_trigger import cli
from docker_trigger import constants
from docker_trigger import parser
from docker_trigger import trigger
from docker_trigger import testsuite as ts

class TestSuiteList(cli.Lister):
    def take_action(self, parsed_args):
        suites = []
        for root, _, files in os.walk(constants.TESTSUITE_PATH):
            for file in files:
                with open(os.path.join(root, file), 'r') as fd:
                    content = yaml.safe_load(fd)
                    if content.has_key('testsuite'):
                        suites.append(content.get('testsuite'))
        columns = ['name', 'objective']
        return self.format_output(columns, suites)


class TestSuiteShow(cli.Show):
    def get_parser(self, prog_name):
        parser = super(TestSuiteShow, self).get_parser(prog_name)
        parser.add_argument('name',
                            metavar='<name>',
                            help='Show test suite by name')
        return parser

    def take_action(self, parsed_args):
        testsuite = parsed_args.name
        self.get_file = ts.get_file
        self.read_file(testsuite)


class TestSuiteRun(cli.Command):
    def get_parser(self, prog_name):
        parser = super(TestSuiteRun, self).get_parser(prog_name)
        parser.add_argument('name',
                            metavar='<name>',
                            help='Run test suite by name')
        parser.add_argument('-p', '--publish',
                            action='store_true',
                            default=False,
                            help='whether to publish the results or not')
        parser.add_argument('-sut', '--sut',
                            action='store_true',
                            default=False,
                            help='whether to publish the results or not')
        return parser

    def take_action(self, parsed_args):
        if parsed_args.sut:
            print 'get sut information'

        ts.TestSuite(parsed_args.name, parsed_args.publish).run()
