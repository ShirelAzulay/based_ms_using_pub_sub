import config

def get_all_satellite_data():
    """
    Retrieves all data from the satellite data table.
    """
    return f"""
    SELECT * 
    FROM `{config.DATASET_NAME}.{config.TABLE_NAME}`;
    """


def get_data_within_polygon(polygon_wkt):
    """
    Retrieves all data where the geo_location falls within a specified polygon.

    :param polygon_wkt: The WKT string of the polygon to search within.
    """
    return f"""
    SELECT id, scan_time, sensor_name, sensor_type, geo_location, storage_location
    FROM `{config.DATASET_NAME}.{config.TABLE_NAME}`
    WHERE ST_WITHIN(
        geo_location, 
        ST_GEOGFROMTEXT('{polygon_wkt}')
    );
    """


def get_data_containing_point(longitude, latitude):
    """
    Retrieves all records where a specific point is contained within the geo_location polygon.

    :param longitude: Longitude of the point.
    :param latitude: Latitude of the point.
    """
    return f"""
    SELECT id, scan_time, sensor_name, sensor_type, ST_ASTEXT(geo_location) as polygon_wkt, storage_location, raw_data
    FROM `{config.DATASET_NAME}.{config.TABLE_NAME}`
    WHERE ST_CONTAINS(
        geo_location, 
        ST_GEOGPOINT({longitude}, {latitude})
    )
    ORDER BY scan_time DESC;
    """


def get_data_intersecting_polygon(polygon_wkt):
    """
    Retrieves all data where geo_location intersects a specified polygon.

    :param polygon_wkt: The WKT string of the polygon to check for intersections.
    """
    return f"""
    SELECT id, scan_time, sensor_name, sensor_type, geo_location, storage_location
    FROM `{config.DATASET_NAME}.{config.TABLE_NAME}`
    WHERE ST_INTERSECTS(
        geo_location, 
        ST_GEOGFROMTEXT('{polygon_wkt}')
    );
    """


def get_data_containing_polygon(polygon_wkt):
    """
    Retrieves all data where the geo_location fully contains the specified polygon.

    :param polygon_wkt: The WKT string of the polygon to check containment.
    """
    return f"""
    SELECT id, scan_time, sensor_name, sensor_type, geo_location, storage_location
    FROM `{config.DATASET_NAME}.{config.TABLE_NAME}`
    WHERE ST_CONTAINS(
        geo_location, 
        ST_GEOGFROMTEXT('{polygon_wkt}')
    );
    """
