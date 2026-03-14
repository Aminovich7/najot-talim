import os
from django.shortcuts import render
from django.http import HttpResponse
import psycopg2


import psycopg2

db_info = {
    "host": os.environ.get("PG_HOST", "localhost"),
    "database": os.environ.get("PG_DATABASE", "dorixona_x"),
    "user": os.environ.get("PG_USER", "postgres"),
    "password": os.environ.get("PG_PASSWORD", ""),
    "port": int(os.environ.get("PG_PORT", "5432")),
}



def view_inventory():
    try:
        with psycopg2.connect(**db_info) as conn:
            with conn.cursor() as cur:
                query = "SELECT * FROM dorilar_table;"
                cur.execute(query)
                rows = cur.fetchall()
                for i in rows:
                    print(HttpResponse(i))

                
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Connection failed: {error}")


def add_inventory(name, manufacturer,price, expiry_date, quantity):
    try:
        with psycopg2.connect(**db_info) as conn:
            with conn.cursor() as cur:
                query = """INSERT INTO dorilar_table (name, manufacturer, price, expiry_date, quantity)
                VALUES(%s, %s, %s, %s, %s)"""
                cur.execute(query, (name, manufacturer, price, expiry_date, quantity))

                return HttpResponse(f'{name} added successfully')


                
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Connection failed: {error}")


def delete_medicine(name):
    try:
        with psycopg2.connect(**db_info) as conn:
            with conn.cursor() as cur:
                query = """
                DELETE FROM dorilar_table
                WHERE name = %s
                """
                cur.execute(query, (name,))
                
                HttpResponse("Medicine deleted successfully")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Delete failed: {error}")