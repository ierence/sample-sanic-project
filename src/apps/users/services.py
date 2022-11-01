from apps.auth.models import ActivationLink, ScopeRecord
from apps.auth.selectors import get_activation_link_by_link

from .models import User
from .schemas import UserUpdate
from .selectors import retrieve_user

import hashlib
import os


async def create_user(request, body):
    salt = os.urandom(32)
    hashed_password = hashlib.pbkdf2_hmac(
        'sha256', body.password.encode("utf8"), salt, 100000)

    user = User(
        username=body.username,
        hashed_password=hashed_password,
        salt=salt
    )

    # add user scope
    scope_record = ScopeRecord(
        user=user,
        value='user'
    )

    # generate_activation_link
    activation_link = ActivationLink(
        user=user
    )

    request.ctx.session.add(user)
    request.ctx.session.add(scope_record)
    request.ctx.session.add(activation_link)

    await request.ctx.session.commit()

    return user


async def update_user(request, pk):
    user_data = UserUpdate(
        **request.json
    )

    user = await retrieve_user(request, pk)

    for key, value in user_data.__dict__.items():
        setattr(user, key, value)

    await request.ctx.session.commit()

    return user


async def activate_user(request, key):
    activation_link = await get_activation_link_by_link(request, key)

    activation_link.user.activated = True

    await request.ctx.session.commit()
