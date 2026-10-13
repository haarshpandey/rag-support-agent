"""
Ask questions over your own documents (RAG).

Loads the FAISS index built by ingest.py, retrieves the most relevant chunks
for each question, and answers with ChatOpenAI — always citing which
documents the answer came from.

Run:  python app.py
      (then type questions; 'quit' to exit)
Requires: OPENAI_API_KEY in the environment (see .env.example)
"""

import os
from pathlib import Path

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

INDEX_DIR = Path(__file__).parent / "index"

SYSTEM_PROMPT = """You are a helpful support assistant. Answer the question using ONLY
the context below. If the answer is not in the context, say you don't know
rather than guessing. Cite the source document for each claim.

Context:
{context}

Question: {question}
"""


def build_chain() -> RetrievalQA:
    embeddings = OpenAIEmbeddings()
    store = FAISS.load_local(
        str(INDEX_DIR), embeddings, allow_dangerous_deserialization=True
    )
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    prompt = PromptTemplate(
        template=SYSTEM_PROMPT, input_variables=["context", "question"]
    )
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=store.as_retriever(search_kwargs={"k": 4}),
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True,
    )


def main() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("Set OPENAI_API_KEY first (see .env.example).")
    if not INDEX_DIR.exists():
        raise SystemExit("No index found. Run `python ingest.py` first.")

    qa = build_chain()
    print("RAG support agent ready. Ask a question (type 'quit' to exit).")
    while True:
        question = input("\nYou: ").strip()
        if question.lower() in {"quit", "exit", "q"}:
            break
        if not question:
            continue
        result = qa.invoke({"query": question})
        print(f"\nAgent: {result['result']}")
        sources = {d.metadata.get("source", "unknown") for d in result["source_documents"]}
        print(f"Sources: {', '.join(sorted(sources))}")


if __name__ == "__main__":
    main()
