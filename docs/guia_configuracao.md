# 🛠️ Guia de Configuração das Automações
Este guia contém os passos necessários para ativar o ecossistema de automação da sua jornada.
## 1. GitHub Actions (Dashboard Automático)
O pipeline já está configurado! Para que ele funcione, você só precisa:
1. Ir em **Settings > Actions > General** no seu repositório.
2. Em **Workflow permissions**, selecione **"Read and write permissions"**.
3. Clique em **Save**.
Agora, sempre que você adicionar novos dados na pasta `data/raw`, o README será atualizado sozinho.
## 2. n8n + Telegram + IA (Custo Zero)
### Passo A: Telegram
1. Fale com o [@BotFather](https://t.me/botfather) e crie um novo bot.
2. Guarde o **API Token**.
### Passo B: IA (Groq - Grátis)
1. Crie uma conta em [console.groq.com](https://console.groq.com/).
2. Gere uma **API Key** (é gratuito e muito rápido).
### Passo C: Importar Fluxo no n8n
1. Abra seu n8n.
2. Clique em **Import from File** e selecione o arquivo `scripts/n8n_workflow_template.json`.
3. Configure as credenciais do Telegram e do Groq com os tokens que você pegou.
## 3. Google Sheets (Opcional)
Se quiser um dashboard no Looker Studio:
1. No n8n, adicione um nó de **Google Sheets**.
2. Conecte sua conta Google e selecione uma planilha para salvar os logs.
---
