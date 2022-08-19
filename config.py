import dotenv

help(dotenv)
token = dotenv.get_variable(".env", "bot_token")
