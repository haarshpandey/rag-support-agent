"""
Build the vector index for the RAG support agent.

Loads every .md/.txt file in docs/, splits them into overlapping chunks,
embeds them, and persists a FAISS index to ./index/.

Run:  python ingest.py
Requires: OPENAI_API_KEY in the environment (see .env.example)
"""

import os
from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

DOCS_DIR = Path(__file__).parent / "docs"
INDEX_DIR = Path(__file__).parent / "index"


def main() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("Set OPENAI_API_KEY first (see .env.example).")

    loader = DirectoryLoader(
        str(DOCS_DIR), glob="**/*.md", loader_cls=TextLoader, loader_kwargs={"encoding": "utf8"}
    )
    documents = loader.load()
    print(f"Loaded {len(documents)} documents from {DOCS_DIR}")

    splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=80)
    chunks = splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks")

    embeddings = OpenAIEmbeddings()
    store = FAISS.from_documents(chunks, embeddings)
    store.save_local(str(INDEX_DIR))
    print(f"Index saved to {INDEX_DIR} ({store.index.ntotal} vectors)")


if __name__ == "__main__":
    main()
