import os


def prod_configurator():
    import config

    config.bot_owner = int(os.environ.get('bot_owner', None))
    config.bot_token = os.environ.get('bot_token', None)
