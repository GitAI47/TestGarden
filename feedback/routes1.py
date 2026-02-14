# Testgarden/feedback/routes.py
from flask import render_template, request, flash, redirect, url_for
from . import feedback_bp   # <— gebruik de blueprint uit __init__.py


@feedback_bp.route("/", methods=["GET", "POST"])
def feedback_form():
    if request.method == "POST":
        data = {
            "impressie": request.form.get("impressie", ""),
            "gebruik": request.form.get("gebruik", ""),
            "inhoud": request.form.get("inhoud", ""),
            "functionaliteit": request.form.get("functionaliteit", ""),
            "vormgeving": request.form.get("vormgeving", ""),
            "suggesties": request.form.get("suggesties", ""),
            "reflectie": request.form.get("reflectie", ""),
        }

        print("Feedback ontvangen:", data)  # later: database/mail/logfile

        flash("Dankjewel voor je feedback! 🌱", "success")
        return redirect(url_for("feedback.feedback_form"))

    return render_template("feedback.html")
