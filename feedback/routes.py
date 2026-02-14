# Testgarden/feedback/routes.py
from flask import render_template, request, flash, redirect, url_for
from . import feedback_bp   # blueprint wordt uit __init__.py gehaald
import csv
import os


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
            "reflectie": request.form.get("reflectie", "")
        }

        print("Feedback ontvangen:", data)  # console logging

        # --- CSV OPSLAAN ---
        csv_path = os.path.join(os.path.dirname(__file__), "feedback_data.csv")

        write_header = not os.path.exists(csv_path)

        with open(csv_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=data.keys())

            if write_header:
                writer.writeheader()

            writer.writerow(data)

        # --- FEEDBACK MELDING ---
        flash("Dankjewel voor je feedback! 🌱", "success")
        return redirect(url_for("feedback.feedback_form"))

    return render_template("feedback.html")

