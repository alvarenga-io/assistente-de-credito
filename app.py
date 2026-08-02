import time
import random
import streamlit as st
import google.genai as genai
from assistente import inicializar_chat_streamlit
# ---- Configurações do Site
st.set_page_config(
    page_title='Assistente de Atendimento',
    page_icon='chat'
)

# -- Cabeçalho
st.title('Assistente de Linhas de Crédito')
st.markdown("Bem-vindo! Descreva sua necessidade e eu ajudarei a encontrar a linha de crédito da GoiásFomento ideal para o seu negócio.")


if "chat_session" not in st.session_state:
    try:
        st.session_state.chat_session = inicializar_chat_streamlit()
    except Exception as e:
        st.error(f"Erro ao iniciar os assistente: {e}")
        st.stop()
# -- Inicialização do histórico
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant", "content": "Você pode tentar me perguntar:\n\n* *Qual linha de crédito serve para capital de giro?*\n* *Qual é o valor máximo que posso financiar pelo FCO Verde?*\n* *Qual o prazo e a carência para um financiamento de investimento destinado a um MEI?*"}
    ]


# -- Renderiza o histórico de mensagens existente
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -- Captura a entrada do usuário
if prompt := st.chat_input("Digite sua dúvida sobre crédito aqui..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Buscando informações na base da GoiásFomento..."):
            try:
                resposta = st.session_state.chat_session.send_message(prompt)

                texto_resposta = resposta.text
                st.markdown(texto_resposta)
                st.session_state.messages.append({"role": "assistant", "content":texto_resposta})
            except Exception as e:
                st.error(f"Erro ao gerar resposta: {e}")