import os
from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Descricao(db.Model):
    __tablename__ = 'descricao'
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.String(64), unique=True)
    curso = db.relationship('Curso', backref='descricao', lazy='dynamic')

    def __repr__(self):
        return '<Descricao %r>' % self.texto


class Curso(db.Model):
    __tablename__ = 'curso'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64), unique=True, index=True)
    descricao_id = db.Column(db.Integer, db.ForeignKey('descricao.id'), unique=True)

    def __repr__(self):
        return '<Curso %r>' % self.nome


class NameForm(FlaskForm):
    curso = StringField('Qual o nome do curso?', validators=[DataRequired()])
    descricao = TextAreaField('Descrição (250 caracteres)', validators=[DataRequired()])
    submit = SubmitField('Cadastrar')

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', hora=datetime.utcnow());

@app.route('/cursos', methods=['GET', 'POST'])
def cursos():
    form = NameForm()
    return render_template('cursos.html', form=form);
    
@app.route('/ocorrencias', methods=['GET', 'POST'])
def o():
    return render_template('nDisponivel.html', hora=datetime.utcnow());

@app.route('/alunos', methods=['GET', 'POST'])
def a():
    return render_template('nDisponivel.html', hora=datetime.utcnow());

@app.route('/disciplinas', methods=['GET', 'POST'])
def d():
    return render_template('nDisponivel.html', hora=datetime.utcnow());

@app.route('/professores', methods=['GET', 'POST'])
def p():
    return render_template('nDisponivel.html', hora=datetime.utcnow());
