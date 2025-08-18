import pytest
from decimal import Decimal
from app.domain.value_objects.money import Money

def test_money_creation_and_rounding():
    m = Money(Decimal("10.005"))
    assert m.value == Decimal("10.01")

def test_money_creation_negative_value():
    with pytest.raises(ValueError, match="Неверное значение суммы"):
        Money(-1)

def test_money_addition():
    m1 = Money(10)
    m2 = Money(5.25)
    result = m1 + m2
    assert result.value == Decimal("15.25")

def test_money_subtraction():
    m1 = Money(10)
    m2 = Money(3)
    result = m1 - m2
    assert result.value == Decimal("7")

def test_money_subtraction_negative_result():
    m1 = Money(5)
    m2 = Money(10)
    with pytest.raises(ValueError, match="не может быть отрицательным"):
        _ = m1 - m2

def test_money_multiplication():
    m = Money(10)
    result = m * 2.5
    assert result.value == Decimal("25.00")

def test_money_right_multiplication():
    m = Money(10)
    result = 2 * m
    assert result.value == Decimal("20.00")

def test_money_division():
    m = Money(10)
    result = m / 2
    assert result.value == Decimal("5.00")

def test_money_division_by_zero():
    m = Money(10)
    with pytest.raises(ZeroDivisionError):
        _ = m / 0
        