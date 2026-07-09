from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

import app.models  # noqa: F401
from config.config import ConflictError, NotFoundError, settings, templates
from routers.api import posts, users
from routers import web


def _is_api_request(request: Request) -> bool:
    return request.url.path.startswith("/api/")


def _error_page(request: Request, status_code: int, message: str) -> JSONResponse:
    return templates.TemplateResponse(
        request=request,
        name="errors/error.html",
        context={
            "status_code": status_code,
            "title": status_code,
            "message": message,
        },
        status_code=status_code,
    )


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name)

    app.mount(
        settings.static_url_prefix,
        StaticFiles(directory=str(settings.static_dir)),
        name="static",
    )
    app.mount(
        settings.storage_url_prefix,
        StaticFiles(directory=str(settings.storage_dir)),
        name="media",
    )

    app.include_router(web.router)
    app.include_router(users.router)
    app.include_router(posts.router)

    @app.exception_handler(NotFoundError)
    def not_found_handler(request: Request, exception: NotFoundError) -> JSONResponse:
        detail = f"{exception.resource} not found"
        if _is_api_request(request):
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"detail": detail},
            )
        return _error_page(request, status.HTTP_404_NOT_FOUND, detail)

    @app.exception_handler(ConflictError)
    def conflict_handler(request: Request, exception: ConflictError) -> JSONResponse:
        if _is_api_request(request):
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={"detail": exception.detail},
            )
        return _error_page(
            request, status.HTTP_422_UNPROCESSABLE_ENTITY, exception.detail
        )

    @app.exception_handler(StarletteHTTPException)
    def http_exception_handler(
        request: Request, exception: StarletteHTTPException
    ) -> JSONResponse:
        message = exception.detail or (
            "An unexpected error occurred. Please check the request and try again."
        )
        if _is_api_request(request):
            return JSONResponse(
                status_code=exception.status_code,
                content={"detail": message},
            )
        return _error_page(request, exception.status_code, message)

    @app.exception_handler(RequestValidationError)
    def validation_exception_handler(
        request: Request, exception: RequestValidationError
    ) -> JSONResponse:
        if _is_api_request(request):
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={"detail": exception.errors()},
            )
        message = ", ".join(error["msg"] for error in exception.errors())
        return _error_page(request, status.HTTP_422_UNPROCESSABLE_ENTITY, message)

    return app
