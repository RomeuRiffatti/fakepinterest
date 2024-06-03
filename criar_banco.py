from fakepintereskcerto import database, app
from fakepintereskcerto.models import Usuario, Foto
with app.app_context():
    database.create_all()