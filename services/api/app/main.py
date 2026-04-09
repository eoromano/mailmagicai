from fastapi import FastAPI

from app.routes import catchup, draft_reply, extract_asks, summarize, triage

app = FastAPI(title="Inbox Triage API", version="0.1.0")

app.include_router(triage.router)
app.include_router(summarize.router)
app.include_router(extract_asks.router)
app.include_router(draft_reply.router)
app.include_router(catchup.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
