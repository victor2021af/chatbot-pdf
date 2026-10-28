# PDF AI Assistant

Faça perguntas sobre um PDF e receba respostas com referência às páginas encontradas. MVP local com Streamlit, PyPDF e API OpenAI opcional.

## Funcionalidades
- Upload de PDF
- Extração de texto por página
- Busca local por palavras-chave, sem API
- Resposta com contexto via API OpenAI quando `OPENAI_API_KEY` estiver configurada
- Indicação das páginas usadas como contexto

## Executar
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
# opcional: copie .env.example para .env e configure OPENAI_API_KEY
streamlit run app.py
```

Sem chave de API, o app encontra páginas relevantes e mostra o texto correspondente. Isso não é uma resposta generativa de IA.

## Segurança
Não envie documentos confidenciais para APIs externas. A chave deve ficar em variável de ambiente, nunca no GitHub.
