from app.core.geo import bounding_box, haversine_miles

def test_haversine_zero_distance():
    assert haversine_miles(0, 0, 0, 0) == 0

def test_haversine_known_distance():
    # Rough distance between NYC and Boston ~190 miles
    d = haversine_miles(40.7128, -74.0060, 42.3601, -71.0589)
    assert 160 <= d <= 230

def test_bounding_box_contains_center():
    lat, lon = 42.3555, -71.0602
    min_lat, max_lat, min_lon, max_lon = bounding_box(lat, lon, 10)
    assert min_lat <= lat <= max_lat
    assert min_lon <= lon <= max_lon