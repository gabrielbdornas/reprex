from imbox import Imbox
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

username = os.getenv("EMAIL_USER")
password = os.getenv("EMAIL_PWD")
host = os.getenv("EMAIL_IMAP")

with Imbox(hostname=host,
        username=username,
        password=password,
        ssl=True,
        ssl_context=None,
        starttls=False) as imbox:
    breakpoint()
