from aiohttp import web
from src.routes import setup_routes
from src.settings import config


app = web.Application()
setup_routes(app)
app['config'] = config
web.run_app(app)
