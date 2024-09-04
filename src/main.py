from typing import Union
from fastapi import FastAPI
from src.users.router import router as users_router
from src.notifications.router import router as notification_router
import os
import logging

script_dir = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(script_dir, 'app.log')

logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

app = FastAPI()
api_prefix = '/api/notifications'
app.include_router(users_router, prefix=api_prefix)
app.include_router(notification_router, prefix=api_prefix)
