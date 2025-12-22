"""
Workflow LangGraph simplificado para processamento de currículos
Extração PDF → Análise AI → Website simples com resumos
"""
from typing import TypedDict, List, Dict
from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
import json

from src.pdf_extractor import extract_text_from_pdf


# === ESTADO DO WORKFLOW ===
class ResumeWorkflowState(TypedDict):
    """Estado compartilhado entre todos os nodes do workflow"""
    pdf_path: str
    pdf_text: str
    analyzed_data: Dict
    website_structure: Dict
    errors: List[str]
    processing_stage: str


# === CONFIGURAÇÃO DO LLM ===
def get_llm(temperature: float = 0.3):
    """Retorna instância do ChatOllama"""
    return ChatOllama(
        model="llama3",
        temperature=temperature,
        base_url="http://localhost:11434",
        format="json"
    )


# === NODE 1: EXTRAÇÃO DE PDF ===
def extract_pdf_node(state: ResumeWorkflowState) -> ResumeWorkflowState:
    """Extrai texto do PDF usando pdfplumber"""
    print("📄 [NODE 1] Extraindo texto do PDF...")

    pdf_data = extract_text_from_pdf(state['pdf_path'])

    if not pdf_data['success']:
        state['errors'].append(f"Erro ao extrair PDF: {pdf_data.get('error')}")
        state['pdf_text'] = ""
    else:
        state['pdf_text'] = pdf_data['text']

    state['processing_stage'] = "PDF extraído"
    print(f"   ✓ Extraídos {len(state['pdf_text'])} caracteres")

    return state


# === NODE 2: ANÁLISE COMPLETA E RESUMOS ===
def analyze_and_summarize_node(state: ResumeWorkflowState) -> ResumeWorkflowState:
    """Analisa o currículo e gera resumos de cada secção"""
    print("🤖 [NODE 2] Analisando currículo e gerando resumos...")

    if not state['pdf_text']:
        state['errors'].append("Sem texto para processar")
        state['analyzed_data'] = {}
        return state

    llm = get_llm(temperature=0.3)

    system_prompt = """You are an expert resume analyzer. Extract information and create CONCISE summaries for each section.

Extract the following and respond ONLY with valid JSON:
{
  "full_name": "string",
  "professional_title": "string (infer from experience, NEVER null)",
  "email": "string or null",
  "phone": "string or null",
  "location": "string or null",
  "linkedin": "url or null",
  "github": "url or null",
  "website": "url or null",

  "about_summary": "2-3 sentence professional summary highlighting key strengths and experience",

  "experience_summary": "2-3 sentence summary of professional experience and key roles",
  "experience_items": [
    {
      "company": "string",
      "position": "string",
      "period": "string",
      "description": "1-2 sentence summary"
    }
  ],

  "education_summary": "1-2 sentence summary of academic background",
  "education_items": [
    {
      "institution": "string",
      "degree": "string",
      "period": "string"
    }
  ],

  "skills_summary": "1 sentence highlighting main skill areas",
  "skills": ["skill1", "skill2", "skill3"],

  "languages": [{"language": "string", "level": "string"}] or null,
  "certifications": ["string"] or null,
  "projects": [{"name": "string", "description": "1 sentence"}] or null
}

Keep summaries CONCISE and PROFESSIONAL. Focus on impact and achievements."""

    user_prompt = f"Currículo completo:\n\n{state['pdf_text']}"

    try:
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]

        response = llm.invoke(messages)
        result = json.loads(response.content)

        state['analyzed_data'] = result
        print(f"   ✓ Analisado: {result.get('full_name', 'N/A')}")

    except Exception as e:
        print(f"   ✗ Erro: {e}")
        state['errors'].append(f"Erro na análise: {str(e)}")
        state['analyzed_data'] = {
            "full_name": "Profissional",
            "professional_title": "Profissional Qualificado",
            "about_summary": "Profissional experiente com histórico comprovado de excelência.",
            "experience_summary": "Experiência sólida em diversas áreas.",
            "education_summary": "Formação académica sólida.",
            "skills_summary": "Competências diversificadas.",
            "experience_items": [],
            "education_items": [],
            "skills": []
        }

    state['processing_stage'] = "Currículo analisado"
    return state


# === NODE 3: ESTRUTURA DO WEBSITE ===
def build_website_structure_node(state: ResumeWorkflowState) -> ResumeWorkflowState:
    """Constrói estrutura simplificada do website"""
    print("🏗️  [NODE 3] Construindo estrutura do website...")

    state['website_structure'] = {
        'data': state['analyzed_data']
    }

    state['processing_stage'] = "Website estruturado"
    print("   ✓ Website simplificado criado")

    return state


# === CONSTRUÇÃO DO GRAPH ===
def create_resume_workflow() -> StateGraph:
    """Cria o workflow LangGraph simplificado"""
    workflow = StateGraph(ResumeWorkflowState)

    # Adiciona nodes
    workflow.add_node("extract_pdf", extract_pdf_node)
    workflow.add_node("analyze_and_summarize", analyze_and_summarize_node)
    workflow.add_node("build_website", build_website_structure_node)

    # Define edges (fluxo sequencial)
    workflow.set_entry_point("extract_pdf")
    workflow.add_edge("extract_pdf", "analyze_and_summarize")
    workflow.add_edge("analyze_and_summarize", "build_website")
    workflow.add_edge("build_website", END)

    return workflow.compile()


# === FUNÇÃO PRINCIPAL ===
def process_resume_with_langgraph(pdf_path: str) -> Dict:
    """
    Processa um currículo usando o workflow LangGraph

    Args:
        pdf_path: Caminho para o ficheiro PDF

    Returns:
        Dict com estrutura completa do website
    """
    print("\n" + "="*60)
    print("🚀 INICIANDO WORKFLOW LANGGRAPH")
    print("="*60 + "\n")

    app = create_resume_workflow()

    initial_state = {
        "pdf_path": pdf_path,
        "pdf_text": "",
        "analyzed_data": {},
        "website_structure": {},
        "errors": [],
        "processing_stage": "Iniciado"
    }

    try:
        final_state = app.invoke(initial_state)

        print("\n" + "="*60)
        print(f"✅ WORKFLOW CONCLUÍDO: {final_state['processing_stage']}")
        if final_state['errors']:
            print(f"⚠️  Com {len(final_state['errors'])} avisos")
        print("="*60 + "\n")

        return {
            'success': True,
            'website_structure': final_state['website_structure'],
            'errors': final_state['errors']
        }

    except Exception as e:
        print(f"\n❌ ERRO NO WORKFLOW: {str(e)}\n")
        return {
            'success': False,
            'error': str(e),
            'website_structure': {},
            'errors': [str(e)]
        }
