from myapp import app
from flask import render_template
from flask_login import login_required
from myapp.dao import Users
import logging
from flask_paginate import Pagination, get_page_args

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S', filename='./logs/my_app_main.log', filemode='w')

# Collection to manipulate users in data base
usersCollection = Users()

users = usersCollection.list_all_users()

def get_users(offset=0, per_page=10):
    return users[offset: offset + per_page]

@app.route('/users')
def pagination_page():
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    total = len(users)
    pagination_users = get_users(offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    return render_template('user/pagination.html', users=pagination_users, page=page, per_page=per_page, pagination=pagination)
