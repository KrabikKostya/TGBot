from dotenv import get_variables

get_variables(".env")
token = get_variables(".env")["bot_token"]
group_id = int(get_variables(".env")["group_id"])
