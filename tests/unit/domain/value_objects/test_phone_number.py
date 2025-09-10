import pytest
from app.domain.value_objects.phone_number import PhoneNumber


def test_phone_number_valid_7_prefix() -> None:
    pn = PhoneNumber("79991234567")
    assert pn.value == "79991234567"
    assert str(pn) == "79991234567"


def test_phone_number_valid_8_prefix() -> None:
    pn = PhoneNumber("89991234567")
    # Нормализуется в 7 + остальное
    assert pn.value == "79991234567"


def test_phone_number_valid_plus7_prefix() -> None:
    pn = PhoneNumber("+79991234567")
    assert pn.value == "79991234567"


def test_phone_number_invalid_prefix() -> None:
    with pytest.raises(ValueError):
        PhoneNumber("59991234567")  # Не начинается с 7, 8 или +7


def test_phone_number_invalid_length() -> None:
    with pytest.raises(ValueError):
        PhoneNumber("7999123456")  # 9 цифр после 7 — слишком короткий

    with pytest.raises(ValueError):
        PhoneNumber("799912345678")  # 11 цифр после 7 — слишком длинный


def test_phone_number_non_digit_characters() -> None:
    pn = PhoneNumber("+7 (999) 123-45-67")
    assert pn.value == "79991234567"


def test_phone_number_all_digits() -> None:
    pn = PhoneNumber("7" * 11)
    assert pn.value == "7" * 11
