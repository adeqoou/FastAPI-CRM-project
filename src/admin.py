from sqladmin import Admin, ModelView
from src.auth.models import User
from src.crm.models import *
from src.database import async_engine
from fastapi import FastAPI


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username]


class ClientsAdmin(ModelView, model=Clients):
    column_list = [Clients.first_name, Clients.last_name]


class PropertyAdmin(ModelView, model=Property):
    column_list = [Property.id, Property.city]


class PropertyImageAdmin(ModelView, model=PropertyImage):
    column_list = [PropertyImage.id, PropertyImage.image]


class DealsAdmin(ModelView, model=Deals):
    column_list = [Deals.id, Deals.deal_type]


def init_admin(app: FastAPI):
    admin = Admin(app, engine=async_engine)
    admin.add_view(UserAdmin)
    admin.add_view(ClientsAdmin)
    admin.add_view(PropertyAdmin)
    admin.add_view(PropertyImageAdmin)
    admin.add_view(DealsAdmin)
