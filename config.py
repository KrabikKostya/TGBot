import dotenv

token = dotenv.get_variable(".env", "bot_token")
group_id = int(dotenv.get_variable(".env", "group_id"))
