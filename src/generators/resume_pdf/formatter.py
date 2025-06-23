from src.models import Certification, Contact, Education, Experience, Language, Skill


def format_header(full_name: str, contact: Contact) -> str:
    return f"""{{\\centering
    {{\\Huge {full_name}}}\\\\[0.2cm]
    \\href{{mailto:{contact.email}}}{{{contact.email}}} \\,|\\, 
    \\href{{tel:{contact.phone}}}{{{contact.phone}}} \\,|\\, 
    \\href{{{contact.linkedin}}}{{{contact.linkedin}}}\\\\[0.4cm]
}}"""

def format_summary(summary: str) -> str:
    return f"""{summary}"""

def format_education(education: list[Education]) -> str:
    lines = []
    for edu in education:
        lines.append(f"""\\textbf{{{edu.institution}}}\\\\
\\textit{{{edu.degree} \\,|\\, {edu.startYear} -- {edu.endYear}}}
\\begin{{itemize}}[left=0pt]
    \\item {edu.description}
\\end{{itemize}}
""")
    return "\n".join(lines)

def format_experience(experience: list[Experience]) -> str:
    lines = []
    for exp in experience:
        lines.append(f"""\\textbf{{{exp.company}}}\\\\
\\textit{{{exp.position} \\,|\\, {exp.startDate} -- {exp.endDate or 'Present'}}}
\\begin{{itemize}}[left=0pt]
""")
        for resp in exp.responsibilities:
            lines.append(f"    \\item {resp}")
        lines.append("\\end{itemize}\n")
    return "\n".join(lines)

def format_skills_and_languages(skills: list[Skill], languages: list[Language]) -> str:
    skills_str = ", ".join([f"{skill.name} ({skill.level})" for skill in skills])
    langs_str = ", ".join([f"{lang.name} ({lang.proficiency})" for lang in languages])
    return f"""\\textbf{{Languages:}} {langs_str}.\\\\
\\textbf{{Skills:}} {skills_str}.
"""

def format_certifications(certifications: list[Certification] = None) -> str:
    if not certifications:
        return ""
    lines = []
    for cert in certifications:
        lines.append(f"\\item {cert.name}, {cert.institution} ({cert.year})")
    return "\\begin{itemize}[left=0pt]\n" + "\n".join(lines) + "\n\\end{itemize}"
