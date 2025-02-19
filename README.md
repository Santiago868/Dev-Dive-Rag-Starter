# Ollama-Based RAG Project

This project demonstrates a Retrieval-Augmented Generation (RAG) pipeline using local models with Ollama. The backend is built with FastAPI and uses a CSV file as the knowledge base. The system uses local Ollama models for embeddings and chat generation.

## Prerequisites

- **Python 3.8+** installed on your system.
   - On MacOS
     - `brew install python3`
   - On Windows
     - [Download](https://www.python.org/downloads/windows/)


- **Ollama** installed and models pulled.  
  - See [Ollama's Installation Guide](https://ollama.com/download) for details.
  - `Ollama pull nomic-embed-text `
  - `Ollama pull llama3.2`
  
- **Knowledge Base** 
  - Add your info into the csv in data.

## Setup Instructions

## 1. Clone the Repository

Clone this repository (or download the code) to your local machine.

## 2. Setup Backend

Open the backend folder and run these commands


### Create & Activate Virtual Enviroment

### On macOS/Linux:
`python3 -m venv venv`

`source venv/bin/activate`


### On Windows:
`python -m venv venv`

`venv\Scripts\activate`

### Install Dependencies

`pip install --upgrade pip`

`pip install -r requirements.txt`

## 3. Setup Frontend
Open the frontend folder and run these commands

### Install Dependencies
`npm install`

## 4. Running Application
- Run `python embeddings.py`
- Start Backend 
  - `uvicorn main:app --reload`
- Start Frontend
  - `npm run dev`
- Alternatively 
  - ` curl -X POST "http://127.0.0.1:8000/query" -H "Content-Type: application/json" -d '{"query": "What is {your name} fav movie"}' `
