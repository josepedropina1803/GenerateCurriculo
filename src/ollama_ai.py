"""
Módulo para integração com Ollama (AI local)
"""
import requests
import json
from typing import Dict, Optional


OLLAMA_API_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "llama3"  # Modelo padrão, pode ser mudado


def check_ollama_available() -> bool:
    """
    Verifica se o Ollama está em execução

    Returns:
        True se Ollama está disponível, False caso contrário
    """
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        return response.status_code == 200
    except:
        return False


def analyze_resume_with_ollama(resume_text: str, model: str = DEFAULT_MODEL) -> Dict:
    """
    Analisa um currículo usando Ollama e extrai informações estruturadas

    Args:
        resume_text: Texto do currículo
        model: Modelo Ollama a usar

    Returns:
        Dict com informações extraídas
    """
    if not check_ollama_available():
        return {
            'success': False,
            'error': 'Ollama não está em execução. Execute: ollama serve'
        }

    prompt = f"""Analisa o seguinte currículo e extrai informações estruturadas em formato JSON.

Currículo:
{resume_text}

Por favor, extrai e estrutura as seguintes informações em JSON:
{{
  "nome_completo": "Nome da pessoa",
  "titulo_profissional": "Cargo/Função principal",
  "resumo_profissional": "Breve resumo em 2-3 frases",
  "email": "email se disponível",
  "telefone": "telefone se disponível",
  "localizacao": "cidade/país",
  "linkedin": "URL do LinkedIn se disponível",
  "github": "URL do GitHub se disponível",
  "website": "website pessoal se disponível",
  "experiencias": [
    {{
      "empresa": "Nome da empresa",
      "cargo": "Cargo ocupado",
      "periodo": "Data início - Data fim",
      "descricao": "Descrição das responsabilidades"
    }}
  ],
  "educacao": [
    {{
      "instituicao": "Nome da instituição",
      "curso": "Nome do curso/grau",
      "periodo": "Data início - Data fim",
      "descricao": "Detalhes adicionais"
    }}
  ],
  "competencias": [
    "Competência 1",
    "Competência 2"
  ],
  "idiomas": [
    {{
      "idioma": "Nome do idioma",
      "nivel": "Nível de proficiência"
    }}
  ],
  "certificacoes": [
    "Certificação 1",
    "Certificação 2"
  ],
  "cores_tematicas": {{
    "primaria": "#hexcolor",
    "secundaria": "#hexcolor"
  }}
}}

Responde APENAS com o JSON válido, sem texto adicional."""

    try:
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "format": "json"
        }

        response = requests.post(
            OLLAMA_API_URL,
            json=payload,
            timeout=120  # 2 minutos timeout
        )

        if response.status_code == 200:
            result = response.json()
            ai_response = result.get('response', '')

            # Tenta fazer parse do JSON
            try:
                parsed_data = json.loads(ai_response)
                return {
                    'success': True,
                    'data': parsed_data,
                    'raw_response': ai_response
                }
            except json.JSONDecodeError as e:
                # Se falhar, tenta extrair JSON da resposta
                return {
                    'success': False,
                    'error': f'Falha ao fazer parse do JSON: {str(e)}',
                    'raw_response': ai_response
                }
        else:
            return {
                'success': False,
                'error': f'Erro na API do Ollama: {response.status_code}'
            }

    except requests.Timeout:
        return {
            'success': False,
            'error': 'Timeout ao comunicar com Ollama (>2min)'
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Erro inesperado: {str(e)}'
        }


def generate_website_content(resume_data: Dict, model: str = DEFAULT_MODEL) -> Dict:
    """
    Gera conteúdo adicional para o website (bio, headline, etc.)

    Args:
        resume_data: Dados estruturados do currículo
        model: Modelo Ollama a usar

    Returns:
        Dict com conteúdo gerado
    """
    if not check_ollama_available():
        return {
            'success': False,
            'error': 'Ollama não está em execução'
        }

    nome = resume_data.get('nome_completo', 'Profissional')
    titulo = resume_data.get('titulo_profissional', '')
    experiencias = resume_data.get('experiencias', [])

    prompt = f"""Com base nas seguintes informações profissionais de {nome}:

Título: {titulo}
Experiências: {json.dumps(experiencias, ensure_ascii=False, indent=2)}

Gera os seguintes conteúdos para um website profissional corporativo em formato JSON:

{{
  "headline": "Uma frase impactante (máx 100 caracteres) que resume a proposta de valor profissional",
  "bio_curta": "Parágrafo de 50-70 palavras sobre a trajetória profissional",
  "bio_longa": "2-3 parágrafos (150-200 palavras) com história profissional detalhada",
  "call_to_action": "Frase convidativa para contacto (máx 60 caracteres)",
  "meta_description": "Descrição SEO do profissional (máx 160 caracteres)"
}}

Responde APENAS com JSON válido."""

    try:
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "format": "json"
        }

        response = requests.post(
            OLLAMA_API_URL,
            json=payload,
            timeout=60
        )

        if response.status_code == 200:
            result = response.json()
            ai_response = result.get('response', '')

            try:
                parsed_data = json.loads(ai_response)
                return {
                    'success': True,
                    'data': parsed_data
                }
            except json.JSONDecodeError:
                return {
                    'success': False,
                    'error': 'Falha ao fazer parse do JSON gerado'
                }
        else:
            return {
                'success': False,
                'error': f'Erro na API: {response.status_code}'
            }

    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }