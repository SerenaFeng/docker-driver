import os

from cliff import command

from docker_driver.common import constants

def get_testcase_path(name):
    return os.path.join(
        constants.TESTCASE_PATH,
        "%s.yml" % (name[9:] if name.startswith('dovetail.') else name))


class TestCaseShow(command.Command):
    def get_parser(self, prog_name):
        parser = super(TestCaseShow, self).get_parser(prog_name)
        parser.add_argument('testcase',
                            metavar='<testcase>',
                            help='Search test case using name')
        return parser

    def take_action(self, parsed_args):
        testcase = parsed_args.testcase
        testcase_path = get_testcase_path(testcase)
        if os.path.isfile(testcase_path):
            with open(testcase_path, 'r') as tc_file:
                try:
                    print tc_file.read()
                except Exception as exc:
                    print exc
        else:
            print 'testcase {} not supported'.format(testcase)


class RunTestCase(command.Command):
    def get_parser(self, prog_name):
        parser = super(RunTestCase, self).get_parser(prog_name)
        parser.add_argument('testcase',
                            metavar='<testcase>',
                            help='Search test case using name')
        return parser

    def take_action(self, parsed_args):
        testcase = parsed_args.testcase
        testcase_path = get_testcase_path(testcase)
        if os.path.isfile(testcase_path):
            print 'run testcase {}'.format(testcase)
        else:
            print 'testcase {} not supported'.format(testcase)
