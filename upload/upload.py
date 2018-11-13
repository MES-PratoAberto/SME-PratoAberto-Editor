# -*- coding: utf-8 -*-

import configparser
import flask_login
import os
import requests
import json
import db_functions
import cardapio_xml_para_dict

from werkzeug.utils import secure_filename
from flask import flash, redirect, render_template, request, url_for, Blueprint
from utils.utils import allowed_file, get_escolas

config = configparser.ConfigParser()
config.read('config/integracao.conf')
api = config.get('ENDPOINTS', 'PRATOABERTO_API')
_user = config.get('LOGIN', 'USER')
_password = config.get('LOGIN', 'PASSWORD')

users = {_user: {'password': _password}}

upload_app = Blueprint('upload_app', __name__)

@upload_app.route('/cria_terceirizada', methods=['GET'])
@flask_login.login_required
def cria_terceirizada():
    if request.method == "GET":
        quebras = db_functions.select_quebras_terceirizadas()
        editais = set([x[1] for x in quebras])
        tipo_unidade = set([x[0] for x in quebras])
        idade = set([x[2] for x in quebras])
        refeicao = set([x[3] for x in quebras])

        return render_template("cria_terceirizadas.html",
                               editais=editais,
                               tipo_unidade=tipo_unidade,
                               idades=idade,
                               refeicoes=refeicao)


@upload_app.route('/escolas', methods=['GET'])
@flask_login.login_required
def escolas():
    if request.method == "GET":
        escolas = get_escolas()

        return render_template("configurações_escolas.html", escolas=escolas)