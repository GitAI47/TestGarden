
database initialiseren

Bash console
python

dan:

from app import create_app
from database.models import db

app = create_app()
with app.app_context():
    db.create_all()
    


Rol admin toewijzen op de server omgeving
Bash console
python

dan:


from app import create_app
from database.models import db, User

app = create_app()
app.app_context().push()

u = User.query.filter_by(username="Jouw_Naam").first()  # verander naam indien nodig
print("Huidige rol:", u.role)

u.role = "admin"
db.session.commit()

print("Nieuwe rol:", u.role)
