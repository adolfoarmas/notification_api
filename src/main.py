from typing import Union
from fastapi import FastAPI
from seeds.seed_categories import seed_categories
from seeds.seed_channels import seed_channels
from seeds.seed_users import seed_users
from src.users.router import router as users_router
from src.notifications.router import router as notification_router
from src.categories.router import router as categories_router
from src.channels.router import router as channels_router
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

logger.info("Starting service...")

app = FastAPI()
api_prefix = '/api/notifications'
app.include_router(users_router, prefix=api_prefix)
app.include_router(categories_router, prefix=api_prefix)
app.include_router(channels_router, prefix=api_prefix)
app.include_router(notification_router, prefix=api_prefix)



@app.on_event("startup")
async def on_startup():
    seed = os.getenv("SEED", False)
    if bool(seed):
        seed_categories()
        seed_channels()
        seed_users()
        logger.info("App seeded, remember comment line with '- SEED=True' in docker-compose.yml file")
