import os
import dotenv


dotenv.load_dotenv()


OAUTH_TOKEN = os.getenv("OAUTH_TOKEN")
FOLDER_ID = os.getenv("FOLDER_ID")
