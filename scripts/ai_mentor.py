import os
import pandas as pd
import requests
import json

# Configurações
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBtz3Dq1DuHHKxr6O5KlXtcjggUMo9k-8Q")
BASE_PATH = "data/processed"

def get_progress_summary():
    cursos = pd.read_csv(f"{BASE_PATH}/DIM_CURSOS.csv", sep=';')
    progresso = pd.read_csv(f"{BASE_PATH}/FATO_PROGRESSO.csv", sep=';')
    
    summary = []
    for _, row in cursos.iterrows():
        cid = row['id_curso']
        total = len(progresso[progresso['id_curso'] == cid])
        concluidas = len(progresso[(progresso['id_curso'] == cid) & (progresso['id_status'].isin([1, 4]))])
        summary.append(f"- {row['nome_curso']}: {concluidas}/{total} aulas")
    
    return "\n".join(summary)

def ask_gemini(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }]
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['candidates'][0]['content']['parts'][0]['text']
    else:
        return f"Erro na IA: {response.text}"

def generate_mentor_advice(energy_level):
    progress = get_progress_summary()
    prompt = f"""
    Você é um Mentor de Carreira em Data Science. 
    O aluno Germano está em uma jornada de transição de carreira.
    
    Estado Atual do Progresso:
    {progress}
    
    Nível de Energia do Germano hoje (1-10): {energy_level}
    
    Com base no progresso e na energia dele, dê uma sugestão de estudo específica e motivadora.
    Se a energia for baixa (1-3), sugira algo leve como Inglês ou revisão.
    Se for alta (7-10), sugira avançar em SQL ou Python.
    Seja curto, direto e use um tom profissional mas encorajador.
    """
    return ask_gemini(prompt)

if __name__ == "__main__":
    # Exemplo de uso
    import sys
    energy = sys.argv[1] if len(sys.argv) > 1 else "5"
    print(generate_mentor_advice(energy))
