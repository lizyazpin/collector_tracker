"""
collection_tracker.py

Manages the collection inventory, wanted items, and items to sell using a MySQL database.
"""

import mysql.connector
from collection_item import CollectionItem
from price_scraper import get_price

class CollectionTracker:
    def __init__(self, host, user, password, database):
        """
        Initialize a CollectionTracker instance.

        :param host: MySQL server host
        :param user: MySQL username
        :param password: MySQL password
        :param database: MySQL database name
        """
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.conn.cursor()

    def add_item(self, item):
        """
        Add an item to the inventory.

        :param item: CollectionItem instance to add
        """
        sql = "INSERT INTO Inventory (name, category, quantity, price, image_path) VALUES (%s, %s, %s, %s, %s)"
        val = (item.name, item.category, item.quantity, item.price, item.image_path)
        self.cursor.execute(sql, val)
        self.conn.commit()

    def remove_item(self, item_name):
        """
        Remove an item from the inventory by name.

        :param item_name: Name of the item to remove
        """
        sql = "DELETE FROM Inventory WHERE name = %s"
        val = (item_name,)
        self.cursor.execute(sql, val)
        self.conn.commit()

    def update_item(self, item_name, quantity=None, price=None, image_path=None):
        """
        Update the details of an existing item in the inventory.

        :param item_name: Name of the item to update
        :param quantity: New quantity (optional)
        :param price: New price (optional)
        :param image_path: New image path (optional)
        """
        if quantity is not None:
            sql = "UPDATE Inventory SET quantity = %s WHERE name = %s"
            val = (quantity, item_name)
            self.cursor.execute(sql, val)
        if price is not None:
            sql = "UPDATE Inventory SET price = %s WHERE name = %s"
            val = (price, item_name)
            self.cursor.execute(sql, val)
        if image_path is not None:
            sql = "UPDATE Inventory SET image_path = %s WHERE name = %s"
            val = (image_path, item_name)
            self.cursor.execute(sql, val)
        self.conn.commit()

    def add_wanted_item(self, item):
        """
        Add an item to the wanted list.

        :param item: CollectionItem instance to add
        """
        sql = "INSERT INTO Wanted (name, category, quantity, price, image_path) VALUES (%s, %s, %s, %s, %s)"
        val = (item.name, item.category, item.quantity, item.price, item.image_path)
        self.cursor.execute(sql, val)
        self.conn.commit()

    def remove_wanted_item(self, item_name):
        """
        Remove an item from the wanted list by name.

        :param item_name: Name of the item to remove
        """
        sql = "DELETE FROM Wanted WHERE name = %s"
        val = (item_name,)
        self.cursor.execute(sql, val)
        self.conn.commit()

    def add_sell_item(self, item, threshold):
        """
        Add an item to the sell list.

        :param item: CollectionItem instance to add
        :param threshold: Price threshold for selling
        """
        sql = "INSERT INTO Sell (name, category, quantity, price, image_path, threshold) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (item.name, item.category, item.quantity, item.price, item.image_path, threshold)
        self.cursor.execute(sql, val)
        self.conn.commit()

    def remove_sell_item(self, item_name):
        """
        Remove an item from the sell list by name.

        :param item_name: Name of the item to remove
        """
        sql = "DELETE FROM Sell WHERE name = %s"
        val = (item_name,)
        self.cursor.execute(sql, val)
        self.conn.commit()

    def get_inventory(self):
        """
        Retrieve all items in the inventory.

        :return: List of CollectionItem instances
        """
        self.cursor.execute("SELECT name, category, quantity, price, image_path FROM Inventory")
        return [CollectionItem(name, category, quantity, price, image_path) for (name, category, quantity, price, image_path) in self.cursor]

    def get_wanted_items(self):
        """
        Retrieve all items in the wanted list.

        :return: List of CollectionItem instances
        """
        self.cursor.execute("SELECT name, category, quantity, price, image_path FROM Wanted")
        return [CollectionItem(name, category, quantity, price, image_path) for (name, category, quantity, price, image_path) in self.cursor]

    def get_sell_items(self):
        """
        Retrieve all items in the sell list.

        :return: List of CollectionItem instances with threshold
        """
        self.cursor.execute("SELECT name, category, quantity, price, image_path, threshold FROM Sell")
        return [(CollectionItem(name, category, quantity, price, image_path), threshold) for (name, category, quantity, price, image_path, threshold) in self.cursor]

    def total_value(self):
        """
        Calculate the total value of all items in the inventory.

        :return: Total value of inventory items
        """
        self.cursor.execute("SELECT SUM(quantity * price) FROM Inventory")
        return self.cursor.fetchone()[0] or 0.0

    def update_wanted_item_prices(self):
        """
        Update the prices of wanted items by scraping the web.
        """
        wanted_items = self.get_wanted_items()
        for item in wanted_items:
            new_price = get_price(item.name)
            if new_price is not None:
                self.update_item(item.name, price=new_price)

    def check_sell_item_prices(self):
        """
        Check the prices of items in the sell list and send alerts if the price meets the threshold.
        """
        sell_items = self.get_sell_items()
        for item, threshold in sell_items:
            current_price = get_price(item.name)
            if current_price is not None and current_price >= threshold:
                self.send_alert(item.name, current_price)

    def send_alert(self, item_name, current_price):
        """
        Send an alert that an item's price has met the threshold.

        :param item_name: Name of the item
        :param current_price: Current price of the item
        """
        print(f"Alert: {item_name} is now ${current_price:.2f}, meeting the threshold!")

    def close(self):
        """
        Close the database connection.
        """
        self.conn.close()
