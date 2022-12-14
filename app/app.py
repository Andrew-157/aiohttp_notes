from aiohttp import web
from src.routes import setup_routes
from src.settings import config
from src.db import pg_context


app = web.Application()
setup_routes(app)
app['config'] = config
app.cleanup_ctx(pg_context)
web.run_app(app)
