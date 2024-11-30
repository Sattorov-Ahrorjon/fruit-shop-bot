from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")

GROUP_ID = env.str("GROUP_ID")
BACKEND_URL = env.str("BACKEND_URL")
