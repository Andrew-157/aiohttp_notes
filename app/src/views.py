import aiohttp_jinja2
import aiohttp.web
from src.db import Note, Tag


@aiohttp_jinja2.template('index.html')
def index(request):
    notes = request.app['db_session'].query(Note).all()
    return {"notes": notes}


@aiohttp_jinja2.template('detail.html')
def detail(request):
    note_id = request.match_info.get('note_id')
    note = request.app['db_session'].query(
        Note).filter(Note.id == note_id).first()
    if not note:
        return aiohttp.web.HTTPFound(location=request.app.router['index'].url_for())
    return {"note": note}


@aiohttp_jinja2.template('note.html')
def note(request):
    tags = request.app['db_session'].query(Tag).all()
    return {"tags": tags}


@aiohttp_jinja2.template('tag.html')
def tag(request):
    return {}


async def create_tag(request):
    data = await request.post()
    tag = Tag(name=data["name"])
    request.app['db_session'].add(tag)
    request.app['db_session'].commit()
    return aiohttp.web.HTTPFound(location=request.app.router['index'].url_for())


async def create_note(request):
    data = await request.post()
    name = data["name"]
    description = data["description"]
    tags = data.getall("tags")
    tags_obj = []
    for tag in tags:
        tags_obj.append(request.app['db_session'].query(
            Tag).filter(Tag.name == tag).first())
    note = Note(name=name, description=description, tags=tags_obj)
    request.app['db_session'].add(note)
    request.app['db_session'].commit()
    return aiohttp.web.HTTPFound(location=request.app.router['index'].url_for())


async def delete_note(request):
    note_id = request.match_info.get('note_id')
    request.app['db_session'].query(Note).filter(Note.id == note_id).delete()
    request.app['db_session'].commit()
    return aiohttp.web.HTTPFound(location=request.app.router['index'].url_for())


async def done_note(request):
    note_id = request.match_info.get('note_id')
    request.app['db_session'].query(Note).filter(
        Note.id == note_id).first().done = True
    request.app['db_session'].commit()
    return aiohttp.web.HTTPFound(location=request.app.router['index'].url_for())
