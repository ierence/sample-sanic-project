from apps.users.models import User
from sqlalchemy import select
from sqlalchemy.orm import selectinload

import hashlib


async def authenticate(request, *args, **kwargs):

    username = request.json['username']
    password = request.json['password']

    stmt = select(User).options(selectinload(User.scope_records)
                                ).where(User.username == username)
    result = await request.ctx.session.scalars(stmt)
    user: User = result.first()

    new_hashed_password = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        user.salt,  # type: ignore
        100000
    )

    assert user.hashed_password == new_hashed_password

    scopes = [scope_record.value for scope_record in user.scope_records]
    auth_data = {"user_id": user.id, "scopes": scopes,
                 "active": user.active, "activated": user.activated}
    return auth_data
