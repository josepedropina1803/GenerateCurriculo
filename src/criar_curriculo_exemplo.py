"""
Script para criar um currículo de exemplo em PDF
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime

def criar_curriculo_exemplo():
    """Cria um PDF de currículo de exemplo"""

    filename = f"uploads/curriculo_exemplo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    # Cria o documento
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18,
    )

    # Container para os elementos
    story = []

    # Estilos
    styles = getSampleStyleSheet()

    # Estilo personalizado para o nome
    style_nome = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    style_cargo = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.HexColor('#3498db'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )

    style_heading = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )

    style_normal = styles['Normal']

    # === CABEÇALHO ===
    story.append(Paragraph("Pedro Miguel Silva", style_nome))
    story.append(Paragraph("Engenheiro de Software Senior", style_cargo))
    story.append(Spacer(1, 0.2*inch))

    # Informações de contacto
    contacto_data = [
        ['Email:', 'pedro.silva@email.com', 'Telefone:', '+351 912 345 678'],
        ['LinkedIn:', 'linkedin.com/in/pedrosilva', 'GitHub:', 'github.com/pedrosilva'],
        ['Localização:', 'Lisboa, Portugal', '', '']
    ]

    contacto_table = Table(contacto_data, colWidths=[1.2*inch, 2*inch, 1.2*inch, 2*inch])
    contacto_table.setStyle(TableStyle([
        ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 9),
        ('FONT', (1, 0), (1, -1), 'Helvetica', 9),
        ('FONT', (2, 0), (2, -1), 'Helvetica-Bold', 9),
        ('FONT', (3, 0), (3, -1), 'Helvetica', 9),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#555555')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(contacto_table)
    story.append(Spacer(1, 0.3*inch))

    # === RESUMO PROFISSIONAL ===
    story.append(Paragraph("Resumo Profissional", style_heading))
    resumo = """Engenheiro de Software com mais de 8 anos de experiência no desenvolvimento
    de aplicações web escaláveis e sistemas distribuídos. Especialista em arquiteturas cloud-native,
    Python, JavaScript e DevOps. Histórico comprovado de liderança técnica em equipas ágeis e
    entrega de projetos de alto impacto para empresas multinacionais."""
    story.append(Paragraph(resumo, style_normal))
    story.append(Spacer(1, 0.2*inch))

    # === EXPERIÊNCIA PROFISSIONAL ===
    story.append(Paragraph("Experiência Profissional", style_heading))

    # Experiência 1
    story.append(Paragraph("<b>Senior Software Engineer</b> - TechCorp International", style_normal))
    story.append(Paragraph("<i>Janeiro 2021 - Presente</i>", style_normal))
    exp1 = """• Liderou equipa de 5 desenvolvedores na criação de plataforma de e-commerce com 1M+ usuários<br/>
    • Implementou arquitetura de microserviços usando Docker, Kubernetes e AWS<br/>
    • Reduziu tempo de deploy em 60% através de pipelines CI/CD automatizados<br/>
    • Melhorou performance da aplicação em 40% através de otimização de queries e caching"""
    story.append(Paragraph(exp1, style_normal))
    story.append(Spacer(1, 0.15*inch))

    # Experiência 2
    story.append(Paragraph("<b>Full Stack Developer</b> - StartupXYZ", style_normal))
    story.append(Paragraph("<i>Março 2018 - Dezembro 2020</i>", style_normal))
    exp2 = """• Desenvolveu aplicação SaaS de gestão de projetos usando React, Node.js e PostgreSQL<br/>
    • Integrou sistema de pagamentos e faturação automática com Stripe<br/>
    • Implementou testes automatizados aumentando cobertura de código para 85%<br/>
    • Colaborou com UX designers para melhorar experiência do utilizador"""
    story.append(Paragraph(exp2, style_normal))
    story.append(Spacer(1, 0.15*inch))

    # Experiência 3
    story.append(Paragraph("<b>Junior Developer</b> - WebSolutions Lda", style_normal))
    story.append(Paragraph("<i>Junho 2016 - Fevereiro 2018</i>", style_normal))
    exp3 = """• Desenvolveu websites corporativos e aplicações web usando Python/Django<br/>
    • Colaborou na manutenção e evolução de sistemas legados<br/>
    • Participou em code reviews e implementou boas práticas de desenvolvimento<br/>
    • Prestou suporte técnico a clientes e resolveu bugs críticos"""
    story.append(Paragraph(exp3, style_normal))
    story.append(Spacer(1, 0.2*inch))

    # === FORMAÇÃO ACADÉMICA ===
    story.append(Paragraph("Formação Académica", style_heading))

    story.append(Paragraph("<b>Mestrado em Engenharia Informática</b>", style_normal))
    story.append(Paragraph("Instituto Superior Técnico, Universidade de Lisboa", style_normal))
    story.append(Paragraph("<i>2014 - 2016</i>", style_normal))
    story.append(Paragraph("Especialização em Sistemas Distribuídos e Cloud Computing", style_normal))
    story.append(Spacer(1, 0.1*inch))

    story.append(Paragraph("<b>Licenciatura em Ciências da Computação</b>", style_normal))
    story.append(Paragraph("Faculdade de Ciências, Universidade de Lisboa", style_normal))
    story.append(Paragraph("<i>2011 - 2014</i>", style_normal))
    story.append(Spacer(1, 0.2*inch))

    # === COMPETÊNCIAS TÉCNICAS ===
    story.append(Paragraph("Competências Técnicas", style_heading))

    competencias = """<b>Linguagens:</b> Python, JavaScript/TypeScript, Java, Go, SQL<br/>
    <b>Frameworks:</b> Django, Flask, React, Node.js, Express, FastAPI<br/>
    <b>Cloud & DevOps:</b> AWS, Docker, Kubernetes, Jenkins, GitLab CI/CD, Terraform<br/>
    <b>Bases de Dados:</b> PostgreSQL, MongoDB, Redis, Elasticsearch<br/>
    <b>Ferramentas:</b> Git, Linux, Nginx, RabbitMQ, Grafana, Prometheus<br/>
    <b>Metodologias:</b> Agile, Scrum, TDD, Microservices, REST APIs"""
    story.append(Paragraph(competencias, style_normal))
    story.append(Spacer(1, 0.2*inch))

    # === CERTIFICAÇÕES ===
    story.append(Paragraph("Certificações", style_heading))
    certs = """• AWS Certified Solutions Architect - Associate (2022)<br/>
    • Certified Kubernetes Administrator (CKA) (2021)<br/>
    • Professional Scrum Master I (PSM I) (2020)"""
    story.append(Paragraph(certs, style_normal))
    story.append(Spacer(1, 0.2*inch))

    # === IDIOMAS ===
    story.append(Paragraph("Idiomas", style_heading))
    idiomas = """• Português - Nativo<br/>
    • Inglês - Fluente (C1)<br/>
    • Espanhol - Intermédio (B1)"""
    story.append(Paragraph(idiomas, style_normal))

    # Constrói o PDF
    doc.build(story)

    return filename

if __name__ == '__main__':
    filename = criar_curriculo_exemplo()
    print(f"✅ Currículo de exemplo criado: {filename}")
