## Rotas, links
from flask import render_template, url_for, redirect
from fakepintereskcerto import app, database, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from fakepintereskcerto.forms import FormLogin, FormCriarConta, FormFoto
from fakepintereskcerto.models import Usuario, Foto
import os
from werkzeug.utils import secure_filename

@app.route('/', methods=['GET','POST'])
def homepage():
    formlogin = FormLogin()
    if formlogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formlogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, formlogin.senha.data): ##Aqui ele compara senha criptografada, o Bcrypt acessa a senha verdadeira atraves da encriptada e compara com a senha passada pelo usuario no formlogin
            login_user(usuario)
            return redirect(url_for("perfil",id_usuario=usuario.id))
    return render_template('homepage.html',form=formlogin)


@app.route('/criarconta', methods=['GET','POST'])
def criarconta():
    form_criarconta = FormCriarConta()
    if form_criarconta.validate_on_submit():
        senha = bcrypt.generate_password_hash(form_criarconta.senha.data).decode('utf-8')
        usuario =  Usuario(username=form_criarconta.username.data,
                           email=form_criarconta.email.data,senha=senha)
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario,remember=True)
        return redirect(url_for("perfil",id_usuario=usuario.id))
    return render_template('criarconta.html',form=form_criarconta)


@app.route('/perfil/<id_usuario>',methods=['GET','POST']) ## decorator serve parar adicionar novos atributos para uma função
@login_required
def perfil(id_usuario):
    if int(id_usuario) == int(current_user.id):
        ## o usuario ta vendo o perfil dele
        form_foto = FormFoto()
        if form_foto.validate_on_submit():
            arquivo = form_foto.foto.data
            nome_seguro = secure_filename(arquivo.filename) ## Altera o nome do arquivo para evitar erros de leitura de nomes no servidor
            ## Salvar o arquivo na pasta post
            
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)), 
                      app.config["UPLOAD_FOLDER"], nome_seguro)
            arquivo.save(caminho)
            ## registrar o arquivo no banco de dados, o nome a ser salvo é o nome seguro
            foto = Foto(imagem=nome_seguro , id_usuario=int(current_user.id)) ##cria o registro da imagem no banco
            database.session.add(foto)
            database.session.commit()
        return render_template("perfil.html", usuario=current_user, form=form_foto)
    else:
        usuario = Usuario.query.get(int(id_usuario))
        return render_template('perfil.html',usuario=usuario, form=None)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))

@app.route('/feed')
def feed():
    fotos = Foto.query.order_by(Foto.data_criação.desc()).all() ##[aqui eu estou solicitando pegar todas as fotos para jogar para dentro do html. se eu quisesse pegar as 10 peimeiras por ex, eu só fazer assim = .all()[10]
    return render_template("feed.html", fotos=fotos)