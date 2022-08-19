import dotenv

help(dotenv)
token = dotenv.dotenv_values(".env")["bot_token"]
