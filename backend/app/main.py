from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config.services import services
from app.api import router
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
    ]
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await services.start()
    yield
    # Shutdown
    await services.stop()

app = FastAPI(lifespan=lifespan)
app.include_router(router)
