# -*- coding: utf-8 -*-
'''
Support for phabricator configuration
'''


def managed(name, value, **kwargs):
    ret = {'name': name,
           'changes': {},
           'comment': '',
           'result': False}

    old_value = __salt__['phabricator_config.get_option'](name)

    if value != old_value:
        if not __opts__['test']:
            __salt__['phabricator_config.set_option'](name, value)
            ret['result'] = True
        else:
            ret['result'] = None

        ret['changes'] = {'new': value, 'old': old_value}
        ret['comment'] = 'New value was set for option %s' % (name,)
    else:
        ret['comment'] = 'The option %s has the right value' % (name,)
        if __opts__['test']:
            ret['result'] = None
        else:
            ret['result'] = True

    return ret


if __name__ == "__main__":
    __salt__ = ''
    __opts__ = ''

    import sys
    sys.exit(0)
