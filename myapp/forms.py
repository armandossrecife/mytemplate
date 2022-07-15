from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField, SelectField
from wtforms.validators import NumberRange, Length, EqualTo, Email, DataRequired, ValidationError
from myapp.dao import User
from wtforms.fields.html5 import DateField, TimeField

class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')

    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

class RepositoryForm(FlaskForm):
    name = StringField(label='Repository Name:', validators=[Length(min=2, max=30), DataRequired()])
    link = StringField(label='Repository Link:', validators=[Length(min=2, max=500), DataRequired()])
    submit = SubmitField(label='New')

class VeiculoForm(FlaskForm):
    placa = StringField(label='Placa do Veiculo:', validators=[Length(min=2, max=20), DataRequired()])
    marca = StringField(label='Marca do Veiculo:', validators=[Length(min=2, max=100), DataRequired()])
    modelo = StringField(label='Modelo do Veiculo:', validators=[Length(min=2, max=100), DataRequired()])
    carga = IntegerField(label='Carga do Veiculo:', validators=[NumberRange(min=1, max=50000), DataRequired()])
    tipo = IntegerField(label='Tipo do Veiculo:', validators=[NumberRange(min=1, max=100), DataRequired()])
    submit = SubmitField(label='New')

class MotoristaForm(FlaskForm):
    cpf = StringField(label='CPF do Motorista:', validators=[Length(min=2, max=20), DataRequired()])
    nome = StringField(label='Nome do Motorista:', validators=[Length(min=2, max=100), DataRequired()])
    data_nascimento = StringField(label='Data de Nascimento:')
    telefone = StringField(label='Telefone do Motorista:', validators=[Length(min=8, max=20), DataRequired()])
    categoria = IntegerField(label='Categoria do Motorista:', validators=[NumberRange(min=1, max=100), DataRequired()])
    submit = SubmitField(label='New')
    def load_content(self, cpf, nome, data_nascimento, telefone, categoria):
        self.cpf.data = cpf
        self.nome.data = nome
        self.data_nascimento.data = data_nascimento
        self.telefone.data = telefone
        self.categoria.data = categoria

class AlocarVeiculoForm(FlaskForm):
    owner_veiculo = SelectField(u'Veiculo:')
    owner_motorista = SelectField(u'Motorista:')
    origem = StringField(label='Origem', validators=[Length(min=2, max=1000), DataRequired()])
    latitude_origem = StringField(label='Latitude da Origem', validators=[Length(min=1, max=100), DataRequired()])
    longitude_origem = StringField(label='Longitude da Origem', validators=[Length(min=1, max=100), DataRequired()])
    destino = StringField(label='Destino da entrega', validators=[Length(min=2, max=1000), DataRequired()])
    latitude_destino = StringField(label='Latitude do Destino', validators=[Length(min=1, max=100), DataRequired()])
    longitude_destino = StringField(label='Longitude do Destino', validators=[Length(min=1, max=100), DataRequired()])
    carga = StringField(label='Peso da carga', validators=[Length(min=1, max=100), DataRequired()])
    data_entrega = StringField(label='Data da entrega', validators=[Length(min=2, max=50), DataRequired()])
    data_entrega2 = DateField('Data', format='%d-%m-%Y')
    hora_entrega2  = TimeField('Time', format='%H:%M')
    submit = SubmitField(label='New')
    def load_content(self, veiculos, motoristas):
        self.owner_veiculo.choices = veiculos
        self.owner_motorista.choices = motoristas