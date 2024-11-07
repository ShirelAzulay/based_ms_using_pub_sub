import config
from google.cloud import bigquery
import logging

def insert_row_into_bigquery(bigquery_client, dataset_name, table_name, message_text):
    """
    Inserts a single row into a BigQuery table.

    :param bigquery_client: BigQuery client.
    :param dataset_name: The dataset name in BigQuery.
    :param table_name: The table name in BigQuery.
    :param message_text: The message text to insert.
    """
    table_id = f"{dataset_name}.{table_name}"
    rows_to_insert = [{"message": message_text}]  # Define the structure of the row to insert

    try:
        errors = bigquery_client.insert_rows_json(table_id, rows_to_insert)
        if errors:
            logging.error(f"Errors while inserting row into BigQuery: {errors}")
        else:
            logging.info("New row has been added to BigQuery")
    except Exception as e:
        logging.error(f"Failed to insert row into BigQuery: {e}")


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
