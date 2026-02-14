from flask import render_template, redirect, url_for, request, flash, session
from sqlalchemy.exc import IntegrityError
from . import users_bp
from database.models import db, User
from users.admin import admin_required



@users_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        # simpele validatie
        if not username or not email or not password:
            flash("Vul alle velden in.", "error")
            return redirect(url_for("users.register"))

        # checks vóór commit (voorkomt 500)
        if User.query.filter_by(username=username).first():
            flash("Gebruikersnaam bestaat al.", "error")
            return redirect(url_for("users.register"))

        if User.query.filter_by(email=email).first():
            flash("E-mailadres is al geregistreerd.", "error")
            return redirect(url_for("users.register"))

        user = User(username=username, email=email)
        user.set_password(password)

        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("Deze gebruiker bestaat al (username/email).", "error")
            return redirect(url_for("users.register"))

        flash("Registratie succesvol! Log nu in.", "success")
        return redirect(url_for("users.login"))

    return render_template("register.html")


@users_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            flash("Ongeldige login.", "error")
            return redirect(url_for("users.login"))

        session["user_id"] = user.id
        session["username"] = user.username
        session["role"] = getattr(user, "role", "student")
        flash("Je bent succesvol ingelogd!", "success")

        next_url = request.args.get("next")
        return redirect(next_url or url_for("core.index"))


    return render_template("login.html")


@users_bp.route("/logout")
def logout():
    session.clear()
    flash("Je bent uitgelogd.", "success")
    return redirect(url_for("core.index"))


@users_bp.route("/admin/make_teacher/<username>")
@admin_required
def make_teacher(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash("Gebruiker niet gevonden", "warning")
        return redirect(url_for("core.index"))

    user.role = "teacher"
    db.session.commit()

    flash(f"{username} is nu docent.", "success")
    return redirect(url_for("core.index"))

@users_bp.route("/admin")
@admin_required
def admin_panel():
    users = User.query.order_by(User.username.asc()).all()
    return render_template("admin.html", users=users)


@users_bp.route("/admin/set_role/<username>/<role>")
@admin_required
def admin_set_role(username, role):
    if role not in ("student", "teacher", "admin"):
        flash("Ongeldige rol.", "warning")
        return redirect(url_for("users.admin_panel"))

    user = User.query.filter_by(username=username).first()
    if not user:
        flash("Gebruiker niet gevonden.", "warning")
        return redirect(url_for("users.admin_panel"))

    user.role = role
    db.session.commit()
    flash(f"{username} is nu {role}.", "success")
    return redirect(url_for("users.admin_panel"))

