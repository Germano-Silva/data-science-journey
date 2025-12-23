# **📊 FLUXO COMPLETO EM MERMAID**
```mermaid
graph TD
    A["🌅 Início do Dia"] --> B{"Dispositivo?"}
    
    B -->|📱 Telegram| C["🤖 DataScience Companion Bot"]
    B -->|💻 Navegador| D["🌐 Interface Web n8n"]
    
    C --> E["/start"]
    C --> F["/energy 4"]
    C --> G["/log 45 SQL Aula 1"]
    C --> H["/progress"]
    C --> I["/help"]
    
    E --> J["Envia: Boas-vindas + instruções"]
    F --> K["Registra energia no sistema"]
    G --> L["Cria log no GitHub + atualiza progresso"]
    H --> M["Consulta progresso das 3 trilhas"]
    I --> N["Lista comandos disponíveis"]
    
    K --> O{"Energia ≤ 3?"}
    O -->|Sim| P["Sugere tarefa LEVE: Revisão / Inglês 15min"]
    O -->|Não| Q{"Energia entre 4 e 6?"}
    Q -->|Sim| R["Sugere tarefa MÉDIA: Exercício prático 25min"]
    Q -->|Não| S["Sugere tarefa PESADA: Mini-projeto 40min"]
    
    P --> T["📅 Atualiza calendário com tarefa"]
    R --> T
    S --> T
    
    T --> U["📝 Cria Issue no GitHub"]
    U --> V["📊 Atualiza GitHub Projects Kanban"]
    V --> W["🏆 Calcula pontos: energia × 5"]
    W --> X["📈 Atualiza dashboard README.md"]
    
    X --> Y{"Usuário concluiu?"}
    Y -->|✅ Sim| Z["Fecha Issue + adiciona ✅ no Projects"]
    Y -->|⏰ Timeout| AA["Envia lembrete após 2h"]
    
    Z --> BB["🎯 Sugere próximo passo"]
    AA --> BB
    
    BB --> CC["📅 Agenda próxima sessão baseada na energia"]
    
    CC --> DD{"É domingo?"}
    DD -->|Sim| EE["📋 Gera relatório semanal automático"]
    DD -->|Não| FF["Aguarda próximo check-in"]
    
    EE --> GG["📊 Atualiza todas as métricas"]
    GG --> HH["🎯 Sugere ajustes para semana seguinte"]
    HH --> FF
    
    FF --> II["⏰ Próximo check-in 17:00"]
    
    subgraph DS["🎓 Trilha Data Science Técnico"]
        direction TB
        DS1["SQL: 0/62 aulas"]
        DS2["Python: 0/79"]
        DS3["Estatística: 0/117"]
        DS4["Machine Learning: 0/123"]
    end
    
    subgraph GE["💼 Trilha Gestão Empresarial"]
        direction TB
        GE1["Concluído: 49/96"]
        GE2["Análise Financeira: 0/4"]
        GE3["Go-to-Market: 0/11"]
    end
    
    subgraph EN["🌐 Trilha Inglês Técnico"]
        direction TB
        EN1["Em andamento: 7/225"]
        EN2["Meta diária: 30min"]
    end
    
    L --> DS1
    L --> GE1
    L --> EN1
    
    M --> DS1
    M --> GE1
    M --> EN1
    
    style A fill:#f9f,stroke:#333,stroke-width:2px
    style C fill:#2266aa,stroke:#ffffff,stroke-width:2px,color:#ffffff
    style T fill:#22aa22,stroke:#333,stroke-width:2px,color:#ffffff
    style U fill:#aa22aa,stroke:#333,stroke-width:2px,color:#ffffff
    style EE fill:#ff9922,stroke:#333,stroke-width:2px

```

---

# **🔗 FLUXO DETALHADO POR COMPONENTE**

```mermaid
graph TB
    subgraph "📱 Interface do Usuário"
        A1[Telegram Bot]
        A2[Webhook n8n]
        A3[Dashboard GitHub README]
    end
    
    subgraph "🧠 Sistema de Decisão"
        B1[Análise de Energia 1-10]
        B2[Sugestor Inteligente]
        B3[Priorizador de Trilhas]
    end
    
    subgraph "📊 Sistema de Tracking"
        C1[GitHub Issues - Log diário]
        C2[GitHub Projects - Kanban]
        C3[Arquivos JSON - Progresso]
        C4[GitHub Actions - Automações]
    end
    
    subgraph "🎯 Sistema de Gamificação"
        D1[Calculadora de Pontos]
        D2[Sistema de Conquistas]
        D3[Leaderboard pessoal]
        D4[Recompensas semanais]
    end
    
    subgraph "🔄 Sistema de Feedback"
        E1[Relatórios semanais]
        E2[Ajustes automáticos]
        E3[Alertas de consistência]
        E4[Sugestões de melhoria]
    end
    
    A1 --> B1
    A2 --> B1
    B1 --> B2
    B2 --> B3
    
    B3 --> C1
    B3 --> C2
    C1 --> D1
    C2 --> D1
    
    D1 --> D2
    D2 --> D3
    D3 --> D4
    
    C4 --> E1
    D4 --> E2
    E1 --> E3
    E2 --> E4
    
    E3 --> B2
    E4 --> B3
    
    style A1 fill:#26a,stroke:#fff,color:#fff
    style B2 fill:#2a2,stroke:#333,color:#fff
    style C2 fill:#a2a,stroke:#333,color:#fff
    style D1 fill:#f92,stroke:#333
    style E1 fill:#9af,stroke:#333
```

---

# **⏰ FLUXO TEMPORAL DIÁRIO**

```mermaid
gantt
    title Fluxo Diário - Data Science Companion
    dateFormat HH:mm
    axisFormat %H:%M
    
    section Manhã
    Preparação sistema :07:00, 10m
    Verificação automática :07:10, 5m
    
    section Tarde
    Check-in automático :17:00, 15m
    Sugestão IA :17:05, 5m
    Execução tarefa :17:15, 45m
    
    section Noite
    Log conclusão :18:00, 10m
    Atualização GitHub :18:10, 10m
    Planejamento amanhã :18:20, 10m
    
    section Background
    Monitoramento energia :07:00, 12h
    Backup dados :22:00, 30m
```

---

# **📁 ARQUITETURA DE DADOS**

```mermaid
graph LR
    subgraph "🎮 Frontend"
        F1[Telegram Bot]
        F2[n8n Web Interface]
        F3[GitHub README Dashboard]
    end
    
    subgraph "🔄 Processamento"
        P1[n8n Workflows]
        P2[GitHub Actions]
        P3[Scripts Python]
    end
    
    subgraph "💾 Armazenamento"
        S1[GitHub Issues]
        S2[GitHub Projects]
        S3[Arquivos JSON]
        S4[GitHub Wiki]
    end
    
    subgraph "🔌 APIs"
        A1[Telegram API]
        A2[GitHub API]
        A3[Z.AI API]
        A4[Ollama API]
    end
    
    F1 --> A1
    F2 --> P1
    F3 --> S1
    
    P1 --> A2
    P1 --> A3
    P1 --> A4
    
    P2 --> S2
    P3 --> S3
    
    A2 --> S1
    A2 --> S2
    
    S3 --> F3
    S4 --> F3
    
    style F1 fill:#26a,stroke:#fff,color:#fff
    style P1 fill:#2a2,stroke:#333,color:#fff
    style S1 fill:#a2a,stroke:#333,color:#fff
    style A2 fill:#f92,stroke:#333
```

---

# **🤖 FLUXO DA CONVERSA COM O BOT**

```mermaid
sequenceDiagram
    participant U as Usuário (Germano)
    participant B as Telegram Bot
    participant N as n8n
    participant G as GitHub
    participant AI as Z.AI/Ollama
    
    Note over U,B: 🕔 17:00 - Check-in automático
    B->>U: "Olá! Energia hoje? (1-10)"
    
    Note over U,B: Usuário responde
    U->>B: "4"
    
    B->>N: Envia energia=4
    N->>AI: "Sugira tarefa para energia 4/10"
    AI->>N: "[SQL] Aula 1 - 25min"
    
    N->>G: Cria Issue #45 com tarefa
    G->>N: Confirma criação
    
    N->>B: Envia sugestão formatada
    B->>U: "🎯 Tarefa: SQL Aula 1 (25min)"
    
    Note over U,B: ⏰ 45 minutos depois
    U->>B: "✅ Concluído!"
    
    B->>N: Registra conclusão
    N->>G: Fecha Issue #45
    N->>G: Atualiza Projects (move para ✅)
    N->>G: Atualiza progresso.json
    
    G->>N: Confirma atualizações
    N->>B: Calcula pontos (4×5=20)
    B->>U: "✅ 20 pontos! Total: 120"
    
    Note over B,U: 🎯 Sugere próximo
    B->>U: "Amanhã: SQL Aula 2 ou revisão?"
```

---

# **📊 PROCESSO SCRUM - 3 FASES**

## **🎯 SPRINT 1: BOT TELEGRAM (MVP)**

### **Diagrama 1: Fluxo do Bot**
```mermaid
graph TD
    A["Usuário abre Telegram"] --> B{"Comando?"}
    
    B --> C["/start"]
    B --> D["/energy<br>1-10"]
    B --> E["/log<br>minutos descrição"]
    B --> F["/progress"]
    B --> G["/help"]
    
    C --> H["Envia: Boas-vindas<br>comandos disponíveis"]
    D --> I["Registra energia<br>no sistema"]
    E --> J["Cria log GitHub<br>+ pontos"]
    F --> K["Consulta progresso<br>3 trilhas"]
    G --> L["Lista comandos<br>e exemplos"]
    
    I --> M{"Energia ≤ 3?"}
    M -->|Sim| N["Sugere tarefa LEVE"]
    M -->|Não| O{"Energia entre 4 e 6?"}
    O -->|Sim| P["Sugere tarefa MÉDIA"]
    O -->|Não| Q["Sugere tarefa PESADA"]
    
    N --> R["📱 Envia sugestão"]
    P --> R
    Q --> R
    
    style A fill:#f9f,stroke:#333,stroke-width:2px
    style H fill:#2a2,stroke:#333,color:#fff
    style R fill:#26a,stroke:#fff,color:#fff,stroke-width:2px

```

### **📋 Tarefas Sprint 1 (Bot):**
1. ✅ Criar bot no Telegram (@BotFather)
2. ⬜ Configurar credencial no n8n
3. ⬜ Implementar comando `/start`
4. ⬜ Implementar comando `/energy`
5. ⬜ Implementar comando `/help`
6. ⬜ Testar fluxo básico

### **📅 Duração estimada:** 2 dias

---

## **🎯 SPRINT 2: AUTOMAÇÃO N8N**

### **Diagrama 2: Fluxo de Automação**
```mermaid
graph LR
    A[⏰ Schedule Trigger 17:00] --> B[🤖 Telegram: pergunta energia]
    B --> C[🔄 Webhook aguarda resposta]
    C --> D[🧠 Processa energia 1-10]
    D --> E[📊 Sugere tarefa baseada<br/>na energia]
    E --> F[📱 Telegram: envia tarefa]
    F --> G[⏳ Aguarda conclusão]
    G --> H[✅ Registra no GitHub]
    
    subgraph "🎯 Decisão por Energia"
        D1[1-3: Revisão/Inglês 15min]
        D2[4-6: Exercício 25min]
        D3[7-10: Projeto 40min]
    end
    
    D -->|≤3| D1
    D -->|4-6| D2
    D -->|≥7| D3
    
    D1 --> E
    D2 --> E
    D3 --> E
    
    style A fill:#f92,stroke:#333
    style B fill:#26a,stroke:#fff,color:#fff
    style H fill:#2a2,stroke:#333,color:#fff
```

### **📋 Tarefas Sprint 2 (Automação):**
1. ⬜ Configurar Schedule Trigger (17:00)
2. ⬜ Criar webhook para respostas
3. ⬜ Implementar lógica de energia → tarefa
4. ⬜ Criar template de mensagens
5. ⬜ Testar fluxo automático
6. ⬜ Adicionar fallback manual

### **📅 Duração estimada:** 3 dias

---

## **🎯 SPRINT 3: TRILHAS E PROGRESSO**

### **Diagrama 3: Fluxo das Trilhas**
```mermaid
graph TB
    A[📊 Progresso das 3 Trilhas] --> B
    
    subgraph "🎓 Data Science Técnico"
        B[SQL: 0/62]
        C[Python: 0/79]
        D[Estatística: 0/117]
    end
    
    subgraph "💼 Gestão Empresarial"
        E[Concluído: 49/96]
        F[Em andamento: 1/9]
    end
    
    subgraph "🌐 Inglês Técnico"
        G[7/225 aulas]
        H[30min/dia]
    end
    
    I[📅 Calendário semanal] --> J{Energia hoje?}
    J -->|Baixa| K[Foca Inglês/Revisão]
    J -->|Média| L[Foca SQL/Python]
    J -->|Alta| M[Foca Projetos/Gestão]
    
    K --> N[Atualiza progresso<br/>na trilha certa]
    L --> N
    M --> N
    
    N --> O[📈 Atualiza dashboard<br/>GitHub README]
    
    style A fill:#f9f,stroke:#333,stroke-width:2px
    style B fill:#9af,stroke:#333
    style E fill:#2a2,stroke:#333,color:#fff
    style G fill:#f92,stroke:#333
    style O fill:#a2a,stroke:#333,color:#fff
```

### **📋 Tarefas Sprint 3 (Trilhas):**
1. ⬜ Criar arquivos JSON para cada trilha
2. ⬜ Implementar sistema de tracking
3. ⬜ Criar dashboard no README
4. ⬜ Integrar com GitHub Projects
5. ⬜ Gerar relatórios semanais
6. ⬜ Sistema de pontos/gamificação

### **📅 Duração estimada:** 4 dias

---

## **📋 BACKLOG COMPLETO:**

### **Prioridade P1 (Essencial):**
1. Bot responde a comandos básicos
2. Check-in automático 17:00
3. Sugestões baseadas em energia
4. Log no GitHub Issues

### **Prioridade P2 (Importante):**
5. Sistema de pontos
6. Dashboard no README
7. GitHub Projects integration
8. Relatórios semanais

### **Prioridade P3 (Desejável):**
9. IA para sugestões personalizadas
10. Calendário visual
11. Gamificação avançada
12. Multiplataforma (WhatsApp/Web)

---
