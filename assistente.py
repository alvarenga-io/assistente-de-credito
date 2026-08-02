import os 
from pathlib import Path
from dotenv import load_dotenv # Carrega as váriaveis do arquivo .env para a memória da aplicação
from google import genai # SDk oficial do Gemini para enviar e receber mensagens
from google.genai import types


# -- Inicialização das variáveis de ambiente e configuração da Biblioteca do Gemini
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("API Key não encontrada. Verifique o arquivo .env!")

client = genai.Client(api_key=api_key)

# -- Carrega o arquivo regras-credito.md

def carregar_base_conhecimento(nome_arquivo="regras-credito.md"):

    diretorio_script = Path(__file__).parent.resolve()
    caminho_arquivo = diretorio_script.parent / "conhecimento" / nome_arquivo
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            conteudo = arquivo.read().strip()
        return conteudo
    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado")
        return None

# -- Instruções de sistema com as regras comportamento.
def construir_prompt_mestre(base_conhecimento: str) -> str:
    return f"""
Você é o **Assistente Virtual de Linhas de Crédito da GoiásFomento**.
Seu objetivo é orientar empreendedores de forma clara, didática e acolhedora sobre as opções de crédito disponíveis.

---
### REGRAS OBRIGATÓRIAS E DIRETRIZES DE COMPORTAMENTO:

1. **FONTE ÚNICA DA VERDADE**:
   - Responda **APENAS** com base nas informações contidas na BASE DE CONHECIMENTO abaixo.
   - NUNCA utilize conhecimento externo prévio nem invente taxas, prazos, exigências ou limites.

2. **GENTILEZA E ANTI-ALUCINAÇÃO**:
   - A base de conhecimento contempla apenas as linhas FCO. Se a dúvida do usuário NÃO estiver coberta pela base de conhecimento, diga de forma educada e transparente: 
     "Não possuo essa informação na minha base de consulta no momento. Você pode consultar todas as linhas disponíveis [!aqui](https://www.goiasfomento.com/linhas-de-credito/). Para detalhes específicos sobre este ponto, recomendo entrar em contato direto com a equipe de atendimento da GoiásFomento."
   - Não tente adivinhar respostas para dados ausentes.

3. **TOM E LINGUAGEM**:
   - Adote um tom acolhedor, profissional e extremamente acessível.
   - Mantenha em mente que muitos empreendedores não dominam termos técnicos financeiros. Explique conceitos de forma simples se necessário.

4. **ESTRUTURA DA RESPOSTA**:
   - Seja direto e objetivo.
   - Quando listar requisitos ou documentos, prefira tópicos (bullet points) para facilitar a leitura.
---

### BASE DE CONHECIMENTO OFICIAL:
{base_conhecimento}
"""

# -- Função  para ser importada pelo app.py do Streamlit.
# carrega a base, monta o prompt e devolve o objeto de chat pronto.
def inicializar_chat_streamlit():
    
    base = carregar_base_conhecimento()
    if not base:
        raise ValueError("Erro: Não foi possível carregar a base de conhecimentos.")

    system_instruction = construir_prompt_mestre(base)

    chat = client.chats.create(
        model="gemini-3.1-flash-lite",
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.2
        )
    )
    return chat
