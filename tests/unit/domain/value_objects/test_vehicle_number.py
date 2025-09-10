import pytest
from app.domain.value_objects.vehicle_number import VehicleNumber


def test_vehicle_number_valid() -> None:
    valid_numbers = ["А123ВС77", "В 456 МН99", "Р789ХХ199", "М321РТ750", "С111СС01"]
    for number in valid_numbers:
        vn = VehicleNumber(number)
        # Проверяем, что пробелы убраны и все буквы в верхнем регистре
        assert vn.value == number.replace(" ", "").upper()
        assert str(vn) == vn.value


def test_vehicle_number_invalid() -> None:
    invalid_numbers = [
        "123АВС77",  # начинается с цифры
        "А12ВС7777",  # слишком длинный
        "А12 В5МН99",  # пробел внутри
        "XYZ12345",  # невалидные буквы
        "А1234ВС7",  # цифр слишком много
        "",
    ]
    for number in invalid_numbers:
        with pytest.raises(ValueError):
            VehicleNumber(number)
