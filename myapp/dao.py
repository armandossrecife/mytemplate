from myapp import db, login_manager
from myapp import my_bcrypt
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    repositories = db.relationship('Repository', backref='owned_user', lazy=True)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = my_bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return my_bcrypt.check_password_hash(self.password_hash, attempted_password)

class Repository(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=False)
    link = db.Column(db.String(length=1024), nullable=False, unique=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    analysis_date = db.Column(db.DateTime, nullable=True, default=None)
    analysed = db.Column(db.Integer(), nullable=True, default=0)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
    
    def __repr__(self):
        return f'Repository {self.name}'

class Veiculo(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    placa = db.Column(db.String(length=20), nullable=False, unique=False)
    marca = db.Column(db.String(length=100), nullable=False, unique=False)
    modelo = db.Column(db.String(length=100), nullable=False, unique=False)
    carga = db.Column(db.Integer(), nullable=True, default=0)
    tipo = db.Column(db.Integer(), nullable=True, default=0)
    def __repr__(self):
        return f'Repository {self.placa}'

class Motorista(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    cpf = db.Column(db.String(length=11), nullable=False, unique=False)
    nome = db.Column(db.String(length=100), nullable=False, unique=False)
    telefone = db.Column(db.String(length=11), nullable=False, unique=False)
    categoria = db.Column(db.Integer(), nullable=True, default=0)
    data_nascimento = db.Column(db.DateTime, nullable=True)
    def __repr__(self):
        return f'Motorista {self.cpf}'

class Veiculo_Alocado(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    owner_veiculo = db.Column(db.Integer(), db.ForeignKey('veiculo.id'))
    owner_motorista = db.Column(db.Integer(), db.ForeignKey('motorista.id'))
    origem = db.Column(db.String(length=1024), nullable=False, unique=False)
    latitude_origem = db.Column(db.Float(), nullable=True, default=0)
    longitude_origem = db.Column(db.Float(), nullable=True, default=0)
    destino = db.Column(db.String(length=1024), nullable=False, unique=False)
    latitude_destino = db.Column(db.Float(), nullable=True, default=0)
    longitude_destino = db.Column(db.Float(), nullable=True, default=0)
    carga = db.Column(db.Float(), nullable=True, default=0)
    data_entrega = db.Column(db.DateTime, nullable=False, default=datetime.now)
    def __repr__(self):
        return f'Repository {self.id}'

class Users:
    def insert_user(self, user):
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            print(f'Error during insert user - {e}')

    def query_user_by_username(self, p_username):
        user = User.query.filter_by(username=p_username).first()
        return user
    def query_user_by_id(self, p_id):
        user = User.query.filter_by(id=p_id).first()
        return user
    
    def list_all_users(self):
        return User.query.all()

class Repositories:
    def insert_repository(self, repository):
        try:
            db.session.add(repository)
            db.session.commit()
        except Exception as e:
            print(f'Error during insert repository - {e}')

    def query_repository_by_name(self, p_name):
        repository = Repository.query.filter_by(name=p_name).first()
        return repository

    def query_repository_by_id(self, p_id):
        repository = Repository.query.filter_by(id=p_id).first()
        return repository
    
    def list_all_repositories(self):
        return Repository.query.all()

    def query_repositories_by_user_id(self, user_id):
        list_repositories = Repository.query.filter_by(owner=user_id).all()
        return list_repositories

    def update_repository_by_name(self, name, user_id, analysed):
        analysis_date = datetime.now()
        repository = Repository.query.filter_by(name=name, owner=user_id).first()
        repository.analysis_date = analysis_date
        repository.analysed = analysed
        db.session.add(repository)
        db.session.commit()

    def query_repositories_by_name_and_user_id(self, repository_name, user_id):
        list_repositories_by_user_id = Repository.query.filter_by(owner=user_id).all()
        list_repositories = []
        for each in list_repositories_by_user_id:
            if each.name == repository_name:
                list_repositories.append(each)

        return list_repositories

class Veiculos:
    # insere novo veiculo
    def insert_veiculo(self, veiculo):
        try:
            db.session.add(veiculo)
            db.session.commit()
        except Exception as e:
            print(f'Error during insert veiculo - {e}')
    
    # procura veiculo por placa
    def query_veiculo_by_placa(self, p_placa):
        veiculo = Veiculo.query.filter_by(placa=p_placa).first()
        return veiculo

    # procura veiculo por id
    def query_veiculo_by_id(self, p_id):
        veiculo = Veiculo.query.filter_by(id=p_id).first()
        return veiculo
    
    # lista todos os veiculos
    def list_all_veiculos(self):
        return Veiculo.query.all()

class Motoristas:
    # insere novo motorista
    def insert_motorista(self, motorista):
        try:
            db.session.add(motorista)
            db.session.commit()
        except Exception as e:
            print(f'Error during insert motorista - {e}')

    # atualiza dados do motorista
    def update_motorista(self, id, novos_dados_motorista):
        try:
            motorista_to_update = self.query_motorista_by_id(id)
            print(f'Dados originais: {motorista_to_update.id, motorista_to_update.cpf, motorista_to_update.nome, motorista_to_update.data_nascimento, motorista_to_update.telefone, motorista_to_update.categoria}')
            motorista_to_update.cpf = novos_dados_motorista.cpf
            motorista_to_update.nome = novos_dados_motorista.nome
            motorista_to_update.data_nascimento = novos_dados_motorista.data_nascimento
            motorista_to_update.telefone = novos_dados_motorista.telefone
            motorista_to_update.categoria = novos_dados_motorista.categoria
            print(f'Novos dados: {motorista_to_update.id, motorista_to_update.cpf, motorista_to_update.nome, motorista_to_update.data_nascimento, motorista_to_update.telefone, motorista_to_update.categoria}')
            db.session.commit()
            print(f'Foi feito o commit!')
        except Exception as e:
            raise Exception(f'Error during update motorista - {e}')

    # procura motorista por cpf
    def query_motorista_by_cpf(self, p_cpf):
        motorista = Motorista.query.filter_by(cpf=p_cpf).first()
        return motorista

    # procura motorista por id
    def query_motorista_by_id(self, p_id):
        motorista = Motorista.query.filter_by(id=p_id).first()
        return motorista
    
    # lista todos os motoristas
    def list_all_motoristas(self):
        return Motorista.query.all()

class Veiculos_Alocados:
    # Aloca um veiculo a um motorista
    def insert_alocacao(self, alocacao):
        try:
            db.session.add(alocacao)
            db.session.commit()
        except Exception as e:
            print(f'Error during insert alocacao - {e}')
    
    # procura alocacoes por veiculo 
    def query_alocacoes_by_veiculo(self, p_id_veiculo):
        alocacoes = Veiculo_Alocado.qyery.filter_by(owner_veiculo=p_id_veiculo).all()
        return alocacoes

    # procura alocacoes por motorista 
    def query_alocacoes_by_motorista(self, p_id_motorista):
        alocacoes = Veiculo_Alocado.qyery.filter_by(owner_motorista=p_id_motorista).all()
        return alocacoes

    # procura alocacao por id
    def query_alocacao_by_id(self, p_id):
        alocacao = Veiculo_Alocado.query.filter_by(id=p_id).first()
        return alocacao
    
    # lista todas as alocacoes
    def list_all_alocacoes(self):
        return Veiculo_Alocado.query.all()