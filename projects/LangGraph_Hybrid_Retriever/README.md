# 🟡 LangGraph Hybrid Retriever

### 🎯 Project Overview
Hybrid retriever built with **LangGraph**, combining **semantic (FAISS)** and **keyword (BM25)** search for improved accuracy and recall.  
Includes evaluation experiments comparing baseline dense retrieval vs hybrid strategy with citation validation.

---

### ⚙️ Tech Stack
- **Language:** Python 3.11  
- **Framework:** LangGraph  
- **Retrievers:** FAISS (dense) + BM25 (sparse)  
- **Evaluation:** LangSmith tracing & manual comparison  
- **Libraries:** sentence-transformers, rank-bm25, openai, pandas

---

### 🧩 Key Features
- Implements **node_hybrid_retrieve** for combining two retrievers with α-weighted blending.  
- Evaluates performance across multiple question sets.  
- Generates structured output showing citations `[chunk=N]` for traceability.  
- Provides automated baseline vs hybrid quality comparison.

---

### 🧱 Project Structure
```
LangGraph_Hybrid_Retriever/
│
├── main.py
├── node_hybrid_retrieve.py
├── evaluate_baseline_vs_hybrid.py
├── prompts.py
├── utils.py
├── data/
│ ├── rules_texts/
│ └── questions.txt
├── outputs/
│ ├── results_hybrid.txt
│ ├── eval_report.md
│ └── plot_accuracy.png
└── README.md
```

---

### 📊 Evaluation Example
| Question | Dense | Hybrid |
|-----------|--------|---------|
| What includes “Safety justification”? | Partial | ✅ Correct, with citation |
| Where must stop valves be installed? | Incomplete | ✅ Retrieved correct chunk |
| When can testing be replaced with documentation review? | Missed | ✅ Found in hybrid |

---

### 🚀 How It Works
1. Load and chunk documents (industrial safety rules).  
2. Embed chunks using **all-MiniLM-L6-v2**.  
3. Build FAISS and BM25 indices.  
4. LangGraph node merges results with α=0.7 weighting.  
5. Evaluate precision, recall, and citation consistency.

---

### 🧠 Skills Demonstrated
- LangGraph pipeline development  
- Hybrid retrieval logic (dense + sparse)  
- Evaluation and visualization  
- FAISS & BM25 integration  
- LangSmith tracing and benchmarking

---

### 🧩 Related Tools
LangGraph · LangChain · FAISS · BM25 · LangSmith · OpenAI API
