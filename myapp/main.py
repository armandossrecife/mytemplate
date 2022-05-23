from myapp import app
from flask import render_template
from flask_login import login_required
from myapp.dao import Users
from GoogleNews import GoogleNews
import os, ssl
import logging
from flask_paginate import Pagination, get_page_args

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S', filename='./logs/my_app_main.log', filemode='w')

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

googlenews = GoogleNews(lang='en', region='US')

@app.context_processor
def inject_enumerate():
    return dict(enumerate=enumerate)

def extract(articles):
    title, desc, date, datetime, link, img, media, site = [], [], [], [], [], [], [], []
    print(f'Total de artigos: {len(articles)}')
    for i in range(len(articles)):
        my_articles = articles[i]

        title.append(my_articles['title'])
        desc.append(my_articles['desc'])
        date.append(my_articles['date'])
        datetime.append(my_articles['datetime'])
        link.append(my_articles['link'])
        img.append(my_articles['img'])
        media.append(my_articles['media'])
        site.append(my_articles['site'])
                
    my_list = zip(title, desc, date, datetime, link, img, media, site)
    return my_list

@app.route('/myapp')
@login_required
def myapp_page():
    googlenews.get_news('APPLE')
    articles_list = extract(googlenews.results())
    return render_template('user/myapp.html', articles_list=articles_list)
 
@app.route('/everything/<word>')
@login_required
def everything_page(word):
    googlenews.get_news(word)
    articles_list = extract(googlenews.results())
    return render_template('user/everything.html', articles_list=articles_list)

def get_news_per_page(articles, offset=0, per_page=10):
    title, desc, date, datetime, link, img, media, site = [], [], [], [], [], [], [], []
    for i in range(offset, offset+per_page):
        my_articles = articles[i]

        title.append(my_articles[0])
        desc.append(my_articles[1])
        date.append(my_articles[2])
        datetime.append(my_articles[3])
        link.append(my_articles[4])
        img.append(my_articles[5])
        media.append(my_articles[6])
        site.append(my_articles[7])
                
    my_list = zip(title, desc, date, datetime, link, img, media, site)
    return my_list

@app.route('/everything2/<word>')
@login_required
def everything_page2(word):
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    googlenews.get_news(word)
    articles_list = extract(googlenews.results())
    test_data = list(articles_list)
    total = len(test_data)
    pagination_news = get_news_per_page(test_data, offset=offset, per_page=per_page)
    print(pagination_news)
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    return render_template('user/everything2.html', articles_list=pagination_news, page=page, per_page=per_page, pagination=pagination)