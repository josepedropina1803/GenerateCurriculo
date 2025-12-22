"""
Workflow LangGraph para processamento inteligente de currículos
Orquestra: Extração PDF → Identificação de Secções → Análise AI → Geração Website
"""
from typing import TypedDict, List, Dict, Annotated
from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import JsonOutputParser
import json

# Importa o extrator de PDF
from src.pdf_extractor import extract_text_from_pdf


# === ESTADO DO WORKFLOW ===
class ResumeWorkflowState(TypedDict):
    """Estado compartilhado entre todos os nodes do workflow"""
    pdf_path: str
    pdf_text: str
    sections_identified: List[Dict]
    analyzed_data: Dict
    website_structure: Dict
    errors: List[str]
    processing_stage: str


# === CONFIGURAÇÃO DO LLM ===
def get_llm(temperature: float = 0.2):
    """Retorna instância do ChatOllama"""
    return ChatOllama(
        model="llama3",
        temperature=temperature,
        base_url="http://localhost:11434",
        format="json"  # Força resposta em JSON
    )


# === NODE 1: EXTRAÇÃO DE PDF ===
def extract_pdf_node(state: ResumeWorkflowState) -> ResumeWorkflowState:
    """
    Extrai texto do PDF usando pdfplumber
    """
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


# === NODE 2: IDENTIFICAÇÃO DE SECÇÕES ===
def identify_sections_node(state: ResumeWorkflowState) -> ResumeWorkflowState:
    """
    Usa LangChain + Ollama para identificar dinamicamente as secções do currículo
    """
    print("🔍 [NODE 2] Identificando secções do currículo...")

    if not state['pdf_text']:
        state['errors'].append("Sem texto para processar")
        state['sections_identified'] = []
        return state

    llm = get_llm(temperature=0.1)

    system_prompt = """You are an expert resume analyzer.
Analyze the resume and identify ALL sections present in the document.

IMPORTANT: Use ONLY the following standardized section IDs when the content exists:
- "home" - Always include (mandatory)
- "about" - About me / Professional summary (if exists)
- "experience" - Work experience / Professional background (MANDATORY - always include)
- "education" - Academic background / Degrees (if exists)
- "skills" - Skills / Competencies / Expertise (if exists)
- "projects" - Projects / Portfolio work (if exists)
- "certifications" - Certifications / Licenses (if exists)
- "languages" - Languages spoken (if exists)
- "publications" - Publications / Research (if exists)
- "awards" - Awards / Achievements (if exists)
- "contact" - Contact information (MANDATORY - always include)

Respond ONLY with valid JSON in this format:
{
  "sections": [
    {"id": "home", "title": "Home", "icon": "🏠", "order": 1},
    {"id": "about", "title": "About", "icon": "👤", "order": 2},
    {"id": "experience", "title": "Experience", "icon": "💼", "order": 3},
    {"id": "contact", "title": "Contact", "icon": "📧", "order": 7}
  ]
}

Rules:
1. ALWAYS include: "home", "experience", "contact"
2. Only include other sections if they have actual content in the resume
3. Order should be logical (home first, contact last)
4. Use appropriate icons for each section
5. Titles should be in formal English"""

    user_prompt = f"Currículo:\n\n{state['pdf_text'][:3000]}"  # Primeiros 3000 chars

    try:
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]

        response = llm.invoke(messages)
        result = json.loads(response.content)

        state['sections_identified'] = result.get('sections', [])
        print(f"   ✓ Identificadas {len(state['sections_identified'])} secções")

    except Exception as e:
        print(f"   ✗ Error: {e}")
        state['errors'].append(f"Error identifying sections: {str(e)}")
        # Fallback to mandatory sections only
        state['sections_identified'] = [
            {"id": "home", "title": "Home", "icon": "🏠", "order": 1},
            {"id": "experience", "title": "Experience", "icon": "💼", "order": 2},
            {"id": "contact", "title": "Contact", "icon": "📧", "order": 3}
        ]

    state['processing_stage'] = "Secções identificadas"
    return state


# === NODE 3: ANÁLISE DETALHADA ===
def analyze_resume_node(state: ResumeWorkflowState) -> ResumeWorkflowState:
    """
    Analisa o currículo e extrai dados estruturados usando LangChain
    """
    print("🤖 [NODE 3] Analisando currículo com IA...")

    llm = get_llm(temperature=0.3)

    system_prompt = """You are an expert resume/CV analyzer for ALL professional fields.
Extract ALL relevant information from the resume in structured JSON format.

IMPORTANT:
- "professional_title" is MANDATORY - infer an appropriate professional title based on experience
- "professional_summary" is MANDATORY - create a 2-3 sentence summary based on experience and education
- Extract "projects" as objects with "name", "description", and relevant details (e.g., "technologies" for tech fields, "outcomes" for other fields)
- Adapt field names to the professional context (e.g., "technologies" for IT, "techniques" for healthcare, "methods" for research)

Respond ONLY with valid JSON following this schema:
{
  "full_name": "string",
  "professional_title": "string (NEVER null - infer from experience)",
  "professional_summary": "string 2-3 sentences (NEVER null - create based on profile)",
  "email": "string or null",
  "phone": "string or null",
  "location": "string or null",
  "linkedin": "url or null",
  "github": "url or null",
  "website": "url or null",
  "experience": [
    {
      "company": "string (or organization/institution)",
      "position": "string (or role/title)",
      "period": "string",
      "description": "string"
    }
  ],
  "education": [
    {
      "institution": "string",
      "degree": "string (or course/program)",
      "period": "string",
      "description": "string or null"
    }
  ],
  "skills": ["string"] or [],
  "languages": [
    {
      "language": "string",
      "level": "string"
    }
  ] or [],
  "certifications": ["string"] or null,
  "projects": [
    {
      "name": "string",
      "description": "string",
      "details": ["string"] (adapt to field: technologies, techniques, methods, tools, etc.)
    }
  ] or [],
  "publications": ["string"] or null,
  "awards": ["string"] or null
}

Be precise and complete. For MANDATORY fields, NEVER use null."""

    user_prompt = f"Currículo completo:\n\n{state['pdf_text']}"

    try:
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]

        response = llm.invoke(messages)
        result = json.loads(response.content)

        state['analyzed_data'] = result
        print(f"   ✓ Data extracted: {result.get('full_name', 'N/A')}")

    except Exception as e:
        print(f"   ✗ Error: {e}")
        state['errors'].append(f"Analysis error: {str(e)}")
        state['analyzed_data'] = {
            "full_name": "Professional",
            "professional_title": "Qualified Professional",
            "professional_summary": "Experienced professional with a proven track record of excellence.",
            "experience": [],
            "education": [],
            "skills": []
        }

    state['processing_stage'] = "Currículo analisado"
    return state


# === NODE 4: GERAÇÃO DE CONTEÚDO ADICIONAL ===
def generate_content_node(state: ResumeWorkflowState) -> ResumeWorkflowState:
    """
    Gera conteúdo adicional para o website (bio, headlines, call-to-action)
    """
    print("✨ [NODE 4] Gerando conteúdo adicional...")

    llm = get_llm(temperature=0.8)

    name = state['analyzed_data'].get('full_name', 'Professional')
    title = state['analyzed_data'].get('professional_title', 'Professional')
    experience = state['analyzed_data'].get('experience', [])
    education = state['analyzed_data'].get('education', [])
    projects = state['analyzed_data'].get('projects', [])

    system_prompt = """You are a professional copywriter specialized in creating PREMIUM content for professional websites across ALL industries.
Create HIGHLY IMPACTFUL, persuasive, and memorable text that highlights achievements and unique value.

IMPORTANT:
- "headline" must be POWERFUL and unique, never generic
- "short_bio" should highlight concrete achievements, not just characteristics
- "long_bio" should tell an engaging story of professional growth
- "call_to_action" should be specific and inviting
- Adapt language to the professional field (avoid tech jargon for non-tech professionals)

Respond ONLY with valid JSON:
{
  "headline": "UNIQUE impactful phrase of 8-12 words (avoid clichés like 'passion for excellence')",
  "short_bio": "1 paragraph of 60-80 words focused on RESULTS and measurable achievements",
  "long_bio": "2-3 paragraphs (180-220 words) telling the professional JOURNEY with specific details",
  "call_to_action": "Specific inviting phrase (max 50 characters)",
  "meta_description": "Attractive SEO description (max 155 characters)"
}

Use numbers, specific achievements, and concrete accomplishments. Adapt terminology to the professional field."""

    user_prompt = f"""Professional: {name}
Title: {title}

Experience:
{json.dumps(experience[:3], ensure_ascii=False, indent=2)}

Education:
{json.dumps(education[:2], ensure_ascii=False, indent=2)}

Projects:
{json.dumps(projects[:3], ensure_ascii=False, indent=2) if projects else "No projects listed"}

Create PREMIUM and highly impactful content that showcases this professional's unique achievements."""

    try:
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]

        response = llm.invoke(messages)
        result = json.loads(response.content)

        # Merge com dados analisados
        state['analyzed_data'].update(result)
        print(f"   ✓ Conteúdo gerado: {result.get('headline', '')[:50]}...")

    except Exception as e:
        print(f"   ✗ Error: {e}")
        state['errors'].append(f"Content generation error: {str(e)}")
        # Fallback to basic content
        state['analyzed_data'].update({
            "headline": f"{title} - Delivering Excellence",
            "short_bio": "Dedicated professional with a proven track record of success.",
            "call_to_action": "Let's work together"
        })

    state['processing_stage'] = "Conteúdo gerado"
    return state


# === NODE 5: ESTRUTURA DO WEBSITE ===
def build_website_structure_node(state: ResumeWorkflowState) -> ResumeWorkflowState:
    """
    Constrói a estrutura final do website baseada nas secções identificadas
    """
    print("🏗️  [NODE 5] Construindo estrutura do website...")

    # Combina secções com dados analisados
    state['website_structure'] = {
        'sections': state['sections_identified'],
        'data': state['analyzed_data'],
        'navbar': {
            'enabled': True,
            'sticky': True,
            'sections': state['sections_identified']
        }
    }

    state['processing_stage'] = "Website estruturado"
    print(f"   ✓ Website com {len(state['sections_identified'])} secções na navbar")

    return state


# === CONSTRUÇÃO DO GRAPH ===
def create_resume_workflow() -> StateGraph:
    """
    Cria o workflow LangGraph para processamento de currículos
    """
    # Define o graph
    workflow = StateGraph(ResumeWorkflowState)

    # Adiciona nodes
    workflow.add_node("extract_pdf", extract_pdf_node)
    workflow.add_node("identify_sections", identify_sections_node)
    workflow.add_node("analyze_resume", analyze_resume_node)
    workflow.add_node("generate_content", generate_content_node)
    workflow.add_node("build_website", build_website_structure_node)

    # Define edges (fluxo sequencial)
    workflow.set_entry_point("extract_pdf")
    workflow.add_edge("extract_pdf", "identify_sections")
    workflow.add_edge("identify_sections", "analyze_resume")
    workflow.add_edge("analyze_resume", "generate_content")
    workflow.add_edge("generate_content", "build_website")
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

    # Cria o workflow
    app = create_resume_workflow()

    # Estado inicial
    initial_state = {
        "pdf_path": pdf_path,
        "pdf_text": "",
        "sections_identified": [],
        "analyzed_data": {},
        "website_structure": {},
        "errors": [],
        "processing_stage": "Iniciado"
    }

    # Executa o workflow
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
