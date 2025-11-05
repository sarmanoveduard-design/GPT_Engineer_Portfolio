# 🔵 NeuroProtocolist

### 🎯 Project Overview
An intelligent assistant that transcribes and structures meeting dialogues.  
It processes audio input, converts it to text (STT), summarizes key points,  
and formats output into professional meeting minutes.

---

### ⚙️ Tech Stack
- **Language:** Python 3.11  
- **Models:** Whisper (STT), GPT-4o-mini (summarization)  
- **Frameworks:** LangChain  
- **Output:** Structured JSON and Markdown summaries

---

### 🧩 Key Features
- Converts meeting recordings into text via Whisper STT.  
- Summarizes dialogues and identifies action points.  
- Outputs both detailed and short summaries.  
- Automatically classifies meeting topics (e.g., technical, business, HR).

---

### 🧱 Structure
```
NeuroProtocolist/
│
├── main.py
├── stt_module.py
├── summary_agent.py
├── utils.py
└── outputs/
├── summary.md
└── protocol.json
```

---

### 🧠 Skills Demonstrated
- Whisper API integration (speech-to-text)  
- GPT summarization and JSON formatting  
- Contextual data structuring  
- Clean, reusable code organization
