from utils import plugins

PLUGIN_NAME = 'Library of Congress Plugin'
DISPLAY_NAME = 'Library of Congress'
DESCRIPTION = 'Libray of Congress Deposit Plugin'
AUTHOR = 'Andy Byers'
VERSION = '0.1'
SHORT_NAME = 'loc_deposit'
MANAGER_URL = 'loc_deposit_manager'
JANEWAY_VERSION = "1.4.2"


class LOCDepositPlugin(plugins.Plugin):
    plugin_name = PLUGIN_NAME
    display_name = DISPLAY_NAME
    description = DESCRIPTION
    author = AUTHOR
    short_name = SHORT_NAME
    manager_url = MANAGER_URL

    version = VERSION
    janeway_version = JANEWAY_VERSION


def install():
    LOCDepositPlugin.install()


def hook_registry():
    LOCDepositPlugin.hook_registry()


def register_for_events():
    pass
