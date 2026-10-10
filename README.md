# 📊 Natural-Language Data Analyst Agent

Ask questions about your CSV in plain English. A local LLM (via [Ollama](https://ollama.com)) writes **pandas / NumPy** code, runs it in a **safe sandbox**, fixes its own mistakes, and explains the answer.

> Example: *"Which region has the highest total revenue?"* → the agent writes `df.groupby("region")["revenue"].sum().idxmax()`, runs it safely, and answers **"West"**.

![python](https://img.shields.io/badge/python-3.10%2B-blue) ![license](https://img.shields.io/badge/license-MIT-green)

---

## ✨ Features

- **Plain-English questions** over any CSV file
- **Schema-aware prompting**: the model sees column names, types, and sample values
- **Safe code execution**: blocks imports, file access, and dunder tricks; enforces a timeout
- **Self-repair loop**: if the code fails, the error is sent back to the model for a fix
- **Evaluation suite**: measures accuracy against pandas-computed ground truth
- **100% local and free**: runs on Ollama, no API keys needed
- **Streamlit UI** and **pytest** tests with GitHub Actions CI

## 🧠 How it works

```
 Your question ──► Prompt (schema + rules) ──► Ollama LLM ──► Python code
                                                                  │
                         ┌────────── error message ◄── fail ──────┤
                         ▼                                        ▼
                  LLM fixes the code            AST safety check → Sandbox run (timeout)
                  (up to N retries)                               │ success
                                                                  ▼
                                                  Result ──► Plain-English explanation
```

## 🚀 Quick start

**Prerequisites:** Python 3.10+, [Ollama](https://ollama.com/download), Git

```bash
# 1. Clone
git clone https://github.com/<your-username>/nl-data-analyst-agent.git
cd nl-data-analyst-agent

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download a model (one time, ~4-5 GB)
ollama list   # make sure llama3.1:latest is installed (or: ollama pull llama3.1)

# 5. Generate sample data
python data/make_sample_data.py

# 6. Launch the app
streamlit run app.py
```

Open the link shown in the terminal (usually http://localhost:8501), upload `data/sales.csv`, and ask a question.

### Try these questions
- What is the total revenue?
- Which region has the highest total revenue?
- How many orders are in the Electronics category?
- What is the average unit price?
- Which category sells the most units?

## 🗂️ Project structure

```
nl-data-analyst-agent/
├── analyst_agent/
│   ├── llm.py        # talks to Ollama
│   ├── prompts.py    # prompt templates + schema summary
│   ├── sandbox.py    # safety checks + timeout runner
│   └── agent.py      # ask → code → run → retry loop
├── app.py            # Streamlit UI
├── data/make_sample_data.py
├── eval/run_eval.py  # accuracy benchmark
├── docs/SETUP_GUIDE.md
├── tests/            # pytest tests
└── .github/workflows/ci.yml
```

## 🛡️ Safety design

| Layer | What it does |
|---|---|
| AST check | Rejects `import`, `eval`, `exec`, `open`, underscore attributes, file read/write methods |
| Restricted builtins | Only a small allow-list of Python built-ins is available |
| Timeout | Code runs in a separate process and is killed after 10 seconds |
| Data copy | The agent works on a copy of your DataFrame, never the original |

> ⚠️ This is a learning-grade sandbox, **not** a hardened security boundary. For production, run generated code inside a locked-down container (no network, read-only filesystem, CPU/memory limits).

## 📈 Evaluation

Run the benchmark:

```bash
python eval/run_eval.py
```

| Model | Questions | Correct | Accuracy | Avg. retries |
|---|---|---|---|---|
| llama3.1:latest | 8 | _fill in_ | _fill in_ | _fill in_ |
| qwen2.5-coder:7b (optional) | 8 | _fill in_ | _fill in_ | _fill in_ |

## ⚠️ Limitations

- Small local models can still write wrong logic that runs without errors
- Charts are not supported yet
- Works on one CSV at a time; large files are limited by memory

## 🗺️ Roadmap

- [ ] Chart generation (Matplotlib / Plotly)
- [ ] Provider switch: Ollama ↔ Groq / Gemini free tier
- [ ] Larger eval set (30-50 questions)
- [ ] Docker image and Hugging Face Spaces demo
- [ ] Conversation memory for follow-up questions

## 🧪 Run tests

```bash
python -m pytest -q
```

## 📄 License

MIT. Free to use for learning and portfolio purposes.
