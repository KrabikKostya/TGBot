from dotenv import get_variables


token = get_variables(".env")["bot_token"]
group_id = int(get_variables(".env")["group_id"])
