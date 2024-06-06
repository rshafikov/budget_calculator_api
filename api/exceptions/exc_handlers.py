from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


def add_exc_handlers(app: FastAPI) -> None:
    @app.exception_handler(OSError)
    async def oserror_handler(request: Request, exc: OSError):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={'error': 'Database not available.'}
        )
