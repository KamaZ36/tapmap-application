from app.utils.uuid_v7 import uuid7
from app.domain.entities.user import User
from app.domain.value_objects.phone_number import PhoneNumber
from app.domain.enums.user import UserRole


def test_create_user_success() -> None:
    user = User(
        name="Виктор",
        phone_number=PhoneNumber("79999999999"),
    )

    assert user.base_city_id is None
    assert user.cancelled_orders_count == 0
    assert user.completed_orders_count == 0
    assert user.name == "Виктор"
    assert isinstance(user.phone_number, PhoneNumber)
    assert user.phone_number.value == "79999999999"
    assert user.roles == [UserRole.user]


def test_complete_order_for_user() -> None:
    user = User(
        name="Виктор",
        phone_number=PhoneNumber("79999999999"),
    )

    assert user.completed_orders_count == 0
    user.complete_order()
    assert user.completed_orders_count == 1


def test_cancel_order_for_user() -> None:
    user = User(
        name="Виктор",
        phone_number=PhoneNumber("79999999999"),
    )

    assert user.cancelled_orders_count == 0
    user.cancel_order()
    assert user.cancelled_orders_count == 1


def test_set_base_city_for_user() -> None:
    user = User(
        name="Виктор",
        phone_number=PhoneNumber("79999999999"),
    )
    assert user.base_city_id is None
    city_id = uuid7()
    user.set_base_city(city_id)
    assert user.base_city_id == city_id


def test_user_roles_management() -> None:
    user = User(
        name="Виктор",
        phone_number=PhoneNumber("79999999999"),
    )

    # Проверяем начальную роль
    assert user.has_role(UserRole.user)
    assert not user.has_role(UserRole.admin)

    # Добавляем роль
    user.add_role(UserRole.admin)
    assert user.has_role(UserRole.admin)
    assert len(user.roles) == 2

    # Добавляем ту же роль повторно (не должно дублироваться)
    user.add_role(UserRole.admin)
    assert len(user.roles) == 2

    # Удаляем роль
    user.remove_role(UserRole.admin)
    assert not user.has_role(UserRole.admin)
    assert user.has_role(UserRole.user)
    assert len(user.roles) == 1
