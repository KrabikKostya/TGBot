import os


config.bot_owner = int(os.environ.get('bot_owner', None))
config.bot_token = os.environ.get('bot_token', None)
