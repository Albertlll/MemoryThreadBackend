from fastapi import APIRouter

from api import base, veterans, events

api_router = APIRouter()

# Include the routers from the different modules
api_router.include_router(base.router)
api_router.include_router(veterans.router)
api_router.include_router(events.router)
