# Setup Guide (Windows / PowerShell)

Follow these steps in order. Run every command from the project root folder
(the folder that contains `app.py`).

## 1. One-time installs
| Tool | Check with |
|---|---|
| Python 3.10+ (tick "Add Python to PATH") | `python --version` |
| Git | `git --version` |
| Ollama | `ollama --version` |
| VS Code + Python extension | optional but recommended |

## 2. Confirm your model
```powershell
ollama list
```
You need `llama3.1:latest`. If it is missing: `ollama pull llama3.1`.
(`nomic-embed-text` is an embedding model and is not used in this project.)

## 3. Create the virtual environment and install packages
```powershell
cd path\to\nl-data-analyst-agent
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```
If activation is blocked:
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, then activate again.
You should see `(.venv)` at the start of the prompt.

## 4. Create sample data
```powershell
python data\make_sample_data.py
```

## 5. Test each layer
```powershell
# a) Does Python talk to Ollama?
python -c "from analyst_agent.llm import ask_llm; print(ask_llm([{'role':'user','content':'Say hello in 5 words'}]))"

# b) Do the safety tests pass?
python -m pytest -q

# c) Does the full agent work in the terminal?
python try_agent.py
```

## 6. Run the app
```powershell
streamlit run app.py
```
Upload `data\sales.csv` and try:
- What is the total revenue?
- Which region has the highest total revenue?
- How many orders are in the Electronics category?

## 7. Run the evaluation
```powershell
python eval\run_eval.py
```
Copy the accuracy numbers into the table in `README.md`.

Compare another model (optional):
```powershell
ollama pull qwen2.5-coder:7b
$env:OLLAMA_MODEL = "qwen2.5-coder:7b"
python eval\run_eval.py
```

## 8. Publish to GitHub
1. On github.com create a new **empty public** repository named `nl-data-analyst-agent`.
2. In PowerShell:
```powershell
git init
git add .
git commit -m "Initial commit: NL data analyst agent"
git branch -M main
git remote add origin https://github.com/<your-username>/nl-data-analyst-agent.git
git push -u origin main
```
3. Open the **Actions** tab and wait for the green check.
4. Edit `README.md`: replace `<your-username>`, add a screenshot/GIF, fill the eval table.
5. Edit `LICENSE`: replace `<your name>`.

## Troubleshooting
| Problem | Fix |
|---|---|
| Connection error to Ollama | Start the Ollama app, or run `ollama serve` |
| `model not found` | `ollama pull llama3.1` |
| `No module named analyst_agent` | Run from the project root; use `python -m pytest` |
| Very slow answers | First call loads the model; close heavy apps; try a smaller model |
| Sandbox seems to hang on Windows | Scripts that call the agent need `if __name__ == "__main__":` |
| Wrong answers | Check the generated code in the app's expander; refine `prompts.py` |

## Good commit checkpoints
1. Project skeleton and sample data
2. Sandbox plus tests
3. Agent loop
4. Streamlit UI
5. Eval results and README table
6. CI badge and screenshots
