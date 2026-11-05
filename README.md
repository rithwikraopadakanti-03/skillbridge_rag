# SkillBridge Academic Insights (Agentic RAG challenge)

Streamlit front end plus the Kaggle notebook solution.

## Run
    pip install -r requirements.txt
    streamlit run app.py

## Layout
- `app.py`: Streamlit UI (ask a question, student lookup, batch/course dashboard, run test set)
- `engine.py`: deterministic policy engine (grading, attendance, alerts, progress, aggregates). 100/100 on train.csv
- `data/`: dataset, policy docs, query files (set `SB_DATA_DIR` to use another location)
- `notebook/agentic_rag_solution.ipynb`: Kaggle notebook (FAISS + Groq agent fallback)
- `submission.csv`: generated predictions for test.csv

The optional Groq key in the sidebar enables an LLM fallback for questions the rules don't recognise (untested against the live API).
