# Testgarden/users/utils.py

from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            flash("Je moet eerst inloggen.", "error")
            return redirect(url_for("users.login"))
        return view(*args, **kwargs)
    return wrapper
