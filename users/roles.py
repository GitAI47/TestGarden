from functools import wraps
from flask import session, redirect, url_for, flash

def role_required(role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if "user_id" not in session:
                flash("Log eerst in.", "warning")
                return redirect(url_for("users.login"))

            current_role = session.get("role", "student")

            # Admin mag altijd
            if current_role == "admin":
                return f(*args, **kwargs)

            if current_role != role:
                flash("Geen toegang tot deze pagina.", "danger")
                return redirect(url_for("core.index"))

            return f(*args, **kwargs)
        return wrapper
    return decorator
