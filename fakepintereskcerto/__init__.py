from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://banco_fakepinterest_9wc5_user:HhGy23563Q5VCNPsnf9qwfbLFzmMDuIa@dpg-cpf32pjtg9os73b6rdng-a.oregon-postgres.render.com/banco_fakepinterest_9wc5"
app.config["SECRET_KEY"] = "354ith5b3bjvhsvgy8425tbnirug97842"
app.config['UPLOAD_FOLDER'] = "static/fotos_posts"
database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "homepage"  ##se um usuario nao estiver logado, para onde ele vai ser direcionado? 
from fakepintereskcerto import routes