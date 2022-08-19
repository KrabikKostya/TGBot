import dotenv

token = dotenv.get_variables(".env")["bot_token"]
group_id = int(dotenv.get_variables(".env")["group_id"])
