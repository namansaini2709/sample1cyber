import sqlite3
import os
import ssl

# Enable TLS for SQLite
conn = sqlite3.connect(DB_PATH, ssl=ssl.CreateDefaultContext())
