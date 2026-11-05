"""Domestic NIU GCJ-02 coordinates to approximate WGS-84 coordinates.

Formula adapted from hasscc/home-assistant-niu-component sensor.py.
Invalid/missing fixes return None rather than a misleading location at (0, 0).
"""

import math

PI = math.pi
ee = 0.00669342162296594323
a = 6378245.0


def gcj02_to_wgs84(lng, lat):
    try:
        lat = float(lat)
        lng = float(lng)
    except (TypeError, ValueError, OverflowError):
        return None
    if not math.isfinite(lng) or not math.isfinite(lat):
        return None
    if not (-180 <= lng <= 180 and -90 <= lat <= 90) or lng == 0 or lat == 0:
        return None

    if out_of_china(lng, lat):
        return lng, lat
    else:
        dlat = transformlat(lng - 105.0, lat - 35.0)
        dlng = transformlng(lng - 105.0, lat - 35.0)
        radlat = lat / 180.0 * PI
        magic = math.sin(radlat)
        magic = 1 - ee * magic * magic
        sqrtmagic = math.sqrt(magic)
        dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * PI)
        dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * PI)
        mglat = lat + dlat
        mglng = lng + dlng
        return lng * 2 - mglng, lat * 2 - mglat


def out_of_china(lng, lat):
    lat = float(lat)
    lng = float(lng)
    return not (lng > 73.66 and lng < 135.05 and lat > 3.86 and lat < 53.55)


def transformlat(lng, lat):
    lat = float(lat)
    lng = float(lng)
    ret = (
        -100.0
        + 2.0 * lng
        + 3.0 * lat
        + 0.2 * lat * lat
        + 0.1 * lng * lat
        + 0.2 * math.sqrt(abs(lng))
    )
    ret += (
        (20.0 * math.sin(6.0 * lng * PI) + 20.0 * math.sin(2.0 * lng * PI)) * 2.0 / 3.0
    )
    ret += (20.0 * math.sin(lat * PI) + 40.0 * math.sin(lat / 3.0 * PI)) * 2.0 / 3.0
    ret += (
        (160.0 * math.sin(lat / 12.0 * PI) + 320 * math.sin(lat * PI / 30.0))
        * 2.0
        / 3.0
    )
    return ret


def transformlng(lng, lat):
    lat = float(lat)
    lng = float(lng)
    ret = (
        300.0
        + lng
        + 2.0 * lat
        + 0.1 * lng * lng
        + 0.1 * lng * lat
        + 0.1 * math.sqrt(abs(lng))
    )
    ret += (
        (20.0 * math.sin(6.0 * lng * PI) + 20.0 * math.sin(2.0 * lng * PI)) * 2.0 / 3.0
    )
    ret += (20.0 * math.sin(lng * PI) + 40.0 * math.sin(lng / 3.0 * PI)) * 2.0 / 3.0
    ret += (
        (150.0 * math.sin(lng / 12.0 * PI) + 300.0 * math.sin(lng / 30.0 * PI))
        * 2.0
        / 3.0
    )
    return ret
