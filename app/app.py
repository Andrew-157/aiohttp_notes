from aiohttp import web
from src.views import setup_routes


app = web.Application()
web.run_app(app)
