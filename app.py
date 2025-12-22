import os
import json
import secrets
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, session
from src.workflow_langgraph import process_resume_with_langgraph
from werkzeug.utils import secure_filename



app = Flask(__name__)

# Carrega configurações do ficheiro config.json
CONFIG_FILE = 'config.json'


def load_config():
    """Carrega configurações do ficheiro config.json"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        'authentication': {'users': []},
        'app': {
            'secret_key': secrets.token_hex(32),
            'max_file_size_mb': 16,
            'allowed_extensions': ['pdf']
        }
    }


config = load_config()

# Configurações da aplicação
app.secret_key = config['app']['secret_key']

UPLOAD_FOLDER = 'uploads'
PHOTOS_FOLDER = 'uploads/photos'
DATA_FOLDER = 'data'
ALLOWED_EXTENSIONS = set(config['app']['allowed_extensions'])
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
MAX_FILE_SIZE = config['app']['max_file_size_mb'] * 1024 * 1024

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PHOTOS_FOLDER'] = PHOTOS_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Ficheiro para guardar metadados
METADATA_FILE = os.path.join(DATA_FOLDER, 'curriculos.json')


def generate_access_token():
    """Gera um token de acesso único e seguro"""
    return secrets.token_urlsafe(32)


def allowed_file(filename):
    """Verifica se o ficheiro tem extensão permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def allowed_image(filename):
    """Verifica se a imagem tem extensão permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


def get_color_scheme(scheme_name):
    """Retorna as cores para o esquema selecionado"""
    schemes = {
        'blue': {
            'primary': '#2c3e50',
            'secondary': '#3498db',
            'gradient': 'linear-gradient(135deg, #2c3e50 0%, #3498db 100%)'
        },
        'green': {
            'primary': '#1e3a2e',
            'secondary': '#27ae60',
            'gradient': 'linear-gradient(135deg, #1e3a2e 0%, #27ae60 100%)'
        },
        'purple': {
            'primary': '#4a148c',
            'secondary': '#9c27b0',
            'gradient': 'linear-gradient(135deg, #4a148c 0%, #9c27b0 100%)'
        },
        'orange': {
            'primary': '#d84315',
            'secondary': '#ff5722',
            'gradient': 'linear-gradient(135deg, #d84315 0%, #ff5722 100%)'
        },
        'teal': {
            'primary': '#004d40',
            'secondary': '#009688',
            'gradient': 'linear-gradient(135deg, #004d40 0%, #009688 100%)'
        }
    }
    return schemes.get(scheme_name, schemes['blue'])


def load_metadata():
    """Carrega metadados dos currículos"""
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_metadata(data):
    """Guarda metadados dos currículos"""
    with open(METADATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# Funções de autenticação
def authenticate_user(username, password):
    """Verifica se as credenciais são válidas"""
    users = config['authentication']['users']
    for user in users:
        if user['username'] == username and user['password'] == password:
            return {
                'username': user['username'],
                'name': user.get('name', username)
            }
    return None


def login_required(f):
    """Decorator para proteger rotas que requerem autenticação"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Por favor, faça login para aceder a esta página', 'error')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


# Rotas de autenticação
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if 'user' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        user = authenticate_user(username, password)
        if user:
            session['user'] = user
            flash(f'Bem-vindo, {user["name"]}!', 'success')

            # Redireciona para a página solicitada ou para o index
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Credenciais inválidas. Tente novamente.', 'error')

    return render_template('login.html')


@app.route('/logout')
def logout():
    """Logout do utilizador"""
    user_name = session.get('user', {}).get('name', 'Utilizador')
    session.pop('user', None)
    flash(f'Até breve, {user_name}!', 'success')
    return redirect(url_for('login'))


@app.route('/')
@login_required
def index():
    """Página principal com formulário de upload"""
    curriculos = load_metadata()
    return render_template('index.html', curriculos=curriculos)


@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    """Processa o upload do PDF"""
    # Verifica se o ficheiro foi enviado
    if 'pdf' not in request.files:
        flash('Nenhum ficheiro foi selecionado', 'error')
        return redirect(url_for('index'))

    file = request.files['pdf']
    username = request.form.get('username', '').strip()

    # Validações
    if file.filename == '':
        flash('Nenhum ficheiro foi selecionado', 'error')
        return redirect(url_for('index'))

    if not username:
        flash('Por favor, insira o seu nome', 'error')
        return redirect(url_for('index'))

    if not allowed_file(file.filename):
        flash('Apenas ficheiros PDF são permitidos', 'error')
        return redirect(url_for('index'))

    # Guarda o ficheiro PDF
    filename = secure_filename(file.filename)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_filename = f"{timestamp}_{filename}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(filepath)

    # Processa foto de perfil (opcional)
    profile_photo_path = None
    if 'profile_photo' in request.files:
        photo = request.files['profile_photo']
        if photo and photo.filename and allowed_image(photo.filename):
            photo_filename = secure_filename(photo.filename)
            unique_photo = f"{timestamp}_{photo_filename}"
            profile_photo_path = os.path.join(app.config['PHOTOS_FOLDER'], unique_photo)
            photo.save(profile_photo_path)
            # Caminho relativo para o template
            profile_photo_path = f"photos/{unique_photo}"

    # Processa esquema de cores (opcional)
    color_scheme_name = request.form.get('color_scheme', 'blue')
    color_scheme = get_color_scheme(color_scheme_name)

    # Gera token de acesso único
    access_token = generate_access_token()

    # === PROCESSAMENTO COM LANGGRAPH WORKFLOW ===
    flash('🚀 Processando currículo com LangGraph... Aguarde 30-60 segundos.', 'info')

    # Processa com o workflow LangGraph
    workflow_result = process_resume_with_langgraph(filepath)

    if not workflow_result['success']:
        flash(f'❌ Erro no workflow: {workflow_result.get("error")}', 'error')
        # Fallback para dados básicos
        resume_data = {
            'full_name': username,
            'professional_title': 'Profissional',
            'about_summary': 'Profissional qualificado.',
            'experience_summary': 'Experiência profissional.',
            'education_summary': 'Formação académica.',
            'skills_summary': 'Competências técnicas.',
            'experience_items': [],
            'education_items': [],
            'skills': []
        }
    else:
        # Extrai dados do website gerado pelo workflow
        website_structure = workflow_result['website_structure']
        resume_data = website_structure.get('data', {})

        # Mostra avisos se houver
        if workflow_result.get('errors'):
            for error in workflow_result['errors']:
                flash(f'⚠️ {error}', 'warning')

    # Garante que full_name existe
    if 'full_name' not in resume_data or not resume_data['full_name']:
        resume_data['full_name'] = username

    # Adiciona foto de perfil e cores aos dados
    resume_data['profile_photo'] = profile_photo_path
    resume_data['color_primary'] = color_scheme['primary']
    resume_data['color_secondary'] = color_scheme['secondary']
    resume_data['color_gradient'] = color_scheme['gradient']

    # Guarda metadados
    metadata = load_metadata()
    new_entry = {
        'id': len(metadata) + 1,
        'username': username,
        'filename': unique_filename,
        'original_filename': filename,
        'upload_date': datetime.now().isoformat(),
        'access_token': access_token,
        'resume_data': resume_data,
        'profile_photo': profile_photo_path,
        'color_scheme': color_scheme_name,
        'processed': True
    }
    metadata.append(new_entry)
    save_metadata(metadata)

    flash(f'Website de {username} gerado com sucesso!', 'success')
    return redirect(url_for('website', token=access_token))


@app.route('/viewer/<token>')
def viewer(token):
    """Página de visualização do PDF"""
    metadata = load_metadata()
    curriculo = next((c for c in metadata if c.get('access_token') == token), None)

    if not curriculo:
        flash('Currículo não encontrado ou token inválido', 'error')
        return redirect(url_for('index'))

    return render_template('viewer.html', curriculo=curriculo)


@app.route('/website/<token>')
def website(token):
    """Página do website personalizado gerado a partir do currículo (SPA)"""
    metadata = load_metadata()
    curriculo = next((c for c in metadata if c.get('access_token') == token), None)

    if not curriculo:
        flash('Website não encontrado ou token inválido', 'error')
        return redirect(url_for('index'))

    # Extrai dados do currículo analisado
    resume_data = curriculo.get('resume_data', {})

    # Adiciona ano atual
    resume_data['current_year'] = datetime.now().year

    return render_template('website_simple.html', **resume_data)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve os ficheiros PDF"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/delete/<token>', methods=['POST'])
@login_required
def delete_curriculo(token):
    """Elimina um currículo"""
    metadata = load_metadata()
    curriculo = next((c for c in metadata if c.get('access_token') == token), None)

    if curriculo:
        # Remove o ficheiro
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], curriculo['filename'])
        if os.path.exists(filepath):
            os.remove(filepath)

        # Remove dos metadados
        metadata = [c for c in metadata if c.get('access_token') != token]
        save_metadata(metadata)

        flash('Currículo eliminado com sucesso', 'success')
    else:
        flash('Currículo não encontrado ou token inválido', 'error')

    return redirect(url_for('index'))


@app.route('/uploads/photos/<filename>')
def uploaded_photo(filename):
    """Serve as fotos de perfil"""
    return send_from_directory(app.config['PHOTOS_FOLDER'], filename)


if __name__ == '__main__':
    # Cria diretórios se não existirem
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(PHOTOS_FOLDER, exist_ok=True)
    os.makedirs(DATA_FOLDER, exist_ok=True)

    # Inicia o servidor
    app.run(debug=True, host='0.0.0.0', port=5001)
