# ⚖️ AI Consumer Rights Defender

An Autonomous Legal Agent that fights for consumer rights. It uses **Llama 3 (Groq)** for legal reasoning and **Tavily Search** to fetch real-time laws/regulations, preventing hallucinations.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![LangChain](https://img.shields.io/badge/LangChain-v0.2-green)
![Llama 3](https://img.shields.io/badge/Model-Llama%203%20(Groq)-orange)

## 🚀 Key Features
* **Architecture:** Decoupled Frontend (Streamlit) & Backend (LangChain Logic).
* **RAG-Optimized:** Uses Tavily API to fetch live legal statutes (e.g., *Consumer Protection Act 2019*) before drafting.
* **Anti-Hallucination:** System prompts enforce a "No Invention" rule—if a law isn't found, it defaults to general principles.
* **Speed:** Optimized for sub-3-second responses using Llama-3-8b-Instant.

## 🛠️ Tech Stack
* **LLM:** Llama 3 (via Groq Cloud)
* **Orchestration:** LangChain
* **Tools:** Tavily Search API
* **Frontend:** Streamlit

## 🛠️ Deployed 
https://lawyerdost.streamlit.app/
