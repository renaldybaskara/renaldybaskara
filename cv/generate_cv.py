#!/usr/bin/env python3
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "Muhammad_Renaldy_Baskara_CV.pdf"
navy, amber, slate, rule = colors.HexColor('#0B1628'), colors.HexColor('#D89519'), colors.HexColor('#47556B'), colors.HexColor('#C9CED5')
styles = getSampleStyleSheet()
name = ParagraphStyle('Name', parent=styles['Title'], fontName='Helvetica-Bold', fontSize=23, leading=25, textColor=navy, alignment=TA_LEFT, spaceAfter=2)
headline = ParagraphStyle('Headline', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10.5, leading=13, textColor=slate, spaceAfter=4)
body = ParagraphStyle('Body', parent=styles['Normal'], fontName='Helvetica', fontSize=8.65, leading=11.3, textColor=navy, spaceAfter=3)
small = ParagraphStyle('Small', parent=body, fontSize=7.5, leading=9)
section = ParagraphStyle('Section', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=10.2, leading=12, textColor=navy, spaceBefore=7, spaceAfter=4, borderWidth=0, borderPadding=0)
role = ParagraphStyle('Role', parent=body, fontName='Helvetica-Bold', fontSize=9.5, leading=11)
project = ParagraphStyle('Project', parent=body, fontSize=8.1, leading=10.4)

def heading(text):
    return [Paragraph(text.upper(), section), Table([['']], colWidths=[178*mm], rowHeights=[0.3*mm], style=TableStyle([('BACKGROUND',(0,0),(-1,-1),rule),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0)])), Spacer(1, 2.5*mm)]

def role_row(title, dates, employer, description=''):
    left = [Paragraph(title, role), Paragraph(employer, ParagraphStyle('Employer', parent=body, fontName='Helvetica-Bold', textColor=slate))]
    if description: left.append(Paragraph(description, body))
    return KeepTogether([Table([[left, Paragraph(dates, role)]], colWidths=[139*mm,39*mm], style=TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('ALIGN',(1,0),(1,0),'RIGHT'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)])), Spacer(1,1.4*mm)])

story = [Paragraph('Muhammad Renaldy Baskara', name), Paragraph('Senior Backend Engineer | Payment Gateway | Golang | ISO8583', headline),
         Paragraph('<b>LinkedIn:</b> <link href="https://www.linkedin.com/in/mrenaldybaskara">linkedin.com/in/mrenaldybaskara</link> &nbsp; | &nbsp; <b>Upwork:</b> <link href="https://www.upwork.com/freelancers/~01356ddc4dbcc68cb0">upwork.com/freelancers/~01356ddc4dbcc68cb0</link>', small), Spacer(1,1*mm)]
story += heading('Professional Summary')
story.append(Paragraph('Backend engineer focused on secure payment systems, scalable APIs, and high-concurrency applications. Helps banking and fintech companies build reliable backend systems that process thousands of transactions efficiently. Currently IT Manager at Bank Rakyat Indonesia (BRI), leading frontend and backend developer squads developing payment systems that support over 200,000 EDC terminals and acquiring infrastructure.', body))
story += heading('Core Competencies')
items = ['Payment Gateway Development','Banking &amp; Fintech Systems','REST APIs &amp; Microservices','System Architecture','High-Concurrency Backend Systems','SaaS Development and Deployment','Backend Implementation Review','SQL Performance Review']
cells = [[Paragraph('- '+items[i],body),Paragraph('- '+items[i+1],body)] for i in range(0,len(items),2)]
story.append(Table(cells,colWidths=[89*mm,89*mm],style=TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),4),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)])))
story += heading('Professional Experience')
story.append(role_row('IT Manager','April 2024 - Present','Bank Rakyat Indonesia (BRI)','Leads frontend and backend developer squads developing payment systems that support over 200,000 EDC terminals and acquiring infrastructure.'))
story.append(role_row('IT Junior Manager','April 2021 - April 2024','Bank Rakyat Indonesia (BRI)'))
story += heading('Selected Projects')
projects=[('Payment App for EDC Merchant BRI','Payment application supporting BRI merchant EDC use cases within the 200,000+ EDC ecosystem.'),('Web Monitoring E-Channel','Web monitoring solution for e-channel operations.'),('Financial Tracker for Private','Private personal financial tracking application.'),('Booking Calendar','Calendar and booking management application.'),('Vehicle Management App','Vehicle management application using Laravel Sanctum and C# WinForms.')]
proj_cells=[]
for i in range(0,len(projects),2):
    row=[]
    for title,desc in projects[i:i+2]: row.append(Paragraph(f'<b>{title}</b><br/>{desc}',project))
    if len(row)==1: row.append('')
    proj_cells.append(row)
story.append(Table(proj_cells,colWidths=[89*mm,89*mm],style=TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),1),('BOTTOMPADDING',(0,0),(-1,-1),3)])))
story += heading('Technical Skills')
skills=[('Languages','Golang, PHP, Node.js, React.js, TypeScript, Java, Rust'),('Data & Messaging','MySQL, PostgreSQL, Redis, RabbitMQ'),('Platform','Docker, Kubernetes, Linux'),('Architecture','Clean Architecture, Microservices, REST APIs, System Architecture'),('Domain','ISO8583, Payment Gateway, FinTech, Web Development, System Analysis, Android App')]
story.append(Table([[Paragraph(f'<b>{k}</b>',body),Paragraph(v,body)] for k,v in skills],colWidths=[34*mm,144*mm],style=TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)])))
story += heading('Availability')
story.append(Table([[Paragraph('Seeking remote opportunities. Open to part-time and full-time work. Target roles: Senior Backend Engineer, Frontend Engineer, Full-Stack Developer, Software Engineer, Technical Lead, IT/Engineering Manager.',body)]],colWidths=[178*mm],style=TableStyle([('LINEBEFORE',(0,0),(0,-1),2,amber),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)])))

doc=SimpleDocTemplate(str(OUT),pagesize=A4,rightMargin=16*mm,leftMargin=16*mm,topMargin=13*mm,bottomMargin=12*mm,title='Muhammad Renaldy Baskara CV',author='Muhammad Renaldy Baskara',subject='Senior Backend Engineer | Payment Gateway | Golang | ISO8583')
doc.build(story)
print(OUT)
