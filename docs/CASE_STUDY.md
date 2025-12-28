# 📖 Case Study: Engenharia de Dados para Transição de Carreira
## 🎯 1. O Problema
A transição de carreira para Ciência de Dados exige consistência e o domínio de múltiplas disciplinas (Técnica, Gestão e Idiomas). Para um profissional que atua no setor de serviços (restaurante), o maior desafio não é apenas o conteúdo, mas a **gestão da energia pós-trabalho** e o **monitoramento real do progresso** para evitar o burnout e a procrastinação.
## 🛠️ 2. A Solução Técnica
Foi desenvolvido um ecossistema de dados autônomo que transforma o estudo passivo em um pipeline de engenharia ativo.
### Arquitetura do Sistema:
1.  **Ingestão de Dados**: Interface via Telegram Bot para registro rápido de logs e nível de energia (1-10).
2.  **Orquestração (n8n)**: Fluxos automatizados que conectam o Telegram ao GitHub e utilizam IA para sugerir tarefas personalizadas baseadas na energia reportada.
3.  **Data Warehouse (Star Schema)**: Implementação de um modelo dimensional (Tabelas Fato e Dimensão) em Python para organizar o histórico de estudos, permitindo análises granulares de performance.
4.  **CI/CD (GitHub Actions)**: Pipeline automatizado que executa o ETL e atualiza o Dashboard do projeto no `README.md` a cada novo registro.
## 🚀 3. Tecnologias Utilizadas
*   **Linguagem**: Python (Pandas para ETL e Pytest para qualidade).
*   **Automação**: n8n (Self-hosted) e GitHub Actions.
*   **Inteligência Artificial**: Gemini IA API para mentoria de estudos.
*   **Banco de Dados**: Versionamento via GitHub (CSV/JSON).
*   **Metodologia**: Star Schema (Modelagem Dimensional).
## 📈 4. Resultados e Impacto
*   **Visibilidade Total**: O progresso das 3 trilhas é atualizado em tempo real, eliminando a necessidade de planilhas manuais.
*   **Otimização de Energia**: Redução da carga cognitiva na escolha do que estudar, delegando a decisão para a IA baseada no estado físico/mental do usuário.
*   **Portfólio Ativo**: O próprio sistema de estudos serve como prova técnica de competência em Engenharia de Dados e Automação para recrutadores.
---
> "Dados são a linguagem do futuro. Este projeto é a prova de que a engenharia pode ser aplicada para otimizar o recurso mais valioso de um estudante: o tempo."
