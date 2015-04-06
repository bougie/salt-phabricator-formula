# -*- coding: utf-8 -*-
'''
Support for phabricator configuration
'''
from __future__ import absolute_import

import logging
log = logging.getLogger(__name__)


def managed(name, value, **kwargs):
    ret = {'name': name,
           'changes': {},
           'comment': '',
           'result': False}

    try:
        old_value = __salt__['phabricator_config.get_option'](name, **kwargs)
    except:
        if __opts__['test']:
            ret['result'] = None
            ret['comment'] = 'option %s seems do not exist' % (name,)
        else:
            ret['result'] = False
            ret['comment'] = 'option %s does not exist' % (name,)
    else:
        if value != old_value:
            ret['changes'] = {'new': value, 'old': old_value}

            if not __opts__['test']:
                try:
                    __salt__['phabricator_config.set_option'](name,
                                                              value,
                                                              **kwargs)
                except:
                    ret['result'] = False
                else:
                    ret['result'] = True
            else:
                ret['result'] = None
        else:
            if __opts__['test']:
                ret['result'] = None
            else:
                ret['result'] = True

    return ret


def absent(name, **kwargs):
    ret = {'name': name,
           'changes': {},
           'comment': '',
           'result': False}

    try:
        curr_value = __salt__['phabricator_config.get_option'](name, **kwargs)
    except:
        if __opts__['test']:
            ret['result'] = None
            ret['comment'] = 'option %s seems do not exist' % (name,)
        else:
            ret['result'] = False
            ret['comment'] = 'option %s does not exist' % (name,)
    else:
        if not __opts__['test']:
            if curr_value is not None:
                try:
                    __salt__['phabricator_config.delete_option'](name, **kwargs)
                except:
                    ret['result'] = False
                else:
                    ret['result'] = True
                    ret['changes'] = {'old': curr_value, 'new': None}
            else:
                ret['result'] = True
        else:
            ret['result'] = None

    return ret


if __name__ == "__main__":
    __salt__ = ''
    __opts__ = ''

    import sys
    sys.exit(0)
