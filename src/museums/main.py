#import logging
from fastapi import FastAPI
#from sqladmin import Admin, ModelView
#from museums.engines.sqldb import engine
#from museums.models.museum_tables import Category, Location, Museum
from museums.admin.admin_base import setup_admin

# from app.routers import users, items
# from app.db.database import engine, Base

# Get Uvicorn's error logger and set level to DEBUG
#logger = logging.getLogger("uvicorn.error")
#logger.setLevel(logging.WARNING)

# Create database tables
# Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="My FastAPI App",
    description="A sample FastAPI application with well-organized structure",
    version="0.1.0",
    #debug=True
)
#admin = Admin(app, engine)

setup_admin(app)

#class CategoryAdmin(ModelView, model=Category):
    #column_list = [Category.id, Category.category]

#class LocationAdmin(ModelView, model=Location):
    #column_list = [Location.id, Location.location]

#class MuseumAdmin(ModelView, model=Museum):
    #column_list = [
        #Museum.id,
        #Museum.entity,
        #Museum.title,
        #Museum.address,
        #Museum.category_id,
        #Museum.location_id,
        #Museum.inn,
        #Museum.affiliation,
        #Museum.submission,
        #Museum.timezone,
        #Museum.teg,
        #Museum.description,
        #Museum.website,
        #Museum.email,
        #Museum.eipsk,
        #Museum.service_name,
        #Museum.updated_at,
    #]

#admin.add_view(CategoryAdmin)
#admin.add_view(LocationAdmin)
#admin.add_view(MuseumAdmin)

# Include routers
# app.include_router(users.router)
# app.include_router(items.router)

@app.get("/")
async def root():
    return {"message": "Welcome to my FastAPI application!"}

'''
from fastapi import FastAPI

from . import config
from .resources import lifespan
from .routers import hello

app = FastAPI(
    title='Hello World',
    lifespan=lifespan,
)
routers = (
    hello.router,
)
for router in routers:
    app.include_router(router)
'''
