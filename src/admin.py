from fastapi_admin.app import app as admin_app
from fastapi_admin.providers.login import UsernamePasswordProvider
from fastapi_admin.widgets import inputs
from src.auth.models import User
from fastapi_admin.resources import Model
from fastapi import Request


class UserResources(Model):
    label = 'Users'
    model = User
    fields = [
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'is_superuser',
        'is_active',
        'created_at',
        'updated_at'
    ]
    filters = [
        inputs.Search(name='username', label='Username'),
        inputs.Select(name='is_superuser', label='Superuser', options=[
            ('', 'All'), ('true', 'True'), ('false', 'False')
        ]),
        inputs.Select(name='is_active', label='Active', options=[
            ('', 'All'), ('true', 'True'), ('false', 'False')
        ])
    ]

    async def get_queryset(self, request: Request):
        queryset = await super().get_queryset(request)
        return queryset


async def setup_admin(app):
    admin_app.setup(
        app,
        admin_secret='',
        providers=[
            UsernamePasswordProvider(
                admin_model=User,
                login_button_text='Login',
                username_field=inputs.Text(label='Username'),
                password_filed=inputs.Text(label='Password')
            )
        ],
        resources=[UserResources(User, display_name='Users')]
    )