##Formularios
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField ##campo de texto, senha e botão para enviar
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from fakepintereskcerto.models import Usuario

class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(),Email()]) 
    senha = PasswordField('Senha',validators=[DataRequired()])
    botao_confirmacao = SubmitField('Fazer Login')
    
    def validate_email(self,email):  ## Na linha abaixo, Usuario é uma tabela do DB, e estou filtrando ela onde na coluna email, o email é igual ao recebido no parametro email. retorna uma lista dos emails e o first pega o primeiro elemento para verificar se tem algum email igual já cadastrado
        usuario = Usuario.query.filter_by(email=email.data).first()   ##quando acessa a database por outr dado que nao seja o id tem que ser com o filter by, senão pode ser com o get
        if not usuario:   ## na linha acima, o primeiro email é o recebido pela função e o segundo são as infos do DB
            raise ValidationError("Usuário inxistente. Crie uma conta para continuar")
    
    def validade_senha(self,senha):
        usuario = Usuario.query

class FormCriarConta(FlaskForm):
    email = StringField("E-mail",validators=[DataRequired(),Email()])
    username = StringField("Nome de Usuário", validators=[DataRequired()])
    senha = PasswordField("Senha", validators=[DataRequired(),Length(6, 20)])
    confirmacaosenha = PasswordField("Confirmação de senha",validators=[DataRequired(),EqualTo('senha')])
    botao_confirmacao = SubmitField('Criar Conta')

    def validate_email(self,email):  ## Na linha abaixo, Usuario é uma tabela do DB, e estou filtrando ela onde na coluna email, o email é igual ao recebido no parametro email. retorna uma lista dos emails e o first pega o primeiro elemento para verificar se tem algum email igual já cadastrado
        usuario = Usuario.query.filter_by(email=email.data).first()   ##quando acessa a database por outr dado que nao seja o id tem que ser com o filter by, senão pode ser com o get
        if usuario:   ## na linha acima, o primeiro email é o recebido pela função e o segundo são as infos do DB
            raise ValidationError("Email já cadastrado, faça login para continuar.")
        
class FormFoto(FlaskForm):
    foto = FileField("Foto", validators=[DataRequired()])
    botao_confirmacao = SubmitField("Enviar")
    