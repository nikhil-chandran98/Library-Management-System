# auth.py
import sqlite3
import hashlib
import getpass
import sys


conn = sqlite3.connect("Library.db")
c = conn.cursor()



def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def sign_up():
    print("\n--- Sign Up ---")
    name = input("Enter your full name: ").strip()
    if not name:
        print("Error: Name cannot be empty.")
        return

    username = input("Choose a username: ").strip()
    if not username:
        print("Error: Username cannot be empty.")
        return

    password = getpass.getpass("Choose a password: ").strip()
    if len(password) < 4:
        print("Error: Password must be at least 4 characters long.")
        return

    if password != getpass.getpass("Confirm password: ").strip():
        print("Error: Passwords do not match.")
        return

    try:
        c.execute(
            "INSERT INTO USERS (name, username, password_hash) VALUES (?, ?, ?)",
            (name, username, hash_password(password))
        )
        conn.commit()
        print(f"Success! Account created for {name} (@{username}). You can now sign in.")
    except sqlite3.IntegrityError:
        print(f"Error: The username '{username}' is already taken.")

def sign_in():
    """Returns (user_id, name, username) if successful, or None if failed."""
    print("\n--- Sign In ---")
    username = input("Username: ").strip()
    password = getpass.getpass("Password: ").strip()

    c.execute(
        "SELECT id, name, username FROM USERS WHERE username = ? AND password_hash = ?",
        (username, hash_password(password))
    )
    user = c.fetchone()

    if user:
        print(f"\nWelcome back, {user[1]}!")
        return user  # Returns a tuple: (id, name, username)
    else:
        print("\nError: Invalid username or password.")
        return None

def authenticate():
    """Runs the auth menu and returns (user_id, name, username) once logged in."""
    
    while True:
        print("\n=== Sign/Sign Up  ===")
        print("1. Sign In")
        print("2. Sign Up")
        print("3. Exit")
        
        choice = input("Select an option (1-3): ").strip()
        
        if choice == "1":
            user = sign_in()
            if user:
                return user  # Passes (id, name, username) to your main program
        elif choice == "2":
            sign_up()
        elif choice == "3":
            print("Goodbye!")
            conn.close()
            sys.exit(0)
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")