"""
Módulo para extração de texto de PDFs usando pdfplumber
"""
import pdfplumber
from typing import Dict, List
import unicodedata


def normalize_text(text: str) -> str:
    """
    Normaliza texto para corrigir problemas de encoding e acentos
    Resolve problemas como Jos´e → José
    """
    if not text:
        return text

    # Mapa de correção para acentos mal formatados (padrão comum em PDFs)
    accent_fixes = {
        '´a': 'á', '´e': 'é', '´i': 'í', '´o': 'ó', '´u': 'ú',
        '´A': 'Á', '´E': 'É', '´I': 'Í', '´O': 'Ó', '´U': 'Ú',
        '`a': 'à', '`e': 'è', '`i': 'ì', '`o': 'ò', '`u': 'ù',
        '`A': 'À', '`E': 'È', '`I': 'Ì', '`O': 'Ò', '`U': 'Ù',
        '^a': 'â', '^e': 'ê', '^i': 'î', '^o': 'ô', '^u': 'û',
        '^A': 'Â', '^E': 'Ê', '^I': 'Î', '^O': 'Ô', '^U': 'Û',
        '~a': 'ã', '~o': 'õ', '~n': 'ñ',
        '~A': 'Ã', '~O': 'Õ', '~N': 'Ñ',
        '¨a': 'ä', '¨e': 'ë', '¨i': 'ï', '¨o': 'ö', '¨u': 'ü',
        '¨A': 'Ä', '¨E': 'Ë', '¨I': 'Ï', '¨O': 'Ö', '¨U': 'Ü',
        'c¸': 'ç', 'C¸': 'Ç',
    }

    # Aplica correções de acentos invertidos (acento antes da letra)
    for wrong, correct in accent_fixes.items():
        text = text.replace(wrong, correct)

    # Também tenta padrão inverso comum (letra + acento)
    text = text.replace('a´', 'á').replace('e´', 'é').replace('i´', 'í').replace('o´', 'ó').replace('u´', 'ú')
    text = text.replace('A´', 'Á').replace('E´', 'É').replace('I´', 'Í').replace('O´', 'Ó').replace('U´', 'Ú')
    text = text.replace('a`', 'à').replace('e`', 'è').replace('i`', 'ì').replace('o`', 'ò').replace('u`', 'ù')
    text = text.replace('a^', 'â').replace('e^', 'ê').replace('i^', 'î').replace('o^', 'ô').replace('u^', 'û')
    text = text.replace('a~', 'ã').replace('o~', 'õ').replace('n~', 'ñ')
    text = text.replace('c¸', 'ç').replace('C¸', 'Ç')

    # Normaliza unicode (converte caracteres compostos para forma canônica)
    text = unicodedata.normalize('NFC', text)

    # Remove caracteres de controle mantendo quebras de linha
    text = ''.join(char for char in text if char == '\n' or not unicodedata.category(char).startswith('C'))

    return text


def extract_text_from_pdf(pdf_path: str) -> Dict[str, any]:
    """
    Extrai texto de um PDF e retorna informações estruturadas

    Args:
        pdf_path: Caminho para o ficheiro PDF

    Returns:
        Dict com texto completo, número de páginas e metadados
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # Extrai texto de todas as páginas
            pages_text = []
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    # Normaliza o texto para corrigir problemas de acentos
                    text = normalize_text(text)
                    pages_text.append(text)

            # Texto completo
            full_text = "\n\n".join(pages_text)

            # Metadados do PDF
            metadata = pdf.metadata or {}

            return {
                'success': True,
                'text': full_text,
                'num_pages': len(pdf.pages),
                'pages': pages_text,
                'metadata': {
                    'title': metadata.get('Title', ''),
                    'author': metadata.get('Author', ''),
                    'subject': metadata.get('Subject', ''),
                    'creator': metadata.get('Creator', ''),
                }
            }

    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'text': '',
            'num_pages': 0,
            'pages': [],
            'metadata': {}
        }


def extract_sections_from_text(text: str) -> Dict[str, str]:
    """
    Tenta identificar secções comuns de um currículo

    Args:
        text: Texto extraído do PDF

    Returns:
        Dict com secções identificadas
    """
    sections = {
        'full_text': text,
        'contact_info': '',
        'experience': '',
        'education': '',
        'skills': '',
        'summary': ''
    }

    # Palavras-chave para identificar secções
    keywords = {
        'experience': ['experiência', 'experience', 'trabalho', 'work history', 'employment'],
        'education': ['educação', 'education', 'formação', 'academic'],
        'skills': ['competências', 'skills', 'habilidades', 'aptidões', 'conhecimentos'],
        'summary': ['resumo', 'summary', 'sobre', 'about', 'perfil', 'profile']
    }

    text_lower = text.lower()
    lines = text.split('\n')

    # Tenta identificar secções básicas
    current_section = None
    section_content = []

    for line in lines:
        line_lower = line.lower().strip()

        # Verifica se a linha indica o início de uma nova secção
        for section_name, section_keywords in keywords.items():
            if any(keyword in line_lower for keyword in section_keywords):
                # Guarda a secção anterior
                if current_section and section_content:
                    sections[current_section] = '\n'.join(section_content)

                current_section = section_name
                section_content = []
                break
        else:
            # Adiciona a linha à secção atual
            if current_section and line.strip():
                section_content.append(line)

    # Guarda a última secção
    if current_section and section_content:
        sections[current_section] = '\n'.join(section_content)

    return sections