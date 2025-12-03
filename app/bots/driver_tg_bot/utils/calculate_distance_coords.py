from math import atan2, sin, sqrt, cos, radians


def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371000  # Радиус Земли в метрах
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c
