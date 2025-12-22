"""
Módulo para extração de texto de PDFs usando pdfplumber
"""
import pdfplumber
from typing import Dict, List


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