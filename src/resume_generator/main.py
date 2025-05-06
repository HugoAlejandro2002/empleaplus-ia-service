#!/usr/bin/env python
import sys
import warnings
from datetime import datetime

from resume_generator.crew import ResumeGenerator

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        "personal_data": {
            "full_name": "Ana María Gutiérrez",
            "email": "ana@example.com",
            "phone": "+591 71234567",
            "country": "Bolivia",
            "city": "La Paz",
            "birth_date": "1998-03-14"
        },
        "education": [
            {
                "institution": "Universidad Privada Boliviana",
                "degree": "Ingeniería de Sistemas",
                "start_year": "2018",
                "end_year": "2023",
                "notes": "Graduada con honores"
            }
        ],
        "experience": [
            {
                "project_name": "Feria de Ciencia",
                "role": "Diseñé el prototipo de un sistema solar",
                "achievements": "Fuimos finalistas del concurso",
                "teamwork": "Lideré un grupo de 3 personas",
                "coordination": "Área de Logística",
                "presentation": "Jurado universitario"
            }
        ],
        "skills": [
            { "skill": "Excel", "level": "Advanced" },
            { "skill": "Canva", "level": "Intermediate" }
        ],
        "languages": [
            { "language": "English", "level": "Intermediate" }
        ],
        "certifications": [
            {
                "course": "Curso de Introducción a Git",
                "provider": "Platzi",
                "year": "2022",
                "certificate": "https://example.com/git-cert"
            }
        ],
        "professional_summary": {
            "summary": "Soy una estudiante apasionada por la tecnología, con experiencia en proyectos escolares y habilidades en herramientas digitales. Estoy motivada por crecer profesionalmente y aportar valor a un equipo de trabajo."
        }
    }
    try:
        ans = ResumeGenerator().crew().kickoff(inputs=inputs)
        print(ans.raw)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        ResumeGenerator().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        ResumeGenerator().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }
    try:
        ResumeGenerator().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
