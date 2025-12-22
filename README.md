# Gerador de Currículo Web

Aplicação web Flask para carregar, armazenar e visualizar currículos em PDF.

## Funcionalidades

- Upload de currículos em formato PDF
- Armazenamento seguro de ficheiros e metadados
- Visualização de PDFs no navegador
- Lista de todos os currículos carregados
- Download de PDFs
- Eliminar currículos
- Interface moderna e responsiva
- Suporte para ecrã completo

## Estrutura do Projeto

```
GenerateCurriculo/
├── app.py                  # Aplicação Flask principal
├── templates/
│   ├── index.html         # Página de upload e listagem
│   └── viewer.html        # Visualizador de PDF
├── static/
│   └── css/
│       └── style.css      # Estilos da aplicação
├── uploads/               # PDFs carregados (criado automaticamente)
├── data/                  # Metadados em JSON (criado automaticamente)
├── requirements.txt       # Dependências Python
└── README.md             # Este ficheiro
```

## Requisitos

- Python 3.8+
- pip (gestor de pacotes Python)

## Instalação

1. Clone ou descarregue o repositório:
```bash
cd GenerateCurriculo
```

2. Crie e ative um ambiente virtual (opcional mas recomendado):
```bash
python -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Como Usar

1. Inicie o servidor Flask:
```bash
python app.py
```

2. Abra o navegador e aceda a:
```
http://localhost:5000
```

3. Na página principal:
   - Insira o seu nome
   - Selecione um ficheiro PDF (máximo 16MB)
   - Clique em "Carregar Currículo"

4. O PDF será automaticamente visualizado após o upload

5. Na página inicial, pode:
   - Ver todos os currículos carregados
   - Visualizar qualquer currículo
   - Descarregar PDFs
   - Eliminar currículos

## Funcionalidades Técnicas

### Backend (Flask)
- Validação de ficheiros (apenas PDFs)
- Limite de tamanho de ficheiro (16MB)
- Nomes de ficheiros únicos com timestamp
- Armazenamento de metadados em JSON
- Rotas para upload, visualização e eliminação

### Frontend
- Design responsivo (funciona em mobile e desktop)
- Visualizador de PDF integrado
- Modo ecrã completo
- Mensagens de feedback ao utilizador
- Animações suaves
- Gradiente moderno

### Segurança
- Validação de extensão de ficheiros
- Sanitização de nomes de ficheiros
- Limite de tamanho de upload
- Secret key para sessões Flask

## Personalização

### Alterar o limite de tamanho de ficheiro

No ficheiro `app.py`, linha 13:
```python
MAX_FILE_SIZE = 16 * 1024 * 1024  # Altere para o tamanho desejado em bytes
```

### Alterar a porta do servidor

No ficheiro `app.py`, última linha:
```python
app.run(debug=True, host='0.0.0.0', port=5000)  # Altere 5000 para a porta desejada
```

### Personalizar cores

Edite as variáveis CSS no ficheiro `static/css/style.css`:
```css
:root {
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    /* ... outras cores ... */
}
```

## Produção

Para usar em produção, altere `app.py`:

1. Desative o modo debug:
```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

2. Altere a secret key para algo seguro:
```python
app.secret_key = 'sua-chave-secreta-muito-forte-aqui'
```

3. Use um servidor WSGI como Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Limitações Conhecidas

- Alguns navegadores podem não suportar visualização de PDFs inline
- PDFs muito grandes podem demorar a carregar
- Não há autenticação de utilizadores (todos podem ver todos os currículos)

## Melhorias Futuras

- Autenticação de utilizadores
- Base de dados SQL em vez de JSON
- Conversão de PDF para HTML/CSS
- Pesquisa e filtros
- Categorização de currículos
- Miniaturas de PDFs
- Upload múltiplo
- Armazenamento em cloud (S3, etc.)

## Licença

Projeto de uso livre.

## Autor

Desenvolvido para facilitar o carregamento e visualização de currículos em formato web.
