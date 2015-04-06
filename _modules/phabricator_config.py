# -*- coding: utf-8 -*-
'''
Support for phabricator configuration
'''
from __future__ import absolute_import

# Import python libs
import os

import logging
# Import salt libs
import salt.utils
from salt.exceptions import CommandExecutionError, SaltInvocationError

log = logging.getLogger(__name__)

__virtualname__ = 'phabricator_config'
available_options = None


def __virtual__():
    '''
    Module load only if php is installed
    '''
    if salt.utils.which('php'):
        return __virtualname__
    else:
        return False


def _bin_dir():
    '''
    Return the path to the root dir of phabricator install dir
    '''
    return __salt__['config.get']('phabricator:root_dir')


def _phab_config_exec(command, bin=None):
    '''
    Return the path to the config binary
    '''
    if bin is not None:
        if os.path.isfile(bin):
            phab_bin = bin
        else:
            phab_bin = os.path.join(bin, 'phabricator', 'bin', 'config')
    else:
        phab_bin = os.path.join(_bin_dir(), 'phabricator', 'bin', 'config')

    return '%s %s' % (phab_bin, command)


def _option_exists(name, **kwargs):
    '''
    Check if a given option name is in the all options list
    '''
    return name in list_options(**kwargs).split('\n')


def list_options(**kwargs):
    '''
    List all configuration options

    CLI Example:

    .. code-block:: bash

        salt '*' phabricator_config.list_options
        salt '*' phabricator_config.list_options bin=/path/to/config/bin
        salt '*' phabricator_config.list_options bin=/path/to/root/dir
    '''
    global available_options

    if available_options is None or kwargs.get('force', False):
        phab_cmd = _phab_config_exec('list', bin=kwargs.get('bin', None))

        cmd_ret = __salt__['cmd.run_all'](phab_cmd)
        if cmd_ret['retcode'] == 0:
            available_options = cmd_ret['stdout']
        else:
            raise CommandExecutionError('Error in command "%s" : %s' % (
                phab_cmd,
                str(cmd_ret)))

    return available_options


def get_option(name, **kwargs):
    '''
    Get value for a given option name

    CLI Example:

    .. code-block:: bash

        salt '*' phabricator_config.get_option <option_name>
        salt '*' phabricator_config.get_option <option_name>
        bin=/path/to/config/bin
        salt '*' phabricator_config.get_option <option_name>
        bin=/path/to/root/dir
    '''
    phab_cmd = _phab_config_exec('get', bin=kwargs.get('bin', None))

    if name is not None and len(name.strip()) > 0:
        phab_cmd = '%s %s' % (phab_cmd, name)

    if _option_exists(name, **kwargs):
        # config get <option_name> returns json if it success
        cmd_ret = __salt__['cmd.run_all'](phab_cmd)
        option_values = {}
        if cmd_ret['retcode'] == 0:
            try:
                option_values = salt.utils.serializers.json.deserialize(
                    cmd_ret['stdout'])
            except:
                raise CommandExecutionError(
                    'Error while parsing JSON : %s' % (cmd_ret['stdout'],))
        else:
            raise CommandExecutionError('Error in command "%s" : %s' % (
                phab_cmd,
                str(cmd_ret)))
    else:
        raise SaltInvocationError('Option %s does not exist' % (name,))

    option_value = None
    if isinstance(option_values, dict) and 'config' in option_values:
        # option_values['config'] contains a local and a database option
        # local option value has priority over database one
        for scope in ['local', 'database']:
            if option_value is None:
                for t_option in option_values['config']:
                    if (t_option['source'] == scope
                            and t_option['key'] == name
                            and t_option['status'] == 'set'):
                        option_value = t_option['value']
                        break
            else:
                break

    return option_value


def set_option(name, value, **kwargs):
    '''
    Set value for a given option name

    CLI Example:

    .. code-block:: bash

        salt '*' phabricator_config.set_option <option_name> <option_value>
        salt '*' phabricator_config.set_option <option_name> <option_value>
        bin=/path/to/config/bin
        salt '*' phabricator_config.get_option <option_name> <option_value>
        bin=/path/to/root/dir
    '''
    phab_cmd = _phab_config_exec('set', bin=kwargs.get('bin', None))

    if name is not None and len(name.strip()) > 0:
        phab_cmd = '%s %s "%s"' % (phab_cmd, name, value)

    if _option_exists(name, **kwargs):
        cmd_ret = __salt__['cmd.run_all'](phab_cmd)
        if cmd_ret['retcode'] == 0:
            return cmd_ret['stdout']
        else:
            raise CommandExecutionError('Error in command "%s" : %s' % (
                phab_cmd,
                str(cmd_ret)))
    else:
        raise SaltInvocationError('Option %s does not exist' % (name,))


def delete_option(name, **kwargs):
    '''
    Delete/Reset value for a given option name

    CLI Example:

    .. code-block:: bash

        salt '*' phabricator_config.delete_option <option_name>
        salt '*' phabricator_config.delete_option <option_name>
        bin=/path/to/config/bin
        salt '*' phabricator_config.delete_option <option_name>
        bin=/path/to/root/dir
    '''
    if (_option_exists(name, **kwargs)
            and get_option(name, **kwargs) is not None):
        phab_cmd = _phab_config_exec('delete', bin=kwargs.get('bin', None))

        if name is not None and len(name.strip()) > 0:
            phab_cmd = '%s %s' % (phab_cmd, name)

        cmd_ret = __salt__['cmd.run_all'](phab_cmd)
        if cmd_ret['retcode'] == 0:
            return cmd_ret['stdout']
        else:
            raise CommandExecutionError('Error in command "%s" : %s' % (
                phab_cmd,
                str(cmd_ret)))
    else:
        return 'option %s is not set' % (name,)


if __name__ == "__main__":
    __salt__ = ''

    import sys
    sys.exit(0)
