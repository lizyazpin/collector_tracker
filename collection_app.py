"""
collection_app.py

Defines the CollectionApp class that provides the GUI for managing the collection inventory.
"""

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from collection_item import CollectionItem
import os
from PIL import Image, ImageTk
import textwrap

class CollectionApp:
    def __init__(self, root, tracker):
        self.root = root
        self.root.title("Collection Tracker")
        self.root.attributes("-fullscreen", True)  # Enable full-screen mode
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))  # Exit full-screen with Escape key
        self.tracker = tracker

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.inventory_tab = ttk.Frame(self.notebook)
        self.wanted_tab = ttk.Frame(self.notebook)
        self.sell_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.inventory_tab, text="Inventory")
        self.notebook.add(self.wanted_tab, text="Wanted Items")
        self.notebook.add(self.sell_tab, text="Sell Items")

        self.create_inventory_tab()
        self.create_wanted_tab()
        self.create_sell_tab()

    def create_inventory_tab(self):
        # Create a canvas to display items
        self.inventory_canvas = tk.Canvas(self.inventory_tab, bg="white")
        self.inventory_canvas.pack(fill=tk.BOTH, expand=True)

        # Add a scrollbar for the canvas
        self.inventory_scrollbar = ttk.Scrollbar(self.inventory_tab, orient=tk.VERTICAL, command=self.inventory_canvas.yview)
        self.inventory_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.inventory_canvas.configure(yscrollcommand=self.inventory_scrollbar.set)

        # Create a frame inside the canvas to hold the items
        self.inventory_frame = ttk.Frame(self.inventory_canvas)
        self.inventory_frame_id = self.inventory_canvas.create_window((0, 0), window=self.inventory_frame, anchor="nw")

        # Configure dynamic scrolling for the frame
        self.inventory_frame.bind("<Configure>", self._on_frame_configure)
        self.inventory_canvas.bind("<Configure>", self._on_canvas_resize)
    
        # Cache for loaded images
        self.image_cache = {}

        # Load and display inventory items inside the canvas (with scrollbar applied)
        self.load_inventory_with_images()

        # Create a separate frame for the form outside the canvas to prevent it from being affected by the scroll
        self.inventory_form_frame = ttk.Frame(self.inventory_tab)
        self.inventory_form_frame.pack(fill=tk.X, side=tk.BOTTOM)

        # Load the add or update inventory form
        self.add_update_inventory_form()
        
    def _on_frame_configure(self, event=None):
        """
        Adjust the canvas scroll region to match the size of the frame.
        """
        self.inventory_canvas.configure(scrollregion=self.inventory_canvas.bbox("all"))

    def _on_canvas_resize(self, event=None):
        """
        Ensure the frame width matches the canvas width.
        """
        canvas_width = event.width
        self.inventory_canvas.itemconfig(self.inventory_frame_id, width=canvas_width)

    def load_inventory_with_images(self):
        for widget in self.inventory_frame.winfo_children():
            widget.destroy()  # Clear existing items in the inventory display

        items = self.tracker.get_inventory()
        for index, item in enumerate(items):
            # Create a frame for each item
            item_frame = ttk.Frame(self.inventory_frame, borderwidth=2, relief=tk.GROOVE, padding=(9, 9))
            item_frame.grid(row=index // 13, column=index % 13, padx=9, pady=9)

            # Load image
            if item.image_path and os.path.exists(item.image_path):
                img = Image.open(item.image_path).resize((90, 90), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.image_cache[item.image_path] = photo  # Store reference to prevent garbage collection
                img_label = tk.Label(item_frame, image=photo)
                img_label.pack()
            else:
                # Placeholder image
                placeholder = Image.new("RGB", (90, 90), color="gray")
                photo = ImageTk.PhotoImage(placeholder)
                self.image_cache[f"placeholder_{index}"] = photo
                img_label = tk.Label(item_frame, image=photo)
                img_label.pack()

            # Display name and year
            #tk.Label(item_frame, text=item.name, font=("Arial", 10, "bold")).pack()
            wrapped_text = "\n".join(textwrap.wrap(item.name, width=15))  # Adjust width as needed
            tk.Label(item_frame, text=wrapped_text, font=("Arial", 10, "bold"), justify=tk.CENTER).pack()
            tk.Label(item_frame, text=f"Year: {item.year}", font=("Arial", 10)).pack()
    
    def add_update_inventory_form(self):
        # Form for adding or updating inventory items
        self.inventory_form = ttk.Frame(self.inventory_tab)
        self.inventory_form.pack(fill=tk.X)

        ttk.Label(self.inventory_form, text="Name:").pack(side=tk.LEFT)
        self.inventory_name = ttk.Entry(self.inventory_form)
        self.inventory_name.pack(side=tk.LEFT)

        ttk.Label(self.inventory_form, text="Category:").pack(side=tk.LEFT)
        self.inventory_category = ttk.Entry(self.inventory_form)
        self.inventory_category.pack(side=tk.LEFT)

        ttk.Label(self.inventory_form, text="Quantity:").pack(side=tk.LEFT)
        self.inventory_quantity = ttk.Entry(self.inventory_form)
        self.inventory_quantity.pack(side=tk.LEFT)

        ttk.Label(self.inventory_form, text="Price:").pack(side=tk.LEFT)
        self.inventory_price = ttk.Entry(self.inventory_form)
        self.inventory_price.pack(side=tk.LEFT)

        ttk.Label(self.inventory_form, text="Image Path:").pack(side=tk.LEFT)
        self.inventory_image_path = ttk.Entry(self.inventory_form)
        self.inventory_image_path.pack(side=tk.LEFT)

        ttk.Label(self.inventory_form, text="Year:").pack(side=tk.LEFT)
        self.inventory_year = ttk.Entry(self.inventory_form)
        self.inventory_year.pack(side=tk.LEFT)

        ttk.Label(self.inventory_form, text="Location:").pack(side=tk.LEFT)
        self.inventory_location = ttk.Entry(self.inventory_form)
        self.inventory_location.pack(side=tk.LEFT)

        ttk.Button(self.inventory_form, text="Add Item", command=self.add_inventory_item).pack(side=tk.LEFT)
        ttk.Button(self.inventory_form, text="Remove Item", command=self.remove_inventory_item).pack(side=tk.LEFT)
        ttk.Button(self.inventory_form, text="Update Item", command=self.update_inventory_item).pack(side=tk.LEFT)


    def create_wanted_tab(self):
        self.wanted_tree = ttk.Treeview(self.wanted_tab, columns=("Name", "Category", "Quantity", "Price", "Image Path", "Year", "Location"), show='headings')
        for col in self.wanted_tree["columns"]:
            self.wanted_tree.heading(col, text=col)
        self.wanted_tree.pack(fill=tk.BOTH, expand=True)

        self.load_wanted_items()

        self.wanted_form = ttk.Frame(self.wanted_tab)
        self.wanted_form.pack(fill=tk.X)

        ttk.Label(self.wanted_form, text="Name:").pack(side=tk.LEFT)
        self.wanted_name = ttk.Entry(self.wanted_form)
        self.wanted_name.pack(side=tk.LEFT)

        ttk.Label(self.wanted_form, text="Category:").pack(side=tk.LEFT)
        self.wanted_category = ttk.Entry(self.wanted_form)
        self.wanted_category.pack(side=tk.LEFT)

        ttk.Label(self.wanted_form, text="Quantity:").pack(side=tk.LEFT)
        self.wanted_quantity = ttk.Entry(self.wanted_form)
        self.wanted_quantity.pack(side=tk.LEFT)

        ttk.Label(self.wanted_form, text="Price:").pack(side=tk.LEFT)
        self.wanted_price = ttk.Entry(self.wanted_form)
        self.wanted_price.pack(side=tk.LEFT)

        ttk.Label(self.wanted_form, text="Image Path:").pack(side=tk.LEFT)
        self.wanted_image_path = ttk.Entry(self.wanted_form)
        self.wanted_image_path.pack(side=tk.LEFT)

        ttk.Label(self.wanted_form, text="Year:").pack(side=tk.LEFT)
        self.wanted_year = ttk.Entry(self.wanted_form)
        self.wanted_year.pack(side=tk.LEFT)

        ttk.Label(self.wanted_form, text="Location:").pack(side=tk.LEFT)
        self.wanted_location = ttk.Entry(self.wanted_form)
        self.wanted_location.pack(side=tk.LEFT)

        ttk.Button(self.wanted_form, text="Add Wanted Item", command=self.add_wanted_item).pack(side=tk.LEFT)
        ttk.Button(self.wanted_form, text="Remove Wanted Item", command=self.remove_wanted_item).pack(side=tk.LEFT)
        ttk.Button(self.wanted_form, text="Update Wanted Item Price", command=self.update_wanted_item_price).pack(side=tk.LEFT)

    def create_sell_tab(self):
        self.sell_tree = ttk.Treeview(self.sell_tab, columns=("Name", "Category", "Quantity", "Price", "Image Path", "Year", "Location", "Threshold"), show='headings')
        for col in self.sell_tree["columns"]:
            self.sell_tree.heading(col, text=col)
        self.sell_tree.pack(fill=tk.BOTH, expand=True)

        self.load_sell_items()

        self.sell_form = ttk.Frame(self.sell_tab)
        self.sell_form.pack(fill=tk.X)

        ttk.Label(self.sell_form, text="Name:").pack(side=tk.LEFT)
        self.sell_name = ttk.Entry(self.sell_form)
        self.sell_name.pack(side=tk.LEFT)

        ttk.Label(self.sell_form, text="Category:").pack(side=tk.LEFT)
        self.sell_category = ttk.Entry(self.sell_form)
        self.sell_category.pack(side=tk.LEFT)

        ttk.Label(self.sell_form, text="Quantity:").pack(side=tk.LEFT)
        self.sell_quantity = ttk.Entry(self.sell_form)
        self.sell_quantity.pack(side=tk.LEFT)

        ttk.Label(self.sell_form, text="Price:").pack(side=tk.LEFT)
        self.sell_price = ttk.Entry(self.sell_form)
        self.sell_price.pack(side=tk.LEFT)

        ttk.Label(self.sell_form, text="Image Path:").pack(side=tk.LEFT)
        self.sell_image_path = ttk.Entry(self.sell_form)
        self.sell_image_path.pack(side=tk.LEFT)

        ttk.Label(self.sell_form, text="Year:").pack(side=tk.LEFT)
        self.sell_year = ttk.Entry(self.sell_form)
        self.sell_year.pack(side=tk.LEFT)

        ttk.Label(self.sell_form, text="Location:").pack(side=tk.LEFT)
        self.sell_location = ttk.Entry(self.sell_form)
        self.sell_location.pack(side=tk.LEFT)

        ttk.Label(self.sell_form, text="Threshold:").pack(side=tk.LEFT)
        self.sell_threshold = ttk.Entry(self.sell_form)
        self.sell_threshold.pack(side=tk.LEFT)

        ttk.Button(self.sell_form, text="Add Sell Item", command=self.add_sell_item).pack(side=tk.LEFT)
        ttk.Button(self.sell_form, text="Remove Sell Item", command=self.remove_sell_item).pack(side=tk.LEFT)
        ttk.Button(self.sell_form, text="Check Sell Item Price", command=self.check_sell_item_price).pack(side=tk.LEFT)

    def load_inventory(self):
        for item in self.tracker.get_inventory():
            self.inventory_tree.insert('', 'end', values=(item.name, item.category, item.quantity, item.price, item.image_path, item.year, item.location))

    def load_wanted_items(self):
        for item in self.tracker.get_wanted_items():
            self.wanted_tree.insert('', 'end', values=(item.name, item.category, item.quantity, item.price, item.image_path, item.year))

    def load_sell_items(self):
        for item, threshold in self.tracker.get_sell_items():
            self.sell_tree.insert('', 'end', values=(item.name, item.category, item.quantity, item.price, item.image_path, item.year, item.location, threshold))

    def add_inventory_item(self):
        item = CollectionItem(
            name=self.inventory_name.get(),
            category=self.inventory_category.get(),
            quantity=int(self.inventory_quantity.get()),
            price=float(self.inventory_price.get()),
            image_path=self.inventory_image_path.get(),
            year=self.inventory_year.get(),
            location=self.inventory_location.get()
        )
        self.tracker.add_item(item)
        self.inventory_tree.insert('', 'end', values=(item.name, item.category, item.quantity, item.price, item.image_path, item.year, item.location))

    def remove_inventory_item(self):
        selected_item = self.inventory_tree.selection()[0]
        item_name = self.inventory_tree.item(selected_item, 'values')[0]
        self.tracker.remove_item(item_name)
        self.inventory_tree.delete(selected_item)

    def update_inventory_item(self):
        selected_item = self.inventory_tree.selection()[0]
        item_name = self.inventory_tree.item(selected_item, 'values')[0]
        self.tracker.update_item(
            item_name,
            quantity=int(self.inventory_quantity.get()) if self.inventory_quantity.get() else None,
            price=float(self.inventory_price.get()) if self.inventory_price.get() else None,
            image_path=self.inventory_image_path.get() if self.inventory_image_path.get() else None,
            year=self.inventory_year.get() if self.inventory_year.get() else None,
            location=self.inventory_location.get() if self.inventory_location.get() else None
        )
        self.inventory_tree.item(selected_item, values=(item_name, self.inventory_category.get(), self.inventory_quantity.get(), self.inventory_price.get(), self.inventory_image_path.get(), self.inventory_year.get(), self.inventory_location.get()))

    def add_wanted_item(self):
        item = CollectionItem(
            name=self.wanted_name.get(),
            category=self.wanted_category.get(),
            quantity=int(self.wanted_quantity.get()),
            price=float(self.wanted_price.get()),
            image_path=self.wanted_image_path.get(),
            year=self.wanted_year.get(),
            location=self.wanted_location.get()
        )
        self.tracker.add_wanted_item(item)
        self.wanted_tree.insert('', 'end', values=(item.name, item.category, item.quantity, item.price, item.image_path, item.year))

    def remove_wanted_item(self):
        selected_item = self.wanted_tree.selection()[0]
        item_name = self.wanted_tree.item(selected_item, 'values')[0]
        self.tracker.remove_wanted_item(item_name)
        self.wanted_tree.delete(selected_item)

    def update_wanted_item_price(self):
        selected_item = self.wanted_tree.selection()[0]
        item_name = self.wanted_tree.item(selected_item, 'values')[0]
        new_price = self.tracker.update_wanted_item_price(item_name)
        self.wanted_tree.item(selected_item, values=(item_name, self.wanted_category.get(), self.wanted_quantity.get(), new_price, self.wanted_image_path.get(), self.wanted_year.get()))

    def add_sell_item(self):
        item = CollectionItem(
            name=self.sell_name.get(),
            category=self.sell_category.get(),
            quantity=int(self.sell_quantity.get()),
            price=float(self.sell_price.get()),
            image_path=self.sell_image_path.get(),
            year=self.sell_year.get(),
            location=self.sell_location.get()
        )
        threshold = float(self.sell_threshold.get())
        self.tracker.add_sell_item(item, threshold)
        self.sell_tree.insert('', 'end', values=(item.name, item.category, item.quantity, item.price, item.image_path, item.year, item.location, threshold))

    def remove_sell_item(self):
        selected_item = self.sell_tree.selection()[0]
        item_name = self.sell_tree.item(selected_item, 'values')[0]
        self.tracker.remove_sell_item(item_name)
        self.sell_tree.delete(selected_item)

    def check_sell_item_price(self):
        selected_item = self.sell_tree.selection()[0]
        item_name = self.sell_tree.item(selected_item, 'values')[0]
        current_price = self.tracker.check_sell_item_price(item_name)
        self.sell_tree.item(selected_item, values=(item_name, self.sell_category.get(), self.sell_quantity.get(), current_price, self.sell_image_path.get(), self.sell_year.get(), self.sell_location.get(), self.sell_threshold.get()))