import os
from flask import Flask
from database.models import db
from core.menu import get_all_menus
from datetime import datetime


def create_app():
    app = Flask(__name__)

    # -------------------------
    # CONFIGURATIE
    # -------------------------
    app.config['SECRET_KEY'] = 'iets-geheims'

    os.makedirs(app.instance_path, exist_ok=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'testgarden.db')

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    # -------------------------
    # DATABASE INITIALISEREN
    # -------------------------
    db.init_app(app)

    # -------------------------# BLUEPRINTS IMPORTEREN
    # -------------------------
    from core import core_bp
    from users import users_bp
    from exercises import exercises_bp
    from feedback import feedback_bp
    from instructions import instructions_bp
    from tools import tools_bp
    from scripts import scripts_bp
    # -------------------------
    # BLUEPRINTS REGISTREREN
    # (met duidelijke tuinbed-paden)
    # ---
    # ----------------------
    app.register_blueprint(core_bp, url_prefix="/")
    app.register_blueprint(feedback_bp, url_prefix="/feedback")
    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(exercises_bp, url_prefix="/exercises")
    app.register_blueprint(instructions_bp, url_prefix="/instructions")
    app.register_blueprint(tools_bp, url_prefix="/tools")
    app.register_blueprint(scripts_bp, url_prefix="/scripts")
    # -------------------------
    # MENU IN ELKE TEMPLATE
    # -------------------------
    from flask import session

    
    @app.context_processor
    def inject_menus():
        logged_in = "user_id" in session
        return {
            "menus": get_all_menus(logged_in=logged_in, username=session.get("username")),
            "current_role": session.get("role", "student"),
        }



    @app.context_processor
    def inject_year():
        return {'year': datetime.now().year}



    return app


# -------------------------
# START APP
# -------------------------
app = create_app()

# print(app.url_map)


if __name__ == "__main__":
    app.run(debug=True)
