from sqlalchemy import select
from sqlalchemy.orm import selectinload

from .models import ActivationLink


async def get_activation_link_by_link(request, link):
    stmt = select(ActivationLink).options(selectinload(
        ActivationLink.user)).where(ActivationLink.link == link)

    result = await request.ctx.session.scalars(stmt)

    activation_link = result.first()

    return activation_link
