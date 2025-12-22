# 🚀 Guia de Deploy - Render (Gratuito)

Este guia explica como fazer deploy gratuito da aplicação no Render com domínio gratuito.

---

## 📋 Pré-requisitos

1. **Conta no GitHub** (já tem ✓)
2. **Conta no Render** - Criar em [render.com](https://render.com)
3. **Chave API do Groq** (gratuita) - Obter em [console.groq.com](https://console.groq.com)

---

## 🔑 Passo 1: Obter Chave API do Groq (Gratuito)

1. Acesse: https://console.groq.com
2. Faça login (pode usar conta Google/GitHub)
3. Vá em **API Keys** no menu lateral
4. Clique em **Create API Key**
5. Dê um nome (ex: "GenerateCurriculo")
6. **COPIE a chave** e guarde (não será mostrada novamente)

---

## 🌐 Passo 2: Deploy no Render

### 2.1 Criar conta no Render

1. Acesse: https://render.com
2. Clique em **Get Started**
3. Faça login com sua conta GitHub

### 2.2 Criar Web Service

1. No dashboard do Render, clique em **New +**
2. Selecione **Web Service**
3. Conecte seu repositório GitHub:
   - Clique em **Connect account** (se necessário)
   - Procure por `GenerateCurriculo`
   - Clique em **Connect**

### 2.3 Configurar o Service

Preencha os campos:

- **Name**: `generatecurriculo` (ou outro nome)
- **Region**: Escolha a mais próxima (Europe West)
- **Branch**: `master`
- **Runtime**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`

### 2.4 Configurar Variáveis de Ambiente

1. Role até **Environment Variables**
2. Clique em **Add Environment Variable**
3. Adicione:
   ```
   Key: GROQ_API_KEY
   Value: [COLE SUA CHAVE AQUI]
   ```

### 2.5 Configurar Plano e Storage

1. **Instance Type**: Free
2. **Auto-Deploy**: Yes (recomendado)
3. Role até **Disk** e clique em **Add Disk**:
   - **Name**: `uploads-data`
   - **Mount Path**: `/opt/render/project/src/uploads`
   - **Size**: 1 GB

### 2.6 Deploy!

1. Clique em **Create Web Service**
2. Aguarde 5-10 minutos enquanto o Render faz o build
3. Quando aparecer **Live**, seu site está no ar! 🎉

---

## 🔗 Seu Domínio Gratuito

Após o deploy, você terá:
- **URL**: `https://generatecurriculo.onrender.com`
- **Acesso público**: Qualquer pessoa pode acessar
- **HTTPS**: Certificado SSL gratuito

---

## ⚙️ Configuração Inicial da Aplicação

### Criar arquivo de configuração

1. No primeiro acesso, você verá um erro. Isso é esperado!
2. Acesse o **Shell** do Render:
   - Dashboard → Seu Service → **Shell**
3. Crie o arquivo `config.json`:

```bash
cat > config.json << 'EOF'
{
  "authentication": {
    "users": [
      {
        "username": "admin",
        "password": "123",
        "name": "Administrador"
      }
    ]
  },
  "app": {
    "secret_key": "sua_chave_secreta_muito_longa_e_aleatoria_aqui",
    "max_file_size_mb": 16,
    "allowed_extensions": ["pdf"]
  }
}
EOF
```

4. Altere `sua_senha_aqui` e `sua_chave_secreta_...`
5. Pressione Enter
6. Reinicie o serviço

---

## 🎨 Acessando sua Aplicação

1. Acesse: `https://seu-app.onrender.com`
2. Faça login com as credenciais do `config.json`
3. Carregue um PDF de currículo
4. Aguarde 30-60 segundos
5. Veja seu website profissional! ✨

---

## ⚠️ Limitações do Plano Gratuito

### Render Free Tier

- ✅ **Domínio gratuito** (.onrender.com)
- ✅ **HTTPS automático**
- ✅ **750 horas/mês gratuitas**
- ⚠️ **Dorme após 15 min de inatividade** (leva ~30s para acordar)
- ⚠️ **1 GB de storage** (suficiente para ~50 currículos)
- ⚠️ **512 MB RAM**

### Groq API Free Tier

- ✅ **Completamente gratuito**
- ✅ **6,000 requisições/minuto**
- ✅ **Muito rápido**
- ⚠️ Limite de tokens por requisição

---

## 🔧 Manutenção

### Atualizar código

1. Faça `git push` para o GitHub
2. Render fará deploy automático
3. Aguarde 2-5 minutos

### Verificar logs

1. Dashboard → Seu Service → **Logs**
2. Veja erros e informações em tempo real

### Adicionar mais utilizadores

1. Acesse o Shell do Render
2. Edite `config.json`:
```bash
vi config.json
```

---

## 🆘 Problemas Comuns

### ❌ Site não carrega

**Solução**: Aguarde 30 segundos (pode estar "dormindo")

### ❌ Erro 500 ao carregar PDF

**Solução**:
1. Verifique se `GROQ_API_KEY` está configurada
2. Verifique logs para ver o erro específico

### ❌ "No space left on device"

**Solução**:
1. Apague currículos antigos
2. Ou aumente o disco (plano pago)

### ❌ Foto de perfil não aparece

**Solução**:
1. Verifique se o disco está montado em `/opt/render/project/src/uploads`
2. Reinicie o serviço

---

## 💡 Dicas

1. **Domínio personalizado**: Configure em Settings → Custom Domains
2. **Monitoramento**: Configure notificações de deploy
3. **Backup**: Baixe currículos importantes periodicamente
4. **Performance**: Considere plano pago para melhor performance

---

## 🎉 Pronto!

Sua aplicação está online e acessível em qualquer lugar do mundo!

**URL de exemplo**: `https://generatecurriculo.onrender.com`

Compartilhe o link com outras pessoas! 🚀
