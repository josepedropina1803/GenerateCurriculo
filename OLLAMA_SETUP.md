# Configuração do Ollama para Geração de Websites

O sistema usa **Ollama** para analisar currículos em PDF e gerar websites personalizados automaticamente.

## O que é o Ollama?

Ollama permite executar modelos de IA localmente no seu computador, **100% grátis** e sem necessidade de API keys ou custos de cloud.

## Instalação do Ollama

O Ollama já está instalado no seu sistema (`/usr/local/bin/ollama`).

## Como Iniciar o Ollama

### 1. Inicie o servidor Ollama:

```bash
ollama serve
```

Deixe este terminal aberto - o Ollama precisa estar em execução em segundo plano.

### 2. Num NOVO terminal, baixe o modelo recomendado:

```bash
ollama pull llama3.2
```

Este comando irá descarregar o modelo Llama 3.2 (aproximadamente 2GB). Só precisa fazer isto uma vez.

### 3. Modelos alternativos (opcional):

Se preferir um modelo diferente:

```bash
# Modelo mais pequeno e rápido (1.5GB)
ollama pull llama3.2:1b

# Modelo maior e mais preciso (4.7GB)
ollama pull llama3.2:3b

# Para português mais fluente
ollama pull gemma2:2b
```

## Verificar se está a funcionar

Teste se o Ollama está em execução:

```bash
curl http://localhost:11434/api/tags
```

Se estiver a funcionar, verá uma lista de modelos instalados.

## Como funciona no sistema

Quando faz upload de um PDF:

1. **Extração de texto** - O sistema lê todo o texto do PDF
2. **Análise com AI** - O Ollama analisa e estrutura as informações (nome, experiência, educação, competências)
3. **Geração de conteúdo** - Cria bio profissional, headlines, etc.
4. **Website gerado** - Renderiza um website corporativo personalizado

## Se o Ollama não estiver disponível

O sistema continuará a funcionar, mas:
- O website será criado com dados básicos
- Não haverá análise inteligente do conteúdo
- Verá uma mensagem: "Ollama não está em execução"

## Estrutura dos dados gerados

O Ollama extrai e estrutura:

```json
{
  "nome_completo": "Nome da Pessoa",
  "titulo_profissional": "Cargo Principal",
  "resumo_profissional": "Breve descrição...",
  "email": "email@exemplo.com",
  "telefone": "+351 ...",
  "localizacao": "Lisboa, Portugal",
  "linkedin": "URL",
  "github": "URL",
  "experiencias": [
    {
      "empresa": "Nome",
      "cargo": "Posição",
      "periodo": "2020 - 2023",
      "descricao": "Responsabilidades..."
    }
  ],
  "educacao": [...],
  "competencias": [...],
  "idiomas": [...],
  "certificacoes": [...]
}
```

## Troubleshooting

### Erro: "Connection refused"
- O Ollama não está em execução
- Solução: Execute `ollama serve` num terminal separado

### Erro: "Model not found"
- O modelo não foi baixado
- Solução: Execute `ollama pull llama3.2`

### Processamento muito lento
- Modelo muito grande para o seu hardware
- Solução: Use um modelo mais leve (`ollama pull llama3.2:1b`)

### Ollama usa muita memória
- Normal para modelos grandes
- Solução: Feche o Ollama quando não estiver em uso (`pkill ollama`)

## Performance

- **Tempo de processamento**: 30-90 segundos por currículo
- **Uso de memória**: 2-8GB dependendo do modelo
- **Uso de CPU**: Alto durante processamento
- **Custo**: **ZERO** - totalmente grátis

## Comandos úteis

```bash
# Verificar modelos instalados
ollama list

# Remover um modelo
ollama rm llama3.2

# Parar o Ollama
pkill ollama

# Ver logs do Ollama
ollama serve --verbose
```

## Alterando o modelo usado

Edite o ficheiro `ollama_ai.py` e mude a variável `DEFAULT_MODEL`:

```python
DEFAULT_MODEL = "llama3.2"  # Mude para "gemma2:2b" ou outro
```

## Recursos

- [Documentação oficial do Ollama](https://ollama.ai)
- [Lista de modelos disponíveis](https://ollama.ai/library)
- [GitHub do Ollama](https://github.com/jmorganca/ollama)
