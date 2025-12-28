import pandas as pd
import os
import re
from datetime import datetime

def load_data():
    base_path = "data/processed"
    cursos = pd.read_csv(f"{base_path}/DIM_CURSOS.csv", sep=';')
    progresso = pd.read_csv(f"{base_path}/FATO_PROGRESSO.csv", sep=';')
    status = pd.read_csv(f"{base_path}/DIM_STATUS.csv", sep=';')
    aulas = pd.read_csv(f"{base_path}/DIM_AULAS.csv", sep=';')
    return cursos, progresso, status, aulas

def calculate_metrics(cursos, progresso, status, aulas):
    # Mapear status de conclusão (Aprovado=1, Concluído=4)
    concluidos_ids = [1, 4]
    
    # Total de aulas por curso (da FATO_PROGRESSO, pois DIM_AULAS não tem id_curso)
    total_aulas_por_curso = progresso.groupby('id_curso').size().to_dict()
    
    # Aulas concluídas por curso
    concluidas_por_curso = progresso[progresso['id_status'].isin(concluidos_ids)].groupby('id_curso').size().to_dict()
    
    metrics = []
    total_geral_aulas = 0
    total_geral_concluidas = 0
    
    for _, row in cursos.iterrows():
        cid = row['id_curso']
        nome = row['nome_curso']
        trilha = row['trilha_origem']
        
        total = total_aulas_por_curso.get(cid, 0)
        concluidas = concluidas_por_curso.get(cid, 0)
        percent = (concluidas / total * 100) if total > 0 else 0
        
        status_emoji = "🔵 Iniciando"
        if percent >= 100: status_emoji = "🟢 Concluído"
        elif percent > 0: status_emoji = "🟡 Em andamento"
        
        metrics.append({
            'Trilha': f"**{trilha}**",
            'Curso': nome,
            'Total Aulas': total,
            'Concluídas': concluidas,
            'Progresso': f"**{percent:.0f}%**",
            'Status': status_emoji
        })
        
        total_geral_aulas += total
        total_geral_concluidas += concluidas
        
    return metrics, total_geral_aulas, total_geral_concluidas

def generate_status_cards(total_aulas, total_concluidas, percent_geral):
    color = "green" if percent_geral > 70 else "yellow" if percent_geral > 30 else "blue"
    cards = f"""
<div align="center">
  <img src="https://img.shields.io/badge/Progresso_Total-{percent_geral:.1f}%25-{color}?style=for-the-badge&logo=target" />
  <img src="https://img.shields.io/badge/Aulas_Concluídas-{total_concluidas}/{total_aulas}-brightgreen?style=for-the-badge&logo=book" />
  <img src="https://img.shields.io/badge/Status-Ativo-orange?style=for-the-badge&logo=clock" />
</div>
"""
    return cards

def generate_mermaid_charts(metrics, progresso, modulos):
    # Gráfico de Pizza Geral
    pie_chart = "```mermaid\npie title Distribuição de Aulas Concluídas\n"
    for m in metrics:
        trilha_nome = m['Trilha'].replace('*', '')
        pie_chart += f'    "{trilha_nome}" : {m["Concluídas"]}\n'
    pie_chart += "```\n"
    
    # Gráfico de Barras por Módulo usando Gantt simplificado e compatível
    bar_chart = "### 📊 Detalhamento por Módulo (Progresso %)\n```mermaid\ngantt\n    title Progresso dos Módulos\n    dateFormat  YYYY-MM-DD\n    section Módulos\n"
    
    # Calcular progresso por módulo
    mod_progress = progresso.groupby('id_modulo').agg(
        total=('id_aula', 'count'),
        concluidas=('id_status', lambda x: x.isin([1, 4]).sum())
    ).reset_index()
    
    # Join com nomes dos módulos
    mod_progress = mod_progress.merge(modulos[['id_modulo', 'nome_modulo']], on='id_modulo')
    
    for _, row in mod_progress.head(10).iterrows():
        nome = row['nome_modulo'] if pd.notnull(row['nome_modulo']) and row['nome_modulo'] != "" else f"Módulo {row['id_modulo']}"
        # Limpar caracteres especiais que quebram o Mermaid
        nome = nome.replace(':', '-').replace('(', '').replace(')', '')
        percent = int((row['concluidas'] / row['total'] * 100)) if row['total'] > 0 else 0
        
        # Usar uma sintaxe de Gantt mais robusta: nome : status, data_inicio, data_fim
        # Como queremos apenas barras de progresso, usamos datas fixas e o percentual no nome
        bar_chart += f"    {nome} ({percent}%) :active, 2025-01-01, {percent}d\n"
        
    bar_chart += "```\n"
    return pie_chart, bar_chart

def generate_markdown_table(metrics):
    header = "| Trilha | Curso | Total Aulas | Concluídas | Progresso | Status |\n"
    separator = "|--------|-------|------------|------------|-----------|--------|\n"
    rows = ""
    for m in metrics:
        rows += f"| {m['Trilha']} | {m['Curso']} | {m['Total Aulas']} | {m['Concluídas']} | {m['Progresso']} | {m['Status']} |\n"
    return header + separator + rows

def check_and_move_certificates(metrics):
    # Lógica para mover certificados de in-progress para completed
    # Simulação: em um ambiente real, buscaria arquivos .pdf/.png com o nome do curso
    for m in metrics:
        if m['Status'] == "🟢 Concluído":
            curso_slug = m['Curso'].lower().replace(' ', '_')
            source = f"certificates/in-progress/{curso_slug}.pdf"
            dest = f"certificates/completed/{curso_slug}.pdf"
            if os.path.exists(source):
                os.rename(source, dest)
                print(f"Certificado de {m['Curso']} movido para concluídos!")

def update_readme(table_content, total_info, pie_chart, bar_chart, cards):
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Atualizar a tabela de progresso
    start_marker = "## 📊 Progresso Geral das Trilhas"
    end_marker = "## 🎓 TRILHA 1"
    
    new_section = f"{start_marker}\n\n{cards}\n\n{pie_chart}\n\n{bar_chart}\n\n{table_content}\n\n**Total Geral:** {total_info}\n\n"
    
    pattern = re.compile(f"{re.escape(start_marker)}.*?{re.escape(end_marker)}", re.DOTALL)
    updated_content = pattern.sub(new_section + end_marker, content)
    
    # Atualizar data de atualização
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    updated_content = re.sub(r"\*\*🔄 Última atualização:\*\*.*", f"**🔄 Última atualização:** {now} (Automático via Manus)", updated_content)
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(updated_content)

if __name__ == "__main__":
    try:
        c, p, s, a = load_data()
        metrics, total_aulas, total_concluidas = calculate_metrics(c, p, s, a)
        table = generate_markdown_table(metrics)
        
        percent_geral = (total_concluidas / total_aulas * 100) if total_aulas > 0 else 0
        total_info = f"{total_aulas} aulas • **Concluídas:** {total_concluidas} ({percent_geral:.1f}%) • **Faltam:** {total_aulas - total_concluidas}"
        
        cards = generate_status_cards(total_aulas, total_concluidas, percent_geral)
        pie, bar = generate_mermaid_charts(metrics, p, modulos=pd.read_csv("data/processed/DIM_MODULOS.csv", sep=';'))
        check_and_move_certificates(metrics)
        update_readme(table, total_info, pie, bar, cards)
        print("Dashboard atualizado com sucesso!")
    except Exception as e:
        print(f"Erro ao atualizar dashboard: {e}")
