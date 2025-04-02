import os
from langchain_community.document_loaders import PDFPlumberLoader, TextLoader, UnstructuredHTMLLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
import ollama
from api.utils import params_check

import datetime
import shutil

try:
    load_dotenv("./.env")
except:
    pass

if not os.getenv("CHROMA_PATH"):
    os.environ["CHROMA_PATH"] = "./chroma"

if not os.path.exists(os.getenv("CHROMA_PATH")):
    os.mkdir(os.getenv("CHROMA_PATH"))

def getModels():

    models = ollama.list().get("models", [])
    return models



def loadFile(file_path):
    

    ext = os.path.splitext(file_path)[-1].lower()

    if ext == ".pdf":
        loader = PDFPlumberLoader(file_path)
    elif ext == ".txt":
        loader = TextLoader(file_path, encoding="utf-8")
    elif ext == ".html":
        loader = UnstructuredHTMLLoader(file_path)
    else:
        print("Unsupported file type: {ext}")
        return False
    
    return loader.load()

def getVector(modelID):

    chroma_db_path = os.getenv("CHROMA_PATH") + "/" + modelID
    data = eval(open(chroma_db_path + "\info.info", "r", encoding="UTF-8").read())

    local_embeddings = OllamaEmbeddings(model=data["MODEL_NAME"])
    vectorstore = Chroma(persist_directory=chroma_db_path, embedding_function=local_embeddings)

    return vectorstore

def search(modelID, question, k):
    
    chroma_db_path = os.getenv("CHROMA_PATH") + "/" + modelID
    data = eval(open(chroma_db_path + "\info.info", "r", encoding="UTF-8").read())

    local_embeddings = OllamaEmbeddings(model=data["MODEL_NAME"])
    vectorstore = Chroma(persist_directory=chroma_db_path, embedding_function=local_embeddings)

    resDoc = vectorstore.similarity_search(question, k=k)
    return resDoc


def find_chroma_db(chroma_db_path, modelName):

    required_files = ["chroma.sqlite3", "info.info"]
    
    if not os.path.exists(chroma_db_path):
        return False
    
    for file in required_files:
        if not os.path.exists(os.path.join(chroma_db_path, file)):
            return False
    
    try:
        data = eval(open(chroma_db_path + "\info.info", "r", encoding="UTF-8").read())
        if data["MODEL_NAME"] != modelName:
            raise "ERROR"
    except:

        if os.path.exists(chroma_db_path):
            shutil.rmtree(chroma_db_path)
            print("Old vector bank removed. Will be recreated with new dimension.")

        return False
    
        
    local_embeddings = OllamaEmbeddings(model=modelName)
    vectorstore = Chroma(persist_directory=chroma_db_path, embedding_function=local_embeddings)

    if vectorstore._collection.count() == 0:
        return False
            
    return True


def genRAG_folder(path, modelID, modelName, chunk_size,chunk_overlap):

    chroma_db_path =  os.getenv("CHROMA_PATH") + "/" + modelID

    if not os.path.exists(chroma_db_path):
        os.mkdir(chroma_db_path)

    if find_chroma_db(chroma_db_path, modelName):
        return

    agentFiles = os.listdir(path)
    if len(agentFiles) == 0:
        return ""

    all_docs = []

    for file in agentFiles:

        file_path = path + "\\" + file
        doc = loadFile(file_path)

        if doc != False:
            all_docs.extend(doc)
        
        print("Loading", file)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    all_splits = text_splitter.split_documents(all_docs)

    print("Chunks",len(all_splits))

    if not params_check.checkModel(modelName):
        raise "Error to find model"

    os.makedirs(chroma_db_path, exist_ok=True)

    local_embeddings = OllamaEmbeddings(model=modelName)
    Chroma.from_documents(documents=all_splits, embedding=local_embeddings, persist_directory=chroma_db_path)
    
    payload = {"DATE": datetime.datetime.now(), "MODEL_NAME": modelName}
    open(chroma_db_path + "\info.info", "w", encoding="UTF-8").write(str(payload))



