"""
collection_app.py

Defines the graphical user interface for the collection tracker using tkinter.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
from collection_item import CollectionItem
from collection_tracker import CollectionTracker

class CollectionApp:
    def __init__(self, root, tracker):
        """
        Initialize the CollectionApp instance.

        :param root: Root tkinter window
        :param tracker: CollectionTracker instance
        """
        self.tracker = tracker
        self.root = root
        self.root.title("Collection Tracker")
        
        self.create_widgets()

    def create_widgets(self):
        """
        Create and arrange widgets in the GUI.
        """
        self.name_label = tk.Label(self.root, text="Name:")
        self.name_label.grid(row=0, column=0)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(row=0, column=1)

        self.category_label = tk.Label(self.root, text="Category:")
        self.category_label.grid(row=1, column=0)
        self.category_entry = tk.Entry(self.root)
        self.category_entry.grid(row=1, column=1)

        self.quantity_label = tk.Label(self.root, text="Quantity:")
        self.quantity_label.grid(row=2, column=0)
        self.quantity_entry = tk.Entry(self.root)
        self.quantity_entry.grid(row=2, column=1)

        self.price_label = tk.Label(self.root, text="Price:")
        self.price_label.grid(row=3, column=0)
        self.price_entry = tk.Entry(self.root)
        self.price_entry.grid(row=3, column=1)

        self.image_label = tk.Label(self.root, text="Image:")
        self.image_label.grid(row=4, column=0)
        self.image_path = tk.StringVar()
        self.image_entry = tk.Entry(self.root, textvariable=self.image_path)
        self.image_entry.grid(row=4, column=1)
        self.image_button =
