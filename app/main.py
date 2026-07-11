from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.responses import JSONResponse, Response

import app.models  # noqa: F401
from config.config import ConflictError, NotFoundError, settings, templates
from config.database import engine, Base
from routers.api import posts, users
from routers import web
from contextlib import asynccontextmanager
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler
)


def _is_api_request(request: Request) -> bool:
    return request.url.path.startswith('/api/')


def _error_page(request: Request, status_code: int, message: str) -> JSONResponse:
    return templates.TemplateResponse(
        request=request,
        name='errors/error.html',
        context={
            'status_code': status_code,
            'title': status_code,
            'message': message,
        },
        status_code=status_code,
    )


# The @asynccontextmanager decorator is used here to define an asynchronous context manager,
# which allows for setup and teardown actions to occur during the application's lifespan.
# The `lifespan` function manages the startup and shutdown lifecycle events for a FastAPI application.
#
# On startup, it establishes an asynchronous connection to the database engine and runs the
# synchronous method to create all tables defined in the SQLAlchemy Base metadata.
#
# The `yield` statement marks the point where control is transferred to the application,
# allowing the app to run while the context manager stays active.
#
# On shutdown (after the app stops), it asynchronously disposes of the database engine,
# properly cleaning up any resources held by the connection pool.
@asynccontextmanager
async def lifespan(_app: FastAPI):
    """ Lifespan context manager for the FastAPI application.
    Handles the startup and shutdown lifecycle of the application.
    On startup, creates the database tables.
    On shutdown, disposes of the database engine.
    """

    # Startup: create database tables before the app starts serving requests
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown: dispose the database engine and release resources
    await engine.dispose()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        lifespan=lifespan
    )

    app.mount(
        settings.static_url_prefix,
        StaticFiles(directory=str(settings.static_dir)),
        name='static',
    )
    app.mount(
        settings.storage_url_prefix,
        StaticFiles(directory=str(settings.storage_dir)),
        name='media',
    )

    app.include_router(web.router)
    app.include_router(users.router)
    app.include_router(posts.router)

    @app.exception_handler(NotFoundError)
    def not_found_handler(request: Request, exception: NotFoundError) -> JSONResponse:
        detail = f'{exception.resource} not found'
        if _is_api_request(request):
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={'detail': detail},
            )
        return _error_page(request, status.HTTP_404_NOT_FOUND, detail)

    @app.exception_handler(ConflictError)
    def conflict_handler(request: Request, exception: ConflictError) -> JSONResponse:
        if _is_api_request(request):
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={'detail': exception.detail},
            )
        return _error_page(
            request, status.HTTP_422_UNPROCESSABLE_ENTITY, exception.detail
        )

    @app.exception_handler(StarletteHTTPException)
    async def general_http_exception_handler(
            request: Request,
            exception: StarletteHTTPException
    ) -> Response | JSONResponse:
        if _is_api_request(request):
            return await http_exception_handler(
                request=request,
                exc=exception
            )

        message = exception.detail or (
            'An unexpected error occurred. Please check the request and try again.'
        )

        return _error_page(request, exception.status_code, message)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
            request: Request, exception: RequestValidationError
    ) -> JSONResponse:
        if _is_api_request(request):
            return await request_validation_exception_handler(
                request=request,
                exc=exception
            )

        message = ', '.join(error['msg'] for error in exception.errors())
        
        return _error_page(request, status.HTTP_422_UNPROCESSABLE_ENTITY, message)

    return app
