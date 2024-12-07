"""
main.py

Entry point for the Collection Tracker application.
"""

import os
import tkinter as tk
from dotenv import load_dotenv
from collection_tracker import CollectionTracker
from collection_app import CollectionApp

def main():
    # Load environment variables from .env file
    load_dotenv()

    # Database connection parameters
    host = os.getenv("DB_HOST")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    database = os.getenv("DB_NAME")
    port = os.getenv("DB_PORT")

    # Initialize the collection tracker
    tracker = CollectionTracker(host, user, password, database, port)

    # Initialize the tkinter root window
    root = tk.Tk()

    # Create the CollectionApp with the tracker and root window
    app = CollectionApp(root, tracker)

    # Start the tkinter main loop
    root.mainloop()

    # Close the database connection when the app is closed
    tracker.close()

if __name__ == "__main__":
    main()
