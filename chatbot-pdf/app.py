import os
import re
import streamlit as st
from pypdf import PdfReader
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title="PDF AI Assistant", page_icon="📄")
st.title("PDF AI Assistant")
st.caption("Faça perguntas sobre um PDF e encontre as páginas relevantes.")

file = st.file_uploader("Envie um PDF", type=["pdf"])
question = st.text_input("Sua pergunta", placeholder="Ex.: Quais são os principais pontos do documento?")
if file:
    reader = PdfReader(file)
    pages = [{"number": i + 1, "text": (p.extract_text() or "").strip()} for i, p in enumerate(reader.pages)]
    pages = [p for p in pages if p["text"]]
    st.write(f"Páginas com texto extraído: {len(pages)}")
    if question:
        terms = set(re.findall(r"\w+", question.lower()))
        ranked = []
        for page in pages:
            text_terms = set(re.findall(r"\w+", page["text"].lower()))
            score = len(terms & text_terms)
            if score:
                ranked.append((score, page))
        ranked.sort(key=lambda x: x[0], reverse=True)
        selected = [p for _, p in ranked[:4]]
        if not selected:
            st.warning("Não encontrei correspondências por palavras-chave. Tente reformular a pergunta.")
        else:
            context = "\n\n".join(f"[Página {p['number']}]\n{p['text'][:5000]}" for p in selected)
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                try:
                    from openai import OpenAI
                    client = OpenAI(api_key=api_key)
                    response = client.chat.completions.create(
                        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                        messages=[
                            {"role": "system", "content": "Responda em português usando apenas o contexto fornecido. Se a informação não estiver no contexto, diga isso. Cite os números das páginas."},
                            {"role": "user", "content": f"Pergunta: {question}\n\nContexto:\n{context}"}
                        ],
                        temperature=0.2,
                    )
                    st.subheader("Resposta")
                    st.write(response.choices[0].message.content)
                    st.caption("Resposta gerada por modelo de IA; confira no documento original.")
                except Exception as exc:
                    st.error(f"Falha ao consultar a API: {exc}")
                    st.info("Abaixo estão os trechos encontrados para consulta manual.")
                    for p in selected:
                        with st.expander(f"Página {p['number']}"):
                            st.write(p["text"][:5000])
            else:
                st.info("Configure OPENAI_API_KEY para ativar respostas generativas. Resultado local por palavras-chave:")
                for p in selected:
                    with st.expander(f"Página {p['number']} — relevância {next(s for s, pg in ranked if pg is p)}"):
                        st.write(p["text"][:5000])
