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
    return (
        "\\begin{center}\n"
        "\\fontsize{16}{18}\\selectfont "
        f"\\textbf{{{escape(full_name.upper())}}}\\\\\n"
        "\\end{center}\n"
    )


def format_contact(contact: CapybaraContact) -> str:
    return (
        "\\begin{center}\n"
        f"{escape(contact.city)}, {escape(contact.country)} $\\cdot$ "
        f"{escape(contact.phone)} $\\cdot$ {escape(contact.email)} $\\cdot$ "
        f"{escape(contact.linkedin)}\\\\\n"
        "\\end{center}\n"
    )


def format_skills_and_softwares(skills: list[str], softwares: list[str]) -> str:
    ns = len(skills)
    nf = len(softwares)
    if ns + nf == 0:
        return ""
    # número de filas = máximo de mitades de cada lista
    half_s = (ns + 1) // 2
    half_f = (nf + 1) // 2
    rows = max(half_s, half_f)

    section  = "\\vspace{0.2cm}\n"
    section += "\\noindent\\textbf{HABILIDADES \\& SOFTWARES}\\\\\n"
    section += "\\noindent\\begin{tabularx}{\\textwidth}{XXXX}\n"

    for i in range(rows):
        # extraemos skill columna 1 y 2
        s1 = skills[i] if i < ns else ""
        s2 = skills[i + half_s] if i + half_s < ns else ""
        # extraemos software columna 3 y 4
        f1 = softwares[i] if i < nf else ""
        f2 = softwares[i + half_f] if i + half_f < nf else ""

        # convertimos a bullets o cadena vacía
        c1 = f"\\textbullet\\ {escape(s1)}" if s1 else ""
        c2 = f"\\textbullet\\ {escape(s2)}" if s2 else ""
        c3 = f"\\textbullet\\ {escape(f1)}" if f1 else ""
        c4 = f"\\textbullet\\ {escape(f2)}" if f2 else ""

        section += f"{c1} & {c2} & {c3} & {c4}\\\\\n"

    section += "\\end{tabularx}\n"
    return section


def format_experience(experiences: list[CapybaraExperience]) -> str:
    if not experiences:
        return ""
    section = "\\vspace{0.2cm}\n"
    section += "\\noindent\\textbf{EXPERIENCIA LABORAL}\\\\\n"
    for exp in experiences:
        # 1) Empresa + fechas
        section += "\\noindent\\begin{tabularx}{\\textwidth}{@{}Xr@{}}\n"
        section += (
            f"\\textbf{{{escape(exp.company)}}} & "
            f"{escape(exp.startDate)} -- {escape(exp.endDate)}\\\\\n"
        )
        section += "\\end{tabularx}\n"
        # 2) Descripción breve
        if exp.relevantCompanyData:
            section += "\\noindent\\begin{tabularx}{\\textwidth}{@{}Xr@{}}\n"
            section += f"{escape(exp.relevantCompanyData)} & \\\\\n"
            section += "\\end{tabularx}\n"
        # 3) Cargo + ubicación
        section += "\\noindent\\begin{tabularx}{\\textwidth}{@{}Xr@{}}\n"
        section += (
            f"{escape(exp.position)} & "
            f"{escape(exp.city)}, {escape(exp.country)}\\\\\n"
        )
        section += "\\end{tabularx}\n"
        # 4) Bullets uniformes
        section += "\\noindent\\begin{itemize}[nosep,leftmargin=*,labelindent=0pt]\n"
        for s in exp.successSentences:
            section += f"  \\item {escape(s)}\n"
        section += "\\end{itemize}\n"
    return section


def format_project_experience(projects: CapybaraProjectExperience) -> str:
    if not projects or not projects.experiences:
        return ""
    section = "\\vspace{0.2cm}\n"
    section += (
        "\\noindent\\textbf{" + escape(projects.titleSection).upper() + "}\\\\\n"
    )
    for exp in projects.experiences:
        # misma estructura que experiencia
        section += "\\noindent\\begin{tabularx}{\\textwidth}{@{}Xr@{}}\n"
        section += (
            f"\\textbf{{{escape(exp.company)}}} & "
            f"{escape(exp.startDate)} -- {escape(exp.endDate)}\\\\\n"
        )
        section += "\\end{tabularx}\n"
        if exp.relevantCompanyData:
            section += "\\noindent\\begin{tabularx}{\\textwidth}{@{}Xr@{}}\n"
            section += f"{escape(exp.relevantCompanyData)} & \\\\\n"
            section += "\\end{tabularx}\n"
        section += "\\noindent\\begin{tabularx}{\\textwidth}{@{}Xr@{}}\n"
        section += (
            f"{escape(exp.position)} & "
            f"{escape(exp.city)}, {escape(exp.country)}\\\\\n"
        )
        section += "\\end{tabularx}\n"
        section += "\\noindent\\begin{itemize}[nosep,leftmargin=*,labelindent=0pt]\n"
        for s in exp.successSentences:
            section += f"  \\item {escape(s)}\n"
        section += "\\end{itemize}\n"
    return section


def format_education(education: list[CapybaraEducation]) -> str:
    if not education:
        return ""
    section  = "\\vspace{0.2cm}\n"
    section += "\\noindent \\textbf{EDUCACIÓN}\\\\\n"
    for ed in education:
        section += "\\noindent \\begin{tabularx}{\\textwidth}{@{}Xr@{}}\n"
        section += (
            f"{escape(ed.degree)}, {escape(ed.institution)}"
            f" & {escape(ed.startDate)} -- {escape(ed.endDate)}\\\\\n"
        )
        left = f"\\textbullet\\ {escape(ed.relevantEducationData)}" if ed.relevantEducationData else ""
        section += f"{left} & {escape(ed.city)}, {escape(ed.country)}\\\\\n"
        section += "\\end{tabularx}\n"
    return section


def format_achievements(achievements: list[CapybaraAchievement]) -> str:
    if not achievements:
        return ""
    section  = "\\vspace{0.2cm}\n"
    section += "\\noindent\\textbf{RECONOCIMIENTOS \\& BECAS}\\\\\n"
    for ach in achievements:
        section += "\\noindent\\begin{tabularx}{\\textwidth}{@{}Xr@{}}\n"
        section += (
            f"\\textbullet\\ {escape(ach.name)}, {escape(ach.institution)} & "
            f"{escape(ach.country)}, {escape(ach.date)}\\\\\n"
        )
        section += "\\end{tabularx}\n"
    return section


def format_complementary_education(
    courses: list[CapybaraComplementaryEducation]
) -> str:
    if not courses:
        return ""
    section  = "\\vspace{0.2cm}\n"
    section += "\\noindent\\textbf{EDUCACIÓN COMPLEMENTARIA}\\\\\n"
    for c in courses:
        section += "\\noindent\\begin{tabularx}{\\textwidth}{@{}Xr@{}}\n"
        section += (
            f"\\textbullet\\ {escape(c.courseType)}, {escape(c.courseName)}, "
            f"{escape(c.institution)} & "
            f"{escape(c.country)}, {escape(c.date)}\\\\\n"
        )
        section += "\\end{tabularx}\n"
    return section

def format_languages(languages: list[CapybaraLanguage]) -> str:
    if not languages:
        return ""
    langs = ", ".join(
        [f"{escape(lang.name)} ({escape(lang.certification if lang.certification else lang.proficiency)})" for lang in languages]
    )
    section = "\\vspace{0.2cm}\n"
    section += f"\\noindent\\textbf{{IDIOMAS}}: {langs}\\\\\n"
    return section
