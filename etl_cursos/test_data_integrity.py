import pandas as pd
import pytest
import os

# Configuração dos caminhos
BASE_PATH = "data/processed"

def load_table(filename):
    path = os.path.join(BASE_PATH, filename)
    if not os.path.exists(path):
        pytest.skip(f"Arquivo {filename} não encontrado.")
    return pd.read_csv(path, sep=';')

def test_dim_cursos_integrity():
    df = load_table("DIM_CURSOS.csv")
    # Verificar se id_curso é único
    assert df['id_curso'].is_unique, "id_curso deve ser único em DIM_CURSOS"
    # Verificar se não há nomes de cursos nulos
    assert df['nome_curso'].notnull().all(), "nome_curso não pode ter valores nulos"

def test_fato_progresso_relationships():
    fato = load_table("FATO_PROGRESSO.csv")
    cursos = load_table("DIM_CURSOS.csv")
    
    # Verificar se todos os id_curso na FATO existem na DIM_CURSOS
    invalid_cursos = fato[~fato['id_curso'].isin(cursos['id_curso'])]
    assert len(invalid_cursos) == 0, f"Existem id_curso na FATO que não existem na DIM_CURSOS: {invalid_cursos['id_curso'].unique()}"

def test_progresso_percentage_logic():
    fato = load_table("FATO_PROGRESSO.csv")
    # Status de conclusão (Aprovado=1, Concluído=4)
    concluidos_ids = [1, 4]
    
    # Agrupar por curso e calcular progresso
    total_aulas = fato.groupby('id_curso').size()
    concluidas = fato[fato['id_status'].isin(concluidos_ids)].groupby('id_curso').size()
    
    for cid in total_aulas.index:
        t = total_aulas[cid]
        c = concluidas.get(cid, 0)
        assert c <= t, f"Curso {cid} tem mais aulas concluídas ({c}) do que o total ({t})"

def test_dim_status_completeness():
    df = load_table("DIM_STATUS.csv")
    # Verificar se os status básicos existem
    required_status = ["Aprovado", "Concluído", "Em andamento"]
    for status in required_status:
        assert status in df['descricao_status'].values, f"Status '{status}' essencial não encontrado em DIM_STATUS"

if __name__ == "__main__":
    # Permite rodar os testes diretamente via python
    pytest.main([__file__])
