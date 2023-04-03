from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_jwt_auth import AuthJWT
from tortoise.contrib.fastapi import register_tortoise

from api.routes import auth, users, router
from api.utils.database import db_url, init_db
import uvicorn
from config import settings


def create_application() -> FastAPI:
    application = FastAPI(title=settings.PROJECT_NAME, debug=settings.DEBUG, openapi_url=f"/{settings.API_V1_PREFIX}/openapi.json")

    # Initialize database
    application.add_event_handler("startup", init_db)

    # Register routes
    application.include_router(router)

    # Add CORS middleware
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


    return application


app = create_application()

# Configure Tortoise ORM
register_tortoise(
    app,
    db_url=db_url(),
    modules={"models": ["app.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)