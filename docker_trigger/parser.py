import codecs
import io
import locale
import logging
import os

import yaml

from docker_trigger import local_yaml

logger = logging.getLogger(__file__)

__all__ = ['YamlParser']


class JenkinsJobsException(Exception):
    pass


class YamlParser(object):
    def __init__(self, path):
        self.data = {}
        self.testcases = []
        self.path = path
        # self.load_files()

    # def load_files(self):
    #     with open(self.path, 'r') as fd:
    #         self.data = yaml.safe_load(fd)

    def load_files(self, fn):

        # handle deprecated behavior, and check that it's not a file like
        # object as these may implement the '__iter__' attribute.
        if not hasattr(fn, '__iter__') or hasattr(fn, 'read'):
            logger.warning(
                'Passing single elements for the `fn` argument in '
                'Builder.load_files is deprecated. Please update your code '
                'to use a list as support for automatic conversion will be '
                'removed in a future version.')
            fn = [fn]

        files_to_process = []
        for path in fn:
            if not hasattr(path, 'read') and os.path.isdir(path):
                files_to_process.extend([os.path.join(path, f)
                                         for f in os.listdir(path)
                                         if (f.endswith('.yml')
                                             or f.endswith('.yaml'))])
            else:
                files_to_process.append(path)

        # symlinks used to allow loading of sub-dirs can result in duplicate
        # definitions of macros and templates when loading all from top-level
        unique_files = []
        for f in files_to_process:
            if hasattr(f, 'read'):
                unique_files.append(f)
                continue
            rpf = os.path.realpath(f)
            if rpf not in unique_files:
                unique_files.append(rpf)
            else:
                logger.warning("File '%s' already added as '%s', ignoring "
                               "reference to avoid duplicating yaml "
                               "definitions." % (f, rpf))

        for in_file in unique_files:
            # use of ask-for-permissions instead of ask-for-forgiveness
            # performs better when low use cases.
            if hasattr(in_file, 'name'):
                fname = in_file.name
            else:
                fname = in_file
            logger.debug("Parsing YAML file {0}".format(fname))
            if hasattr(in_file, 'read'):
                self._parse_fp(in_file)
            else:
                self.parse(in_file)

    def _parse_fp(self, fp):
        # wrap provided file streams to ensure correct encoding used
        data = local_yaml.load(self.wrap_stream(fp), search_path=self.path)
        if data:
            if not isinstance(data, list):
                raise JenkinsJobsException(
                    "The topmost collection in file '{fname}' must be a list,"
                    " not a {cls}".format(fname=getattr(fp, 'name', fp),
                                          cls=type(data)))
            for item in data:
                cls, dfn = next(iter(item.items()))
                group = self.data.get(cls, {})
                if len(item.items()) > 1:
                    n = None
                    for k, v in item.items():
                        if k == "name":
                            n = v
                            break
                    # Syntax error
                    raise JenkinsJobsException("Syntax error, for item "
                                               "named '{0}'. Missing indent?"
                                               .format(n))
                # allow any entry to specify an id that can also be used
                _id = dfn.get('id', dfn['name'])
                group[_id] = dfn
                self.data[cls] = group

    def parse(self, fn):
        with io.open(fn, 'r', encoding='utf-8') as fp:
            self._parse_fp(fp)

    @staticmethod
    def wrap_stream(stream, encoding='utf-8'):

        try:
            stream_enc = stream.encoding
        except AttributeError:
            stream_enc = locale.getpreferredencoding()

        if hasattr(stream, 'buffer'):
            stream = stream.buffer

        if str(stream_enc).lower() == str(encoding).lower():
            return stream

        return codecs.EncodedFile(stream, encoding, stream_enc)
