from src.models import (
    CapybaraAchievement,
    CapybaraComplementaryEducation,
    CapybaraContact,
    CapybaraEducation,
    CapybaraExperience,
    CapybaraLanguage,
    CapybaraProjectExperience,
)


def escape(text: str) -> str:
    if not text:
        return ""
    return (
        text.replace("&", r"\&")
            .replace("%", r"\%")
            .replace("_", r"\_")
            .replace("$", r"\$")
    )


def format_header(full_name: str) -> str:
    return f"\\textbf{{\\Large {escape(full_name)}}}\\\\\n"


def format_contact(contact: CapybaraContact) -> str:
    return (
        f"{escape(contact.city)}, {escape(contact.country)} $\\cdot$ "
        f"{escape(contact.phone)} $\\cdot$ {escape(contact.email)} $\\cdot$ {escape(contact.linkedin)}\\\\\n"
    )


def format_skills_and_softwares(skills: list[str], softwares: list[str]) -> str:
    items = skills + softwares
    if not items:
        return ""

    section = "\\vspace{0.4cm}\n\\textbf{HABILIDADES Y SOFTWARES}\\\\\n"
    section += "\\begin{tabular}{lll}\n"

    rows = [items[i:i + 3] for i in range(0, len(items), 3)]
    for row in rows:
        col1 = f"$\\bullet$ {escape(row[0])}" if len(row) > 0 else ""
        col2 = f"$\\bullet$ {escape(row[1])}" if len(row) > 1 else ""
        col3 = f"$\\bullet$ {escape(row[2])}" if len(row) > 2 else ""
        section += f"{col1} & {col2} & {col3}\\\\\n"

    section += "\\end{tabular}\n"
    return section

def format_experience(experiences: list[CapybaraExperience]) -> str:
    if not experiences:
        return ""

    section = "\\vspace{0.2cm}\\textbf{EXPERIENCIA LABORAL}\\\\\n"
    for exp in experiences:
        section += f"\\textbf{{{escape(exp.company)}}} \\hfill {escape(exp.startDate)} -- {escape(exp.endDate)}\\\\\n"
        if exp.relevantCompanyData:
            section += f"{escape(exp.relevantCompanyData)}\\\\\n"
        section += f"{escape(exp.position)} \\hfill {escape(exp.city)}, {escape(exp.country)}\\\\\n"
        section += "\\begin{itemize}[leftmargin=*]\n"
        for s in exp.successSentences:
            section += f"\\item {escape(s)}\n"
        section += "\\end{itemize}\\vspace{0.2cm}\n"
    return section


def format_project_experience(projects: CapybaraProjectExperience) -> str:
    if not projects or not projects.experiences:
        return ""

    section = f"\\vspace{{0.2cm}}\\textbf{{{escape(projects.titleSection).upper()}}}\\\\\n"
    for exp in projects.experiences:
        section += f"\\textbf{{{escape(exp.company)}}} \\hfill {escape(exp.startDate)} -- {escape(exp.endDate)}\\\\\n"
        if exp.relevantCompanyData:
            section += f"{escape(exp.relevantCompanyData)}\\\\\n"
        section += f"{escape(exp.position)} \\hfill {escape(exp.city)}, {escape(exp.country)}\\\\\n"
        section += "\\begin{itemize}[leftmargin=*]\n"
        for s in exp.successSentences:
            section += f"\\item {escape(s)}\n"
        section += "\\end{itemize}\\vspace{0.2cm}\n"
    return section


def format_education(education: list[CapybaraEducation]) -> str:
    if not education:
        return ""

    section = "\\vspace{0.2cm}\\textbf{EDUCACIÓN}\\\\\n"
    for ed in education:
        section += f"{escape(ed.degree)}, {escape(ed.institution)} \\hfill {escape(ed.startDate)} -- {escape(ed.endDate)}\\\\\n"
        if ed.relevantEducationData:
            section += f"\\begin{{itemize}}[leftmargin=*]\n\\item {escape(ed.relevantEducationData)}\n\\end{{itemize}}\n"
        section += f"\\hfill {escape(ed.city)}, {escape(ed.country)}\\\\\n"
    return section


def format_achievements(achievements: list[CapybaraAchievement]) -> str:
    if not achievements:
        return ""

    section = "\\vspace{0.4cm}\n\\textbf{RECONOCIMIENTOS \\& BECAS}\\\\\n"
    section += "\\begin{tabularx}{\\textwidth}{Xr}\n"

    for ach in achievements:
        main = f"$\\bullet$ {escape(ach.name)}, {escape(ach.institution)}"
        city = f"{escape(ach.city)}, {escape(ach.country)}"
        section += f"{main} & {escape(ach.date)}\\\\\n"
        section += f" & {city}\\\\\n"

    section += "\\end{tabularx}\n"
    return section



def format_complementary_education(courses: list[CapybaraComplementaryEducation]) -> str:
    if not courses:
        return ""

    section = "\\vspace{0.4cm}\n\\textbf{EDUCACIÓN COMPLEMENTARIA}\\\\\n"
    section += "\\begin{tabularx}{\\textwidth}{Xr}\n"

    for c in courses:
        line = f"$\\bullet$ {escape(c.courseType)}, {escape(c.courseName)}, {escape(c.institution)}"
        city = f"{escape(c.city)}, {escape(c.country)}"
        section += f"{line} & {escape(c.date)}\\\\\n"
        section += f" & {city}\\\\\n"

    section += "\\end{tabularx}\n"
    return section



def format_languages(languages: list[CapybaraLanguage]) -> str:
    if not languages:
        return ""
    langs = ", ".join([f"{escape(l.name)} ({escape(l.proficiency)})" for l in languages])
    return f"\\vspace{{0.4cm}}\n\\textbf{{IDIOMAS}}: {langs}\\\\\n"
