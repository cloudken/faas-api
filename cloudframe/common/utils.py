
import logging
import os
import sys
import uuid

from oslo_concurrency import processutils

LOG = logging.getLogger(__name__)


def generate_uuid():
    """Creates a random uuid string.

    :returns: string
    """
    return str(uuid.uuid4())


def import_module(import_str):
    """Import a module.

    .. versionadded:: 0.3
    """
    __import__(import_str)
    return sys.modules[import_str]


def try_import(import_str, default=None):
    """Try to import a module and if it fails return default."""
    try:
        return import_module(import_str)
    except ImportError:
        return default


def get_resource(resource_name, version):
    res = 'restframe.api.resources.' + version + '.' + resource_name
    return import_module(res)


def _get_root_helper():
    return 'sudo cloudframe-rootwrap %s'


def execute(*cmd, **kwargs):
    """Convenience wrapper around oslo's execute() method.

    :param cmd: Passed to processutils.execute.
    :param use_standard_locale: True | False. Defaults to False. If set to
                                True, execute command with standard locale
                                added to environment variables.
    :returns: (stdout, stderr) from process execution
    :raises: UnknownArgumentError
    :raises: ProcessExecutionError
    """

    use_standard_locale = kwargs.pop('use_standard_locale', False)
    if use_standard_locale:
        env = kwargs.pop('env_variables', os.environ.copy())
        env['LC_ALL'] = 'C'
        kwargs['env_variables'] = env
    if kwargs.get('run_as_root') and 'root_helper' not in kwargs:
        kwargs['root_helper'] = _get_root_helper()
    result = processutils.execute(*cmd, **kwargs)
    LOG.debug('Execution completed, command line is "%s"',
              ' '.join(map(str, cmd)))
    LOG.debug('Command stdout is: "%s"' % result[0])
    LOG.debug('Command stderr is: "%s"' % result[1])
    return result
