import pyinstrument
from starlette.middleware.base import BaseHTTPMiddleware


class ProfilerMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, **kwargs):
        super().__init__(app)
        self.profiler_kwargs = kwargs

    async def dispatch(self, request, call_next):
        with pyinstrument.Profiler(**self.profiler_kwargs) as p:
            response = await call_next(request)
        p.print()
        return response
