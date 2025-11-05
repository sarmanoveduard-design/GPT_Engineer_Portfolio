# 🟣 RAG Consultant OPOS

### 🎯 Project Overview
AI consultant for industrial safety documentation (ФНП ПС).  
Implements hybrid retrieval with **FAISS (semantic)** and **BM25 (keyword)** search,  
plus citation-based grounding for verified answers.

---

### ⚙️ Tech Stack
- **Language:** Python 3.11  
- **Frameworks:** LangChain, LangGraph  
- **Retrievers:** FAISS + BM25  
- **Evaluation:** Citation tracing, hybrid vs dense comparison  
- **Libraries:** openai, rank-bm25, faiss, pandas

---

### 🧩 Key Features
- Hybrid search (dense + sparse) for industrial safety documentation.  
- Chunked document embeddings with metadata.  
- Context-aware answer generation with `[chunk=N]` citations.  
- Benchmarking baseline vs hybrid retrievers.

---

### 🧱 Structure
```
RAG_Consultant_OPOS/
│
├── main.py
├── rag_pipeline.py
├── retrievers/
│ ├── dense_faiss.py
│ ├── sparse_bm25.py
│ └── hybrid_merge.py
├── prompts.py
├── utils.py
└── README.md
```
---

### 📊 Example Use
> **Q:** Где должны располагаться стоп-краны в пассажирском составе?  
> **A:** В каждом межвагонном тамбуре. [chunk=145]

---

### 🧠 Skills Demonstrated
- RAG pipeline construction  
- LangGraph node design  
- Hybrid retrieval logic  
- Citation validation  
- Vectorization & FAISS/BM25 integration
