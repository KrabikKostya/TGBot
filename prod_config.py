import os


is_heroku = os.environ.get('IS_HEROKU', None)
if is_heroku:
    import config

    config.bot_owner = int(os.environ.get('bot_owner', None))
    config.bot_token = os.environ.get('bot_token', None)
