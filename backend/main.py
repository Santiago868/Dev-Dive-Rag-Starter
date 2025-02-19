import logging
import asyncio
import os
import pickle
import faiss
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

from langchain_ollama.chat_models import ChatOllama
from langchain_ollama.embeddings import OllamaEmbeddings

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()
load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    llm = ChatOllama(model="llama3.2")
    #Utilizes same embeddings model we used to precompute embeddings
    embedding_model = OllamaEmbeddings(model="nomic-embed-text")
    logger.info("Initialized ChatOllama and OllamaEmbeddings successfully.")
except Exception as e:
    logger.exception("Error initializing Ollama models: %s", e)
    raise

# Attempt to load precomputed embeddings
precomputed_path = Path("precomputed_embeddings.pkl")
if precomputed_path.exists():
    with open(precomputed_path, "rb") as f:
        data = pickle.load(f)
    docs = data["docs"]
    embeddings_list = data["embeddings"]
    logger.info("Loaded precomputed embeddings.")
else:
    logger.error("Precomputed embeddings not found. Please run embeddings.py first.")
    raise Exception("Precomputed embeddings not found. Please run embeddings.py first.")

docs = [doc.copy(update={"id": str(i)}) for i, doc in enumerate(docs)]

try:
    sample_embedding = embedding_model.embed_query("sample")
    embedding_dim = len(sample_embedding)
    logger.debug("Sample embedding dimension: %d", embedding_dim)
except Exception as e:
    logger.exception("Error computing sample embedding: %s", e)
    raise

index = faiss.IndexFlatL2(embedding_dim)

# Create vector store from precomputed embeddings.Add code here.


try:
    vector_store.add_documents(documents=docs)
    logger.info("Added %d documents to the vector store.", len(docs))
except Exception as e:
    logger.exception("Error adding documents to vector store: %s", e)
    raise

#Vector store as retriever to get the embeddings
retriever = vector_store.as_retriever()

# Define the system and human prompts for the chat pipeline. Add code here.


# Create the LangChain pipeline for question-answering. Adds code here.


@app.post("/query")
async def query_rag(payload: dict):
    if "query" not in payload:
        logger.error("Query key missing in payload: %s", payload)
        raise HTTPException(status_code=400, detail="Missing 'query' in request.")
    try:
        logger.info("Received query: %s", payload["query"])
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, lambda: rag_chain.invoke({"input": payload["query"]}))
        prompts =  await loop.run_in_executor(None, lambda: rag_chain.get_prompts())
        logger.info("Prompts: %s", prompts)
        context = result.get("context")
        answer = result.get("answer") or result.get("result") or "No answer returned."
        logger.info("Chain output: %s", result)
        logger.info("Answer: %s", answer)
        return {"answer": answer, "context": context}
    except Exception as e:
        logger.exception("Error processing query: %s", e)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
