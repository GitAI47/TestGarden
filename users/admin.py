from functools import wraps
from flask import session, redirect, url_for, flash

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get("role") != "admin":
            flash("Alleen admins mogen dit.", "danger")
            return redirect(url_for("core.index"))
        return f(*args, **kwargs)
    return wrapper
