"""
Writer class for PostgreSQL that suits the expectations of the turbo stream services.
"""
import logging

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from turbo_stream import _WriterInterface

logging.basicConfig(
    format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s", level=logging.INFO
)


class _PostgreSQLWriter(_WriterInterface):
    def __init__(self, credentials: (dict, str), configuration: dict = None, **kwargs):
        super().__init__(configuration, credentials, **kwargs)

        self._credentials = credentials
        self._configuration = configuration

        self._test_cursor()

    def _connect(self):
        """
        Establish connection to PostgreSQL database.
        The basic connection parameters are:
        - *dbname*: the database name
        - *database*: the database name (only as keyword argument)
        - *user*: user name used to authenticate (defaults to postgres if not provided)
        - *password*: password used to authenticate
        - *host*: database host address (defaults to UNIX socket if not provided)
        - *port*: connection port number (defaults to 5432 if not provided)
        """
        logging.info(f"Establishing a connection to PostgreSQL database.")

        if "dbname" in self._credentials:
            return psycopg2.connect(
                dbname=self._credentials.get("dbname"),
                user=self._credentials.get("user", "postgres"),
                password=self._credentials.get("password"),
                host=self._credentials.get("host"),
                port=self._credentials.get("port", 5432),
            )

        return psycopg2.connect(
            database=self._credentials.get("database", "postgres"),
            user=self._credentials.get("user", "postgres"),
            password=self._credentials.get("password"),
            host=self._credentials.get("host", "localhost"),
            port=self._credentials.get("port", 5432),
        )

    def _test_cursor(self):
        """
        Get PostgreSQL cursor for querying.
        :return: Cursor object.
        """
        # test the connection before returning it
        try:
            self._execute_query("SELECT 1")
            logging.info("Connection to PostgreSQL successful.")

        except psycopg2.OperationalError as err:
            logging.info("Connection to PostgreSQL failed.")
            raise err

    def _execute_query(self, query, dataset=None):
        #  Some PostgreSQL command such as CREATE DATABASE or VACUUM can’t run into a transaction.
        _connection = self._connect()
        _connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        _cursor = _connection.cursor()
        logging.info(query)
        if dataset is None:
            _cursor.execute(query)
        else:
            _cursor.executemany(query, dataset)
        _connection.close()

    def _create_table(self, table_name: str, schema: dict):
        """
        Converts a standardised dict object that represents the typical PostgreSQL
        Table Schema and generates a physical database from it.
        :param table_name: The name of the new table.
        :param schema: The dict schema object of the new table which looks like:
                        schema = {
                            "user_id": {
                                "type": "INT",
                                "not_null": True,
                                "primary_key": True,
                                "unique": True
                            },
                            "user_name": {
                                "type": "INT",
                                "not_null": True,
                                "primary_key": False,
                                "unique": False,
                            },
                        }
        """
        logging.info(
            f"Attempting to create {table_name} table for PostgreSQL database."
        )
        field_set_string = []
        count = 1
        for field_name, field_meta in schema.items():
            field_set_string.append(field_name)

            if field_meta.get("type", False):
                field_set_string.append(field_meta.get("type"))

            if field_meta.get("not null", False):
                field_set_string.append("NOT NULL")

            if field_meta.get("primary_key", False):
                field_set_string.append("PRIMARY KEY")

            if field_meta.get("unique", False):
                field_set_string.append("UNIQUE")

            if len(schema) > count:
                # break each statement except for the last one
                field_set_string.append(",")

            count += 1

        query_frame_string = (
            f"CREATE TABLE IF NOT EXISTS "
            f"{table_name} (ts_id SERIAL, ts_date DATE DEFAULT now(), {' '.join(field_set_string)});"
        )

        self._execute_query(query_frame_string)

        logging.info(
            f"Attempting to create {table_name} table for PostgreSQL database complete."
        )

    def _insert_table(self, table_name: str, dataset: list, truncate_on_insert=False):
        """
        Submits a dataset in a record orientation that fists the tables schema.
        :param table_name: The table to write to.
        :param dataset: The dataset that fits the table schema.
        :param truncate_on_insert: Bool to clear out table before inserting dataset.
        """

        if truncate_on_insert:
            logging.info(f"Attempting to truncate {table_name} table.")
            query = f"TRUNCATE TABLE {table_name};"
            self._execute_query(query)

        logging.info(f"Attempting to insert data into {table_name} table.")
        fields = [str(f) for f in dataset[0].keys()]

        value_insert_set = []
        for field in fields:
            value_insert_set.append(f"%({field})s")

        query = (
            f"INSERT INTO {table_name}({', '.join(fields)}) "
            f"VALUES ({', '.join(value_insert_set)})"
        )
        self._execute_query(query=query, dataset=dataset)
        logging.info(f"Attempting to insert data into {table_name} table complete.")

    def _drop_duplicates(self, table_name: str, schema: dict):
        """
        Query to drop all fields that may have duplicates.
        This is faster because this runs only 2 queries.
        First one to select all the duplicates, then one to delete all items from the table.
        :param table_name: The name of the new table.
        :param schema: The dict schema object of the new table which looks like:
                        schema = {
                            "user_id": {
                                "type": "INT",
                                "not_null": True,
                                "primary_key": True,
                                "unique": True
                            },
                            "user_name": {
                                "type": "INT",
                                "not_null": True,
                                "primary_key": False,
                                "unique": False,
                            },
                        }
        """

        logging.info(f"Attempting to drop duplicates for {table_name} table.")
        fields = schema.keys()
        comparison_clauses = []
        for field in fields:
            comparison_clauses.append(f"a.{field} = b.{field}")
        query = (
            f"DELETE FROM {table_name} a USING (SELECT MIN(ctid) as ctid, {', '.join(fields)} "
            f"FROM {table_name} GROUP BY {', '.join(fields)} HAVING COUNT(*) > 1) b WHERE "
            f"{' AND '.join(comparison_clauses)} AND a.ctid <> b.ctid;"
        )
        logging.info(query)
        self._execute_query(query)
        logging.info(f"Attempting to drop duplicates for {table_name} table complete.")
