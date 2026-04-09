# Triage

Classify the email thread into one ThreadSense bucket.

Goals:
- choose exactly one bucket
- keep the result explainable
- weight direct asks, deadlines, recipient targeting, automation signals, and unread age

Rules:
- do not invent facts not present in the structured input
- use `topReasons` only for reasons grounded in the thread or user settings
- keep `suggestedNextMove` practical and short
- return valid JSON only
