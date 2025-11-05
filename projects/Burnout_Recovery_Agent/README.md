# 🟠 Burnout Recovery Agent

### 🎯 Project Overview
An autonomous GPT-based agent designed to develop **personalized recovery strategies** after cognitive burnout.  
It considers sleep, dopamine balance, nutrition, digital load, and mental state — forming practical, step-by-step recommendations.

---

### ⚙️ Tech Stack
- **Language:** Python 3.11  
- **Framework:** LangGraph  
- **LLM:** GPT-4o-mini  
- **Search:** Tavily API  
- **Core Concepts:** Agentic workflows, goal decomposition, loop termination

---

### 🧩 Key Features
- Generates **subtasks dynamically** (e.g., “Find post-stress sleep practices”).  
- Uses **Tavily search** to collect verified materials.  
- Avoids duplication and irrelevant tasks.  
- Stops automatically upon goal achievement or reaching iteration limit.  
- Outputs a **structured recovery plan** tailored to user needs.

---

### 🧱 Структура проекта
```
Burnout_Recovery_Agent/
│
├── main.py
├── prompts.py
├── utils.py
├── langgraph_nodes/
│ ├── search_node.py
│ ├── task_plan_node.py
│ └── result_node.py
└── README.md
```
---

### 🚀 How It Works
1. User sets a global goal: *“Recover cognitive energy after burnout.”*  
2. Agent decomposes it into subtasks (e.g., “find sleep optimization methods”).  
3. Tavily search node retrieves content.  
4. The reasoning node summarizes findings.  
5. Agent completes the cycle consciously (goal reached / limit hit).

---

### 📎 Skills Demonstrated
- LangGraph agent design  
- Autonomous planning and reasoning  
- Tavily web search integration  
- Task deduplication and safe termination  
- JSON-based structured outputs

---

### 💡 Example Output
> **Goal:** Restore cognitive energy  
> **Subtasks:** Sleep improvement, dopamine balance, digital detox, mindfulness  
> **Plan:**  
> 1. Limit screen time before bed  
> 2. Add morning sunlight exposure  
> 3. Practice 10-min breathing exercises  
> 4. Journal mood and focus weekly  
> 5. Track dopamine-friendly habits  
> *(All sources verified via Tavily search)*

---

### 🧠 Related Tools
LangGraph · OpenAI API · Tavily · Python 3.11
