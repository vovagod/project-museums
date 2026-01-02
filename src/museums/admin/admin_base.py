from typing import Optional
from fastapi import FastAPI  
from starlette_admin.contrib.sqla import Admin as BaseAdmin
from starlette.requests import Request

from museums.engines.sqldb import engine  
from museums.admin.views.exposition_view import ExpositionView
from museums.admin.views.museum_view import CategoryView, LocationView, MuseumView
from museums.models.exposition_tables import Exposition
from museums.models.museum_tables import Category, Location, Museum


class Admin(BaseAdmin):
    #pass
    def custom_render_js(self, request: Request) -> Optional[str]:
        print(f"We are in custom_render_js...") # development
        return request.url_for("admin:statics", path="js/new_render.js")

def setup_admin(app: FastAPI) -> None:  
    admin = Admin(
        engine=engine,
        title="Museums Admin", 
        debug=True, 
        statics_dir = "admin/statics"
    )   

    #admin.add_view(UserView(User))  
    admin.add_view(CategoryView(Category)) 
    admin.add_view(LocationView(Location))
    admin.add_view(MuseumView(Museum)) 
    admin.add_view(ExpositionView(Exposition))  

    admin.mount_to(app=app)