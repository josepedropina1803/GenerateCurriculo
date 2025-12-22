# 📄 Gerador de Website Curricular com IA

Aplicação Flask que converte currículos PDF em websites profissionais personalizados usando IA (LangGraph + Groq/Ollama).

![Version](https://img.shields.io/badge/version-2.0-blue)
![Python](https://img.shields.io/badge/python-3.11+-green)
![License](https://img.shields.io/badge/license-MIT-orange)

---

## ✨ Funcionalidades

### 🤖 Processamento com IA
- **Extração inteligente** de texto de PDFs com correção de acentos
- **Análise automática** com LangGraph workflow
- **Geração de resumos** profissionais para cada secção
- **LLM flexível**: Ollama (local) ou Groq (nuvem, gratuito)

### 🎨 Personalização
- **5 esquemas de cores** profissionais
- **Upload de foto de perfil** (opcional)
- **Website SPA** responsivo e moderno
- **Design limpo** sem navbar, focado em conteúdo

### 🔗 Partilha
- **Botão de partilha** com link único
- **Partilha direta** via WhatsApp, LinkedIn, Email
- **Copiar link** com feedback visual
- **Acesso público** sem necessidade de login

### 🔐 Segurança
- **Sistema de autenticação** configurável
- **Tokens únicos** para cada currículo
- **Validação de arquivos** e sanitização
- **HTTPS** pronto (em produção)

---

## 🚀 Deploy Gratuito

**Veja [DEPLOY.md](DEPLOY.md)** para instruções completas de deploy no Render com:
- ✅ Domínio gratuito (.onrender.com)
- ✅ HTTPS automático
- ✅ Storage persistente
- ✅ Deploy automático via GitHub

---

## 🏠 Instalação Local

### Requisitos

- Python 3.11+
- Ollama (para desenvolvimento local) ou Groq API Key

### Passo 1: Clone o repositório

```bash
git clone https://github.com/josepedropina1803/GenerateCurriculo.git
cd GenerateCurriculo
```

### Passo 2: Instale dependências

```bash
# Criar ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Instalar pacotes
pip install -r requirements.txt
```

### Passo 3: Configure Ollama (opcional para local)

```bash
# Instalar Ollama
# macOS/Linux: https://ollama.com/download
# Windows: https://ollama.com/download/windows

# Baixar modelo
ollama pull llama3
```

**OU** use Groq (gratuito):

```bash
# Criar arquivo .env
cp .env.example .env

# Editar .env e adicionar:
# GROQ_API_KEY=sua_chave_aqui
# Obtenha em: https://console.groq.com
```

### Passo 4: Configure autenticação

```bash
# Copiar exemplo
cp config.json.example config.json

# Editar config.json
# Altere username, password e secret_key
```

### Passo 5: Execute

```bash
python app.py
```

Acesse: http://localhost:5001

---

## 📁 Estrutura do Projeto

```
GenerateCurriculo/
├── app.py                      # Aplicação Flask principal
├── src/
│   ├── workflow_langgraph.py   # Workflow de IA (LangGraph)
│   ├── pdf_extractor.py        # Extração e normalização de PDFs
│   └── ollama_ai.py           # (Legacy)
├── templates/
│   ├── index.html             # Dashboard de upload
│   ├── login.html             # Autenticação
│   ├── website_simple.html    # Template SPA do currículo
│   └── viewer.html            # Visualizador de PDF
├── static/css/
│   └── style.css              # Estilos globais
├── uploads/                   # PDFs e fotos (auto-criado)
├── data/                      # Metadados JSON (auto-criado)
├── requirements.txt           # Dependências Python
├── render.yaml               # Configuração para Render
├── DEPLOY.md                 # Guia de deploy
└── README.md                 # Este arquivo
```

---

## 🎯 Como Usar

### 1. Login
- Acesse a aplicação
- Use credenciais do `config.json`

### 2. Upload de Currículo
- Insira seu nome
- Carregue PDF do currículo
- (Opcional) Adicione foto de perfil
- (Opcional) Escolha esquema de cores

### 3. Aguarde Processamento
- IA extrai e analisa o currículo (30-60s)
- Gera resumos profissionais
- Cria website personalizado

### 4. Visualize e Partilhe
- Veja seu website curricular
- Clique em "🔗 Partilhar"
- Copie link ou partilhe em redes sociais

---

## 🛠️ Tecnologias

### Backend
- **Flask** - Framework web
- **LangGraph** - Workflow de IA
- **LangChain** - Integração com LLMs
- **Groq/Ollama** - Modelos de linguagem
- **pdfplumber** - Extração de PDFs

### Frontend
- **Vanilla JS** - Sem frameworks
- **CSS3** - Design moderno
- **Responsive** - Mobile-first

### Deploy
- **Render** - Hosting gratuito
- **Gunicorn** - WSGI server
- **GitHub** - CI/CD automático

---

## 🎨 Esquemas de Cores

1. **Azul Profissional** (padrão) - #2c3e50 → #3498db
2. **Verde Corporativo** - #1e3a2e → #27ae60
3. **Roxo Criativo** - #4a148c → #9c27b0
4. **Laranja Dinâmico** - #d84315 → #ff5722
5. **Teal Moderno** - #004d40 → #009688

---

## 🔧 Configuração

### config.json

```json
{
  "authentication": {
    "users": [
      {
        "username": "admin",
        "password": "sua_senha",
        "name": "Administrador"
      }
    ]
  },
  "app": {
    "secret_key": "chave_secreta_aleatoria",
    "max_file_size_mb": 16,
    "allowed_extensions": ["pdf"]
  }
}
```

### Variáveis de Ambiente

```bash
# .env (opcional para Groq)
GROQ_API_KEY=sua_chave_groq
```

---

## 📊 Workflow de IA

```
PDF Upload
    ↓
[NODE 1] Extração de Texto
    - pdfplumber
    - Normalização de acentos
    ↓
[NODE 2] Análise e Resumos
    - Identificação de secções
    - Extração de dados
    - Geração de resumos
    ↓
[NODE 3] Estrutura do Website
    - Organização de conteúdo
    - Aplicação de cores
    - Preparação para renderização
    ↓
Website Gerado ✨
```

---

## 🐛 Problemas Conhecidos

- Plano gratuito do Render "dorme" após 15min
- Storage limitado a 1GB (gratuito)
- PDFs com encoding especial podem ter problemas de acentos

---

## 🚧 Roadmap

- [ ] Temas adicionais (minimalista, criativo, executivo)
- [ ] Download do website como HTML estático
- [ ] Edição manual dos resumos gerados
- [ ] Suporte para múltiplos idiomas
- [ ] Analytics de visualizações
- [ ] Integração com LinkedIn API
- [ ] Templates de website adicionais

---

## 📝 Licença

MIT License - Use livremente!

---

## 👤 Autor

**José Pedro Pina**
GitHub: [@josepedropina1803](https://github.com/josepedropina1803)

---

## 🙏 Agradecimentos

- [LangChain](https://langchain.com) - Framework de IA
- [Groq](https://groq.com) - API gratuita e rápida
- [Render](https://render.com) - Hosting gratuito
- [Ollama](https://ollama.com) - LLMs locais

---

## 💡 Suporte

Encontrou um bug? Tem uma sugestão?
Abra uma [issue](https://github.com/josepedropina1803/GenerateCurriculo/issues)

---

**⭐ Se gostou do projeto, deixe uma estrela no GitHub!**
