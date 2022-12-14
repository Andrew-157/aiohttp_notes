from aiohttp import web
from app.src.routes import index


def setup_routes(app: web.Application):
    app.router.add_get('/', index)
