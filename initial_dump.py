import asyncio

from sqlalchemy.exc import IntegrityError

from api.schemas.category_schemas import CategoryCreate
from api.schemas.user_schemas import AdminCreate, Role, UserCreate
from api.services.user_service import get_user_service
from api.services.category_service import get_category_service

from api.utils.uow import UnitOfWork


async def main():
    uow = UnitOfWork()
    user_service = await get_user_service(uow)
    category_service = await get_category_service(uow)

    new_users = [
         AdminCreate(
            telegram_id='admin',
            password='pass',
            name='admin',
            role=Role.ADMIN
         ),
         UserCreate(
             telegram_id='user',
             password='pass',
             name='user',
             role=Role.USER
         )
    ]

    for new_user in new_users:
        try:
            user = await user_service.add_user(new_user)
        except IntegrityError:
            print('User already exists')
            user = await user_service.get_user(telegram_id=new_user.telegram_id)

        print(user)

        new_categories = [
            {'name': 'category_1', 'symbol': '1️⃣'},
            {'name': 'category_2', 'symbol': '2️⃣'},
            {'name': 'category_3', 'symbol': '3️⃣'},
        ]
        for category in new_categories:
            print(
                await category_service.create_instance(
                    CategoryCreate(user_id=user.id, **category)
                )
            )


asyncio.run(main())
