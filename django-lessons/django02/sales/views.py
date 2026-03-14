import os
from django.shortcuts import render
from django.http import HttpResponse
import psycopg2

db_info = {
    "host": os.environ.get("PG_HOST", "localhost"),
    "database": os.environ.get("PG_DATABASE", "dorixona_x"),
    "user": os.environ.get("PG_USER", "postgres"),
    "password": os.environ.get("PG_PASSWORD", ""),
    "port": int(os.environ.get("PG_PORT", "5432")),
}


def sell_medicine(name, sell_quantity):
    try:
        with psycopg2.connect(**db_info) as conn:
            with conn.cursor() as cur:

                check_query = """
                SELECT quantity FROM dorilar_table
                WHERE name = %s
                """
                cur.execute(check_query, (name,))
                result = cur.fetchone()

                if result is None:
                    print("Medicine not found")
                    return

                current_quantity = result[0]

                if current_quantity < sell_quantity:
                    print("Not enough stock")
                    return

                update_query = """
                UPDATE dorilar_table
                SET quantity = quantity - %s
                WHERE name = %s
                """
                cur.execute(update_query, (sell_quantity, name))

                print("Medicine sold successfully")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Sale failed: {error}")


def return_medicine(name, return_quantity):
    try:
        with psycopg2.connect(**db_info) as conn:
            with conn.cursor() as cur:

                query = """
                UPDATE dorilar_table
                SET quantity = quantity + %s
                WHERE name = %s
                """

                cur.execute(query, (return_quantity, name))

                print("Medicine returned successfully")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Return failed: {error}")