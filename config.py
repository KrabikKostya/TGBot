import os


is_heroku = os.environ.get('IS_HEROKU', None)
if is_heroku:
    bot_owner = int(os.environ.get('bot_owner', None))
    bot_token = os.environ.get('bot_token', None)
