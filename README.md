# RAG Support Agent

A retrieval-augmented generation (RAG) Q&A agent built with **LangChain**: it answers questions over your own documents by retrieving the most relevant chunks and grounding every answer in them — with source citations and an explicit "I don't know" when the answer isn't in the docs.

## How it works

```
docs/*.md --ingest.py--> FAISS index --app.py--> question
                                              |--> retrieve top-4 chunks
                                              |--> ChatOpenAI answers from context only
                                              |--> answer + source documents
```

## Quickstart

```bash
pip install -r requirements.txt
cp .env.example .env        # add your OPENAI_API_KEY
python ingest.py            # build the vector index from docs/
python app.py               # ask questions
```

Example:

```
You: How long is a password reset link valid?
Agent: A password reset link is valid for 30 minutes and can only be used once.
Sources: docs/password-reset.md
```

## Design choices

- **Chunking**: 600 chars with 80-char overlap — keeps procedures (like SSO setup steps) intact within a chunk
- **Grounded prompting**: the system prompt forbids answering from outside the retrieved context, which kills most hallucinations
- **Source citations**: every answer lists which documents it came from, so it's auditable

## Files

- `ingest.py` — document loading, chunking, embedding, FAISS index build
- `app.py` — interactive Q&A loop with retrieval + cited answers
- `docs/` — sample support docs (swap in your own)
- `.env.example` — required configuration

## Limitations / next steps

- Embeddings and LLM calls need an `OPENAI_API_KEY` (swap in any LangChain-compatible embeddings/chat model)
- Sample docs are fictional; point `ingest.py` at real docs for a production use case
- Natural extensions: conversation memory, hybrid (BM25 + vector) retrieval, eval set with faithfulness scoring
