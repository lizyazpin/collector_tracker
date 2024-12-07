"""
collection_item.py

Defines the CollectionItem class to represent items in the collection.
"""

class CollectionItem:
    def __init__(self, name, category, quantity, price, image_path=None):
        """
        Initialize a CollectionItem instance.

        :param name: Name of the item
        :param category: Category of the item
        :param quantity: Quantity of the item
        :param price: Price of the item
        :param image_path: Path to the image file of the item
        """
        self.name = name
        self.category = category
        self.quantity = quantity
        self.price = price
        self.image_path = image_path

    def __repr__(self):
        """
        Return a string representation of the CollectionItem instance.
        """
        return f"{self.name} ({self.category}): {self.quantity} @ ${self.price}, Image: {self.image_path or 'None'}"
