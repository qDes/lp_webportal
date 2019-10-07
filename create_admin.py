from getpass import getpass
import sys

from app import create_app
from app.db import db
from app.user.models import User

app = create_app()

with app.app_context():
    username = input("Enter username:")

    if User.objects(username=username):
        print(f"{username} already exists.")
        sys.exit(0)

    password1 = getpass("Enter password:")
    password2 = getpass("Repeat password:")

    if not password1 == password2:
        print("Fuckup with passwords")
        sys.exit(0)

    new_user = User(username=username, role='admin')
    new_user.set_password(password1)
    new_user.save()
    print(f"New user {User} added.")
