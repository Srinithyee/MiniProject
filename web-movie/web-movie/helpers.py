import os
import sqlite3


from flask import redirect, render_template, request, session
from functools import wraps


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user-id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def inr(value):
    """Format value as INR."""
    return f"${value:,.2f}"


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData