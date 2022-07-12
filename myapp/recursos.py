from myapp import app
from unicodedata import category
from flask import render_template, flash, url_for, redirect
from flask_login import login_required
from myapp.forms import  VeiculoForm, MotoristaForm, AlocarVeiculoForm
from myapp.dao import Veiculo, Veiculos, Motorista, Motoristas, Veiculo_Alocado, Veiculos_Alocados
import logging
from flask_paginate import Pagination, get_page_args
from datetime import datetime

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S', filename='./logs/my_app_main.log', filemode='w')

# Collection to manipulate recursos in data base
veiculosCollection = Veiculos()
motoristasCollection = Motoristas()
alocacoesCollection = Veiculos_Alocados()

veiculos = veiculosCollection.list_all_veiculos()
motoristas = motoristasCollection.list_all_motoristas()
alocacoes = alocacoesCollection.list_all_alocacoes()

def get_veiculos(offset=0, per_page=10, veiculos=veiculos):
    return veiculos[offset: offset + per_page]

def get_motoristas(offset=0, per_page=10, motoristas=motoristas):
    return motoristas[offset: offset + per_page]

def get_alocacoes(offset=0, per_page=10, alocacoes=alocacoes):
    return alocacoes[offset: offset + per_page]

@app.route('/myapp')
@login_required
def myapp_page():
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    alocacoes = alocacoesCollection.list_all_alocacoes()
    total = len(alocacoes)
    pagination_alocacoes = get_alocacoes(offset=offset, per_page=per_page, alocacoes=alocacoes)
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    return render_template('recursos/pagination_veiculos_alocados.html', veiculos=pagination_alocacoes, page=page, per_page=per_page, pagination=pagination)

# Lista os veiculos paginados cadastradaos
@app.route('/veiculos')
@login_required
def veiculos_page():
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    veiculos = veiculosCollection.list_all_veiculos()
    total = len(veiculos)
    print(f'Total de veiculos: {total}')
    pagination_veiculos = get_veiculos(offset=offset, per_page=per_page, veiculos=veiculos)
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    return render_template('recursos/pagination_veiculos.html', veiculos=pagination_veiculos, page=page, per_page=per_page, pagination=pagination)

# Checa se o veiculo ja foi cadastrado
def exist_veiculo(placa):
    veiculo = veiculosCollection.query_veiculo_by_placa(placa)
    if veiculo is not None:
        return True
    return False

# Form para inserir novo veiculo
@app.route('/insereveiculo', methods=['GET', 'POST'])
@login_required
def insere_veiculo():
    form = VeiculoForm()
    if form.validate_on_submit():
        placa = form.placa.data  
        marca = form.marca.data
        modelo = form.modelo.data
        carga = form.carga.data
        tipo = form.tipo.data
        if not exist_veiculo(placa):
            veiculo = Veiculo(placa=placa, marca=marca, modelo=modelo, carga=carga, tipo=tipo)
            veiculosCollection.insert_veiculo(veiculo)
            flash(f'Veiculo {veiculo.placa} salvo com sucesso!', category='success')
            # Lista veiculos atualizados
            return redirect(url_for('veiculos_page'))
        flash('Veiculo already exist!', category='danger')

    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with new veiculo: {err_msg}', category='danger')

    return render_template('recursos/veiculo.html', form=form)  


# Lista os motoristas cadastrados
@app.route('/motoristas')
@login_required
def motoristas_page():
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    motoristas = motoristasCollection.list_all_motoristas()
    total = len(motoristas)
    pagination_motoristas = get_motoristas(offset=offset, per_page=per_page, motoristas=motoristas)
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    return render_template('recursos/pagination_motoristas.html', motoristas=pagination_motoristas, page=page, per_page=per_page, pagination=pagination)

# Checa se o motorista ja foi cadastrado
def exist_motorista(cpf):
    motorista = motoristasCollection.query_motorista_by_cpf(cpf)
    if motorista is not None:
        return True
    return False

# todo: corrigir a funcao dummy
def convert_str_to_datetime(birthday):
    birthday = "2000-01-23 00:00:00"
    birthday_object = datetime.strptime(birthday, '%Y-%m-%d %H:%M:%S')
    return birthday_object

# Form para inserir novo motorista
@app.route('/inseremotorista', methods=['GET', 'POST'])
@login_required
def insere_motorista():
    form = MotoristaForm()
    if form.validate_on_submit():
        cpf = form.cpf.data
        nome = form.nome.data
        data_nascimento = convert_str_to_datetime(form.data_nascimento.data)
        telefone = form.telefone.data
        categoria = form.categoria.data

        if not exist_motorista(cpf):
            motorista = Motorista(cpf=cpf, nome=nome, telefone=telefone, data_nascimento=data_nascimento, categoria=categoria)
            motoristasCollection.insert_motorista(motorista)
            flash(f'Motorista {motorista.cpf} salvo com sucesso!', category='success')
            # Lista motoristas atualizados
            return redirect(url_for('motoristas_page'))
        flash('Motorista already exist!', category='danger')

    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with new motorista: {err_msg}', category='danger')

    return render_template('recursos/motorista.html', form=form)  

# todo: revisar a regra de negocio, pois um mesmo veiculo pode ser alocado varias vezes por um mesmo motorista em horarios e dias diferentes
# um veiculo é alocado para uma entrega
# Checa se o veiculo e o motorista ja foram associados antiormente
def exist_alocacao(id_veiculo, id_motorista, data_alocacao):
    alocacao = alocacoesCollection.query_alocacao_by_id(0)
    if alocacao is not None:
        return True
    return False

# todo: corrigir a funcao dummy
def convert_str_to_datetime_entrega(entrega):
    entrega = "2022-07-12 00:00:00"
    entrega_object = datetime.strptime(entrega, '%Y-%m-%d %H:%M:%S')
    return entrega_object

# Form para alocar veiculo a motorista
@app.route('/alocaveiculo', methods=['GET', 'POST'])
@login_required
def alocar_veiculo_page():
    form = AlocarVeiculoForm()
    if form.validate_on_submit():
        owner_veiculo = int(form.owner_veiculo.data)
        owner_motorista = int(form.owner_motorista.data)
        origem = form.origem.data
        latitude_origem = float(form.latitude_origem.data)
        longitude_origem = float(form.longitude_origem.data)
        destino = form.destino.data
        latitude_destino = float(form.latitude_destino.data)
        longitude_destino = float(form.longitude_destino.data)
        carga = float(form.carga.data)
        data_entrega = convert_str_to_datetime_entrega(form.data_entrega.data)

        if not exist_alocacao(owner_veiculo, owner_motorista, data_entrega):
            alocacao = Veiculo_Alocado(owner_veiculo=owner_veiculo, owner_motorista=owner_motorista,origem=origem,latitude_origem=latitude_origem,longitude_origem=longitude_origem,destino=destino,latitude_destino=latitude_destino,longitude_destino=longitude_destino,carga=carga,data_entrega=data_entrega)
            alocacoesCollection.insert_alocacao(alocacao)
            flash(f'Veiculo {owner_veiculo} alocado pelo motorista {owner_motorista} com sucesso!', category='success')
            # Lista de veiculos alocados
            return redirect(url_for('veiculos_alocados_page'))
        flash('Alocacao already exist!', category='danger')

    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with new alocacao: {err_msg}', category='danger')

    return render_template('recursos/alocar_veiculo.html', form=form)  

# Lista as alocacoes realizadas
@app.route('/alocacoes')
@login_required
def veiculos_alocados_page():
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    alocacoes = alocacoesCollection.list_all_alocacoes()
    total = len(alocacoes)
    pagination_alocacoes = get_alocacoes(offset=offset, per_page=per_page, alocacoes=alocacoes)
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    return render_template('recursos/pagination_veiculos_alocados.html', veiculos=pagination_alocacoes, page=page, per_page=per_page, pagination=pagination)