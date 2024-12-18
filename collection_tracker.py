"""
collection_tracker.py

Manages the collection inventory, wanted items, and items to sell using a PostgreSQL database.
"""
# collection_tracker.py

import psycopg2
import os
from dotenv import load_dotenv
from collection_item import CollectionItem

load_dotenv()

class CollectionTracker:
    def __init__(self, host, user, password, database, port=5432):
        self.conn = psycopg2.connect(
            dbname=database,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cur = self.conn.cursor()

    def add_item(self, item):
        self.cur.execute(
            """
            INSERT INTO inventory (name, category, quantity, price, image_path, year, location)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (item.name, item.category, item.quantity, item.price, item.image_path, item.year, item.location)
        )
        self.conn.commit()

    def remove_item(self, item_name):
        self.cur.execute("DELETE FROM inventory WHERE name = %s", (item_name,))
        self.conn.commit()

    def update_item(self, item_name, quantity=None, price=None, image_path=None, year=None, location=None):
        query = "UPDATE inventory SET "
        fields = []
        values = []

        if quantity is not None:
            fields.append("quantity = %s")
            values.append(quantity)
        if price is not None:
            fields.append("price = %s")
            values.append(price)
        if image_path is not None:
            fields.append("image_path = %s")
            values.append(image_path)
        if year is not None:
            fields.append("year = %s")
            values.append(year)
        if location is not None:
            fields.append("location = %s")
            values.append(location)

        query += ", ".join(fields)
        query += " WHERE name = %s"
        values.append(item_name)

        self.cur.execute(query, values)
        self.conn.commit()

    def get_inventory(self):
        self.cur.execute("SELECT name, category, quantity, price, image_path, year, location FROM inventory")
        rows = self.cur.fetchall()
        return [CollectionItem(*row) for row in rows]

    def add_wanted_item(self, item):
        self.cur.execute(
            """
            INSERT INTO wanted_items (name, category, quantity, price, image_path, year, location)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (item.name, item.category, item.quantity, item.price, item.image_path, item.year, item.location)
        )
        self.conn.commit()

    def remove_wanted_item(self, item_name):
        self.cur.execute("DELETE FROM wanted_items WHERE name = %s", (item_name,))
        self.conn.commit()

    def get_wanted_items(self):
        self.cur.execute("SELECT name, category, quantity, price, image_path, year, location FROM wanted")
        rows = self.cur.fetchall()
        return [CollectionItem(*row) for row in rows]

    def update_wanted_item_price(self, item_name):
        # Dummy implementation for price update from web scraping
        # Replace this with actual scraping logic
        new_price = 100.00  # Example new price
        self.cur.execute("UPDATE wanted_items SET price = %s WHERE name = %s", (new_price, item_name))
        self.conn.commit()
        return new_price

    def add_sell_item(self, item, threshold):
        self.cur.execute(
            """
            INSERT INTO sell_items (name, category, quantity, price, image_path, year, location, threshold)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (item.name, item.category, item.quantity, item.price, item.image_path, item.year, item.location, threshold)
        )
        self.conn.commit()

    def remove_sell_item(self, item_name):
        self.cur.execute("DELETE FROM sell_items WHERE name = %s", (item_name,))
        self.conn.commit()

    def get_sell_items(self):
        self.cur.execute("SELECT name, category, quantity, price, image_path, year, location, threshold FROM sell")
        rows = self.cur.fetchall()
        return [(CollectionItem(*row[:7]), row[7]) for row in rows]

    def check_sell_item_price(self, item_name):
        # Dummy implementation for price check from web scraping
        # Replace this with actual scraping logic
        current_price = 150.00  # Example current price
        return current_price

    def update_sell_item_price(self, item_name, new_price):
        self.cur.execute("UPDATE sell_items SET price = %s WHERE name = %s", (new_price, item_name))
        self.conn.commit()
