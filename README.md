## 1. Installing requirement

Prepare o ambiente virtual para logo depois rodar a aplicação flask principal. 

Virtual environment
```bash
python3 -m venv venv
```

Activate virtual environment
```bash
source venv/bin/activate
```

Install requirements
```bash
pip3 install -r requirements.txt
```

## 2. Run application

To run the application, it is necessary to install all the modules and extensions mentioned above. In addition, you need to set the following environment variables:

For the Posix environment:
```bash
# Shell 1
export FLASK_APP=run.py && export FLASK_ENV=development
```
More details at [CLI Flask](https://flask.palletsprojects.com/en/2.0.x/cli/)

Run the application via CLI:
```bash
# Shell 1
flask run --host=0.0.0.0 --port=5000
```

## 3. Directories and file structure

```
.
├── logs
│   ├── my_app.log
|   ├── ...
|
├── myapp
│   ├── __init__.py
│   ├── authentication.py
│   ├── dao.py
│   ├── forms.py
│   ├── myapp.db
│   ├── recursos.py
│   ├── static
│   │   ├── css
│   │   │   ├── grid.css
│   │   │   ├── ...
|   |   |
│   │   ├── img
│   │   │   ├── anonymous2.png
│   │   │   ├── ...
|   |   |
│   │   ├── infobox.js
│   │   ├── mapa.css
│   │   ├── mapa.js
│   │   ├── mapas.js
│   │   ├── mapsStores.json
│   │   └── markerclusterer.js
│   ├── templates
│   │   ├── authenticate
│   │   │   ├── home.html
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   ├── base.html
│   │   ├── recursos
│   │   │   ├── alocar_veiculo.html
│   │   │   ├── mapa.html
│   │   │   ├── mapa_lojas.html
│   │   │   ├── motorista.html
│   │   │   ├── myapp.html
│   │   │   ├── pagination_motoristas.html
│   │   │   ├── pagination_veiculos.html
│   │   │   ├── pagination_veiculos_alocados.html
│   │   │   ├── veiculo.html
│   │   │   └── veiculos.html
│   │   └── user
│   │       └── pagination.html
│   └── users.py
├── requirements.txt
└── run.py
```

## 4. Main Features
- Autenticação/Autorização
- Registrar novo usuário
- Alocação de Veículos
- Veículos
- Motorista
- Manutenções
- Mapas
- Alertas
- Abastecimento
- Multas
- Relatórios

## 5. TODO
- Formatação de I/O
- Upload de imagem
- Download de imagem
- Gerar PDF
- Gear QR Code
- Gerar Dashboard de Resumo