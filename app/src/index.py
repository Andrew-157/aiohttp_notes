from aiohttp import web
from src.views import index


def setup_routes(app: web.Application):
    app.router.add_get('/', index)
