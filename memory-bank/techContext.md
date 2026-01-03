# Tech Context: Data Science Journey

## Stack Tecnológico

### Linguagens
- **Python 3.8+**: Linguagem principal para ETL, análise e automação
- **Markdown**: Documentação e README dinâmico
- **Mermaid**: Diagramas e visualizações embutidas em Markdown

### Bibliotecas Python

#### Core Dependencies
```
pandas>=1.3.0        # Data manipulation e análise
pathlib              # Path handling cross-platform (stdlib)
logging              # Sistema de logging (stdlib)
typing               # Type hints (stdlib)
```

#### Ambiente de Desenvolvimento
```
python>=3.8
pip                  # Package manager
venv                 # Virtual environments (opcional)
```

### Ferramentas de Desenvolvimento

#### Controle de Versão
- **Git**: Versionamento de código e dados
- **GitHub**: Hospedagem, colaboração e visualização de progresso

#### IDE/Editores
- **Visual Studio Code**: IDE principal
  - Extensões úteis:
    - Python
    - Markdown Preview Enhanced
    - GitLens
    - Mermaid Preview

#### Sistema Operacional
- **Windows 11**: Ambiente primário de desenvolvimento
- **CMD/PowerShell**: Shell padrão para execução de scripts

## Estrutura de Dados

### Formato de Arquivos

#### Input (data/raw/)
- **CSV**: Dados brutos de cursos
  - Encoding: UTF-8
  - Delimitador: `,` (vírgula)
  - Formatos variados por plataforma:
    - DNC: Estrutura padrão de módulos
    - Kultive: Estrutura com aulas detalhadas
    - Prepara Portugal: Estrutura simplificada

- **Markdown**: Informações complementares
  - Duração de aulas
  - Descrições detalhadas

#### Output (data/processed/)
- **CSV**: Tabelas dimensionais
  - Encoding: UTF-8
  - Delimitador: `;` (ponto e vírgula)
  - Header: Sempre presente
  - Quoting: Minimal (apenas quando necessário)

### Schema de Dados

#### DIM_CURSOS
```
id_curso (int)
nome_curso (str)
categoria (str)
total_aulas (int)
requisitos (str, nullable)
```

#### DIM_MODULOS
```
id_modulo (int)
id_curso (int, FK)
nome_modulo (str)
numero_modulo (int)
duracao_estimada (str, nullable)
```

#### DIM_AULAS
```
id_aula (int)
id_modulo (int, FK)
nome_aula (str)
duracao_aula (str, nullable)
tipo_conteudo (str, nullable)
```

#### DIM_STATUS
```
id_status (int)
descricao_status (str)
categoria_status (str)
```

#### DIM_TEMPO
```
id_tempo (int)
data_completa (date)
ano (int)
trimestre (int)
mes (int)
semana (int)
```

#### FATO_PROGRESSO
```
id_progresso (int)
id_curso (int, FK)
id_modulo (int, FK)
id_aula (int, FK)
id_status (int, FK)
id_tempo (int, FK)
data_inicio (date, nullable)
data_fim (date, nullable)
```

## Configuração do Ambiente

### Setup Inicial

```bash
# 1. Clonar repositório
git clone https://github.com/Germano-Silva/data-science-journey.git
cd data-science-journey

# 2. Criar ambiente virtual (opcional mas recomendado)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Instalar dependências
pip install pandas

# 4. Verificar instalação
python --version
python -c "import pandas; print(pandas.__version__)"
```

### Estrutura de Diretórios Esperada

```
data-science-journey/
├── .git/                      # Git repository
├── .gitignore                 # Git ignore rules
├── README.md                  # Documentation principal
├── LICENSE                    # MIT License
│
├── data/
│   ├── raw/                   # Dados originais (NÃO MODIFICAR)
│   │   ├── Cursos - DNC.csv
│   │   ├── Cursos - Kultive.csv
│   │   └── Cursos - Prepara Portugal.csv
│   ├── processed/             # Dados processados (GERADOS)
│   │   ├── DIM_CURSOS.csv
│   │   ├── DIM_MODULOS.csv
│   │   ├── DIM_AULAS.csv
│   │   ├── DIM_STATUS.csv
│   │   ├── DIM_TEMPO.csv
│   │   ├── FATO_PROGRESSO.csv
│   │   └── etl.log
│   └── external/              # Dados externos
│
├── etl_cursos/                # Pipeline ETL
│   ├── config.py
│   ├── extractors.py
│   ├── transformers.py
│   ├── loaders.py
│   ├── utils.py
│   ├── main.py
│   ├── run_etl.py
│   ├── test_etl_basic.py
│   ├── test_etl_structure.py
│   ├── test_data_integrity.py
│   └── README.md
│
├── scripts/                   # Automações
│   ├── update_dashboard.py
│   ├── ai_mentor.py
│   ├── automation/
│   └── data-processing/
│
├── notes/                     # Anotações de estudo
│   ├── cheatsheets/
│   ├── concepts/
│   └── daily-logs/
│
├── projects/                  # Projetos práticos
├── docs/                      # Documentação adicional
├── certificates/              # Certificados de conclusão
│   ├── completed/
│   └── in-progress/
│
└── memory-bank/               # Memory Bank (contexto)
    ├── projectbrief.md
    ├── productContext.md
    ├── systemPatterns.md
    ├── techContext.md
    ├── activeContext.md
    └── progress.md
```

## Comandos Principais

### Pipeline ETL

```bash
# Executar ETL completo
python etl_cursos/main.py

# Ou usar o runner
python etl_cursos/run_etl.py

# Testar estrutura (sem pandas)
python etl_cursos/test_etl_basic.py

# Testar com pandas
python etl_cursos/test_etl_structure.py

# Testar integridade de dados
python etl_cursos/test_data_integrity.py
```

### Atualizar Dashboard

```bash
# Regenerar README com métricas atualizadas
python scripts/update_dashboard.py
```

### Git Workflow

```bash
# 1. Verificar status
git status

# 2. Adicionar mudanças
git add data/processed/*.csv
git add README.md

# 3. Commit com mensagem descritiva
git commit -m "Update: Progresso 85.4% - 274/321 aulas"

# 4. Push para GitHub
git push origin main

# 5. Ver histórico
git log --oneline -10
```

## Dependências Externas

### Plataformas de Cursos
- **DNC (Digital Nation Courses)**: Plataforma principal para cursos técnicos
- **Kultive**: Cursos de gestão e negócios
- **Prepara Portugal**: Cursos complementares

### Serviços Cloud
- **GitHub**: 
  - Repositório de código
  - GitHub Pages (futuro: dashboard interativo)
  - GitHub Actions (futuro: CI/CD)

### Badges e Visualizações
- **Shields.io**: Geração de badges dinâmicos
- **Mermaid.js**: Renderização de diagramas no GitHub

## Constraints Técnicas

### Limitações
1. **Processamento Local**: Toda computação é local, sem cloud
2. **Armazenamento em CSV**: Sem database, limite de ~1M linhas
3. **Manual Updates**: Dados brutos atualizados manualmente
4. **No CI/CD**: Deploy e testes manuais

### Performance
- **ETL Runtime**: < 5 segundos para dataset atual
- **File Size**: CSVs < 1MB cada
- **Memory Usage**: < 100MB durante ETL

### Compatibilidade
- **OS**: Windows 11 (primário), compatível com Linux/Mac
- **Python**: 3.8, 3.9, 3.10, 3.11, 3.12
- **Pandas**: 1.3+

## Segurança e Privacidade

### Dados Públicos
- Todos os dados são pessoais e públicos
- Nenhuma informação sensível ou confidencial
- Progresso de aprendizado é transparente e compartilhável

### Credenciais
- Nenhuma credencial hardcoded
- Git push via SSH ou HTTPS com token
- Sem APIs keys necessárias

## Troubleshooting

### Problemas Comuns

#### 1. ImportError: No module named 'pandas'
```bash
# Solução
pip install pandas
```

#### 2. FileNotFoundError: data/raw/...
```bash
# Solução: Verificar que arquivos CSV estão no diretório correto
ls data/raw/
```

#### 3. UnicodeDecodeError
```bash
# Verificar encoding do arquivo
# Todos devem ser UTF-8
# Converter se necessário no editor
```

#### 4. CSV delimiter issues
```bash
# Verificar delimitador esperado
# Input: , (vírgula)
# Output: ; (ponto e vírgula)
```

### Debug Mode

```python
# Em config.py, adicionar:
DEBUG = True

# Em utils.py:
if DEBUG:
    logger.setLevel(logging.DEBUG)
```

## Roadmap Técnico

### Próximas Tecnologias a Adicionar

#### Curto Prazo (Q1 2026)
- [ ] **Jupyter Notebooks**: Análises exploratórias
- [ ] **Matplotlib/Seaborn**: Visualizações estáticas
- [ ] **pytest**: Framework de testes robusto

#### Médio Prazo (Q2-Q3 2026)
- [ ] **SQLite**: Database local para analytics
- [ ] **Plotly/Dash**: Dashboard interativo
- [ ] **GitHub Actions**: Automação de ETL

#### Longo Prazo (Q4 2026+)
- [ ] **PostgreSQL**: Database para produção
- [ ] **Docker**: Containerização
- [ ] **FastAPI**: API para consultas
- [ ] **Streamlit**: Web app para visualização

## Recursos de Aprendizado

### Documentação Oficial
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Python Pathlib](https://docs.python.org/3/library/pathlib.html)
- [Mermaid Documentation](https://mermaid.js.org/)

### Tutoriais Relevantes
- Data Engineering with Python
- ETL Best Practices
- Star Schema Design
- Git Workflow for Data Projects

## Notas de Versão

### v1.0 (Janeiro 2026)
- Pipeline ETL funcional
- Star Schema implementado
- README auto-atualizado
- Sistema de logging

### Decisões de Versioning
- **Git tags**: Para marcos importantes
- **Semantic versioning**: major.minor.patch
- **Changelog**: Mantido em commits descritivos
