## Estrutura banco de dados
from fakepintereskcerto import database, login_manager
from datetime import datetime
from flask_login import UserMixin



@login_manager.user_loader ## To dizendo que a função que carrega um usuario, ele chamou essa sintaxe de decorator, diz que essa função é parte do login manager. Função que carrga usuario
def load_usuario(id_usuario):
    return  Usuario.query.get(int(id_usuario))


class Usuario(database.Model, UserMixin): ## ser uma subclasse do database.Model é uma classe que o DB vai entender 
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email =  database.Column(database.String, nullable=False,unique=True)
    senha = database.Column(database.String, nullable=False)
    fotos = database.relationship("Foto", backref='usuario') ## o back ref diz que o contrario tambem é verdadeiro, no caso, assim como a classe usuario pode acessar a classe foto, o contratio tambem pode acontecer


class Foto(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    imagem = database.Column(database.String, default='default.png')
    data_criação = database.Column(database.DateTime, nullable=False, default=datetime.utcnow())
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    