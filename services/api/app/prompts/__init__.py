from app.prompts.loader import load_prompt

CATCHUP_PROMPT = load_prompt("catchup")
DRAFT_REPLY_PROMPT = load_prompt("draft_reply")
EXTRACT_ASKS_PROMPT = load_prompt("extract_asks")
SUMMARIZE_THREAD_PROMPT = load_prompt("summarize")
THOUGHT_PARTNER_PROMPT = load_prompt("thought_partner")
TRIAGE_THREAD_PROMPT = load_prompt("triage")

__all__ = [
    "CATCHUP_PROMPT",
    "DRAFT_REPLY_PROMPT",
    "EXTRACT_ASKS_PROMPT",
    "SUMMARIZE_THREAD_PROMPT",
    "THOUGHT_PARTNER_PROMPT",
    "TRIAGE_THREAD_PROMPT",
]
