from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moto_pecas.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Modelos
class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(120), nullable=False)
    nome = db.Column(db.String(80), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    imagem = db.Column(db.String(200))
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Rotas
@app.route('/')
def index():
    produtos = Produto.query.order_by(Produto.data_criacao.desc()).all()
    return render_template('index.html', produtos=produtos)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        usuario = Usuario.query.filter_by(email=email).first()
        
        if usuario and check_password_hash(usuario.senha, senha):
            login_user(usuario)
            return redirect(url_for('index'))
        flash('Email ou senha inválidos')
    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        nome = request.form.get('nome')
        
        if Usuario.query.filter_by(email=email).first():
            flash('Email já cadastrado')
            return redirect(url_for('registro'))
            
        novo_usuario = Usuario(
            email=email,
            senha=generate_password_hash(senha),
            nome=nome
        )
        db.session.add(novo_usuario)
        db.session.commit()
        flash('Registro realizado com sucesso!')
        return redirect(url_for('login'))
    return render_template('registro.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/admin/produtos', methods=['GET', 'POST'])
@login_required
def admin_produtos():
    if not current_user.is_admin:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')
        preco = float(request.form.get('preco'))
        
        if 'imagem' in request.files:
            arquivo = request.files['imagem']
            if arquivo and allowed_file(arquivo.filename):
                filename = secure_filename(arquivo.filename)
                arquivo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                imagem = f'uploads/{filename}'
            else:
                imagem = None
        else:
            imagem = None
            
        novo_produto = Produto(
            nome=nome,
            descricao=descricao,
            preco=preco,
            imagem=imagem
        )
        db.session.add(novo_produto)
        db.session.commit()
        flash('Produto adicionado com sucesso!')
        return redirect(url_for('admin_produtos'))
        
    produtos = Produto.query.all()
    return render_template('admin_produtos.html', produtos=produtos)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Criar usuário admin se não existir
        if not Usuario.query.filter_by(email='admin@admin.com').first():
            admin = Usuario(
                email='admin@admin.com',
                senha=generate_password_hash('admin123'),
                nome='Administrador',
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
    app.run(debug=True) 