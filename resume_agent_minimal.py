# resume_agent_app.py

import re
import os
# from dotenv import load_dotenv
from pathlib import Path
import streamlit as st
# import openai
import streamlit as st

import streamlit as st

st.set_page_config(
    page_title="Resume Agent",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={}
)

hide_streamlit_style = """
<style>
  #MainMenu, header, footer {visibility: hidden;}
  .css-1d391kg, .css-18e3th9 {padding: 0;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import FAISS # stubbed out for embed UI testing
# from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.memory import ConversationBufferMemory

# Load environment variables
# load_dotenv()
# openai.api_key = st.secrets["OPENAI_API_KEY"]
# openai_key = st.secrets["OPENAI_API_KEY"]


# 📎 Manual case study URL map
case_study_links = {
    "Demonstrating Strategic P&L Ownership and Customer.md": "https://www.canva.com/design/DAGncSFIvHg/CK8h5GKzBCrt2ig2gS0bMw/view?utm_content=DAGncSFIvHg&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=h7f7803d827",
    "Driving Adoption & Retention.md": "https://www.canva.com/design/DAGnjKSGHNk/4T3MK6YELPATzxtgV_Vd-Q/view?utm_content=DAGnjKSGHNk&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=hdaf63b95d2",
    "Leading Culture-Driven Transformation.md": "https://www.canva.com/design/DAGoGUoywCQ/hG7e74REdSTCz1AHBTWWnQ/view?utm_content=DAGoGUoywCQ&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=h8222948442",
    "Margin Improvement & Revenue Integrity.md": "https://www.canva.com/design/DAGndX1mdjw/G5xk6W4NRTNT-SFe76aVRQ/view?utm_content=DAGndX1mdjw&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=h779a5f4e4a",
    "Scaling Customer Experience through VOC.md": "https://www.canva.com/design/DAGndukdNyE/kcFNsRRrvVbuzJkrEs5sdQ/view?utm_content=DAGndukdNyE&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=h39a6f25d57",
    "automation.md": "https://www.canva.com/design/DAGndukdNyE/kcFNsRRrvVbuzJkrEs5sdQ/view?utm_content=DAGndukdNyE&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=h39a6f25d57"
}

# 📄 Load documents from /docs
@st.cache_data
def load_documents(folder_path="docs"):
    import re  # Make sure this is imported at the top
    docs = []
    folder = Path(folder_path)
    
    for file_path in folder.glob("*"):
        ext = file_path.suffix.lower()
        if ext == ".pdf":
            loader = PyPDFLoader(str(file_path))
        elif ext == ".docx":
            loader = Docx2txtLoader(str(file_path))
        elif ext in [".txt", ".md"]:
            loader = TextLoader(str(file_path))
        else:
            print(f"Skipping unsupported file: {file_path.name}")
            continue

        raw_docs = loader.load()
        file_name = file_path.name
        source_url = case_study_links.get(file_name, "")

        # Clean title: remove suffix starting with first digit, keep readable name
        clean_title = re.sub(r"\s?\d.*", "", file_name).replace("_", " ").replace(file_path.suffix, "").strip()

        # Manual override for automation case
        if file_name == "automation.md":
            clean_title = "Driving Automation and Efficiency"

        # Attach metadata
        for doc in raw_docs:
            doc.metadata["source_url"] = source_url
            doc.metadata["title"] = clean_title

        docs.extend(raw_docs)

    return docs


# 🧠 Set up persistent memory
if "memory" not in st.session_state:
    from langchain.memory import ConversationBufferMemory
    st.session_state.memory = ConversationBufferMemory(
        memory_key="chat_history", 
        return_messages=True,
        output_key="answer",
    )

#Initialize Chain
#Initialize Chain
@st.cache_resource
def initialize_chain():
    # --- FAISS & RetrievalQA chain is stubbed out for embed UI testing ---
    def dummy_qa_chain(inputs: dict):
        question = inputs.get("question", "")
        return {
            "answer": f"(UI test) You asked: {question}",
            "source_documents": []
        }

    return dummy_qa_chain

# 🖥️ Streamlit UI
st.set_page_config(page_title="Resume Agent (UI Test)", layout="wide")
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# 2) Constrain & center the input boxst.markdown(
st.markdown(
    """
    <style>
      /* make the Ask-a-question input max 400px wide and center it */
      .stTextInput > div > div > input {
        max-width: 400px !important;
        margin-left: auto !important;
        margin-right: auto !important;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

#initialize dummy chain
qa_chain = initialize_chain()


# render Input box and echo logic
query = st.text_input("Ask a question:")

if query:
    result = qa_chain({"question": query})
    st.write(result["answer"])
