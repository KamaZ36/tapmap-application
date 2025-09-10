import pytest
from app.domain.value_objects.coordinates import Coordinates


def test_coordinates_valid() -> None:
    coord = Coordinates(latitude=55.7558, longitude=37.6173)  # Москва, например
    assert coord.latitude == 55.7558
    assert coord.longitude == 37.6173
    assert str(coord) == "(55.7558, 37.6173)"


@pytest.mark.parametrize("lat", [-91, 91, 1000, -1000])
def test_coordinates_invalid_latitude(lat) -> None:
    with pytest.raises(ValueError, match="Latitude .* out of range"):
        Coordinates(latitude=lat, longitude=0)


@pytest.mark.parametrize("lon", [-181, 181, 1000, -1000])
def test_coordinates_invalid_longitude(lon) -> None:
    with pytest.raises(ValueError, match="Longitude .* out of range"):
        Coordinates(latitude=0, longitude=lon)
