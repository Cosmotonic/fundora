# core.py
import sqlite3  # This is Python’s built-in module for SQLite

def verify_user(email, password):
    # 🔌 Connect to the SQLite database file

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()  # This lets us run SQL commands

    # 🔍 SQL query: find the user where email and password match
    cursor.execute("""
        SELECT name, address, phone, age FROM users
        WHERE email = ? AND password = ?
    """, (email, password))  # The values are safely inserted using ?, not string formatting

    row = cursor.fetchone()  # Get the first matching result, or None if no match
    #print("DEBUG: Row result =", row)
    conn.close()  # Always close the connection when done

    # ✅ If we found a matching user, return their info
    if row:
        return {
            "name"      : row[0],        # First column = name
            "email"     : email,        # We already know the email
            "address"   : row[1],      # Second column = address
            "phone"     : row[2],  # ← NEW
            "age"       : row[3]  # ← NEW
        }
        

    # ❌ No matching user found — return None
    return None




######################################################
######################################################
######################################################

def calculate_monthly_payment(principal, annual_rate, years):
    rate = annual_rate / 100 / 12
    months = years * 6 # month pr year, 20 by "mistake" here
    if rate == 0:
        return principal / months
    return principal * rate / (1 - (1 + rate) ** -months)

