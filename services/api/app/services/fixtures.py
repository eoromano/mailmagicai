from app.schemas.common import EmailMessage, EmailThread
from app.schemas.responses import UserSettings

DEFAULT_USER_SETTINGS = UserSettings(
    display_name="You",
    email_address="you@example.com",
    signature="Thanks,\nYou",
    reply_tone="neutral",
    include_draft_replies=True,
    show_thought_partner=True,
    vip_senders=["maya@example.com", "priya@example.com"],
    priority_domains=["example.com"],
    urgency_keywords=["today", "asap", "blocker"],
    copied_only_keywords=["for visibility", "fyi"],
    draft_voice_preferences=["concise", "executive"],
    save_history=True,
    mock_mode=True,
)


def thread_needs_action_now() -> EmailThread:
    return EmailThread(
        id="thread-needs-action",
        subject="Need your approval today for customer response",
        participants=["Maya Patel", "Jordan Lee", "You"],
        message_count=3,
        unread_count=2,
        last_message_at="2026-04-08T16:42:00Z",
        messages=[
            EmailMessage(
                id="msg-1",
                from_name="Maya Patel",
                from_email="maya@example.com",
                to_recipients=["you@example.com"],
                cc_recipients=["jordan@example.com"],
                sent_at="2026-04-08T15:30:00Z",
                body_text="Can you review and approve the reply today? Please decide before 5pm.",
                is_unread=True,
            )
        ],
    )


def thread_likely_needs_reply() -> EmailThread:
    return EmailThread(
        id="thread-likely-reply",
        subject="Can you confirm next week's kickoff?",
        participants=["Alex Kim", "You"],
        message_count=1,
        unread_count=1,
        last_message_at="2026-04-08T11:00:00Z",
        messages=[
            EmailMessage(
                id="msg-1",
                from_name="Alex Kim",
                from_email="alex@example.com",
                to_recipients=["you@example.com"],
                cc_recipients=[],
                sent_at="2026-04-08T11:00:00Z",
                body_text="Hi You, can you confirm whether next week's kickoff still works for you?",
                is_unread=True,
            )
        ],
    )


def thread_important_fyi() -> EmailThread:
    return EmailThread(
        id="thread-fyi",
        subject="Weekly launch status update",
        participants=["Launch Ops", "Team", "You"],
        message_count=1,
        unread_count=1,
        last_message_at="2026-04-08T09:00:00Z",
        messages=[
            EmailMessage(
                id="msg-1",
                from_name="Launch Ops",
                from_email="launch-ops@example.com",
                to_recipients=["team@example.com"],
                cc_recipients=["you@example.com"],
                sent_at="2026-04-08T09:00:00Z",
                body_text="FYI: weekly status update. No action needed, but sharing the latest milestone summary.",
                is_unread=True,
            )
        ],
    )


def thread_copied_only() -> EmailThread:
    return EmailThread(
        id="thread-copied-only",
        subject="Vendor contract review",
        participants=["Legal", "Procurement", "You"],
        message_count=1,
        unread_count=1,
        last_message_at="2026-04-08T10:00:00Z",
        messages=[
            EmailMessage(
                id="msg-1",
                from_name="Legal Team",
                from_email="legal@example.com",
                to_recipients=["procurement@example.com"],
                cc_recipients=["you@example.com"],
                sent_at="2026-04-08T10:00:00Z",
                body_text="Procurement, please review the vendor redlines. Copying You for visibility.",
                is_unread=True,
            )
        ],
    )


def thread_low_signal_noise() -> EmailThread:
    return EmailThread(
        id="thread-noise",
        subject="Build passed on main",
        participants=["CI Bot", "You"],
        message_count=1,
        unread_count=1,
        last_message_at="2026-04-08T08:00:00Z",
        messages=[
            EmailMessage(
                id="msg-1",
                from_name="CI Bot",
                from_email="noreply-ci@example.com",
                to_recipients=["eng-all@example.com"],
                cc_recipients=["you@example.com"],
                sent_at="2026-04-08T08:00:00Z",
                body_text="Automated notice: build passed on main. This is a broad status update.",
                is_unread=True,
            )
        ],
    )


def thread_at_risk_of_being_missed() -> EmailThread:
    return EmailThread(
        id="thread-at-risk",
        subject="Quick decision on pricing page copy",
        participants=["Priya Rao", "You"],
        message_count=1,
        unread_count=1,
        last_message_at="2026-03-31T09:00:00Z",
        messages=[
            EmailMessage(
                id="msg-1",
                from_name="Priya Rao",
                from_email="priya@example.com",
                to_recipients=["you@example.com"],
                cc_recipients=[],
                sent_at="2026-03-31T09:00:00Z",
                body_text="Following up in case this got buried. Could you decide on the pricing page copy when you can?",
                is_unread=True,
            )
        ],
    )


def thread_for_summary_exec() -> EmailThread:
    return EmailThread(
        id="thread-summary-exec",
        subject="Board prep and customer escalation follow-up",
        participants=["Chief of Staff", "Finance", "You"],
        message_count=4,
        unread_count=2,
        last_message_at="2026-04-08T18:20:00Z",
        messages=[
            EmailMessage(
                id="msg-1",
                from_name="Chief of Staff",
                from_email="cos@example.com",
                to_recipients=["you@example.com"],
                cc_recipients=["finance@example.com"],
                sent_at="2026-04-08T09:00:00Z",
                body_text="Can you review the board prep draft and confirm the customer escalation posture by today?",
                is_unread=False,
            ),
            EmailMessage(
                id="msg-2",
                from_name="Finance",
                from_email="finance@example.com",
                to_recipients=["you@example.com"],
                cc_recipients=[],
                sent_at="2026-04-08T11:30:00Z",
                body_text="Waiting on you for the final pricing note before I update the board appendix.",
                is_unread=True,
            ),
            EmailMessage(
                id="msg-3",
                from_name="Chief of Staff",
                from_email="cos@example.com",
                to_recipients=["you@example.com"],
                cc_recipients=[],
                sent_at="2026-04-08T17:45:00Z",
                body_text="> Earlier thread below\nPlease decide whether we can tell the customer Monday is still the target. This is the current blocker.",
                is_unread=True,
            ),
        ],
    )


def thread_for_summary_repeated_quotes() -> EmailThread:
    return EmailThread(
        id="thread-summary-quotes",
        subject="Weekly team update",
        participants=["Ops Lead", "You"],
        message_count=2,
        unread_count=1,
        last_message_at="2026-04-08T14:00:00Z",
        messages=[
            EmailMessage(
                id="msg-1",
                from_name="Ops Lead",
                from_email="ops@example.com",
                to_recipients=["you@example.com"],
                cc_recipients=[],
                sent_at="2026-04-08T13:00:00Z",
                body_text="Status update: launch checklist is complete. No action needed right now.",
                is_unread=False,
            ),
            EmailMessage(
                id="msg-2",
                from_name="Ops Lead",
                from_email="ops@example.com",
                to_recipients=["you@example.com"],
                cc_recipients=[],
                sent_at="2026-04-08T14:00:00Z",
                body_text="> Status update: launch checklist is complete. No action needed right now.\nFYI: customer note went out successfully.",
                is_unread=True,
            ),
        ],
    )


def thread_for_ask_extraction_explicit() -> EmailThread:
    return EmailThread(
        id="thread-asks-explicit",
        subject="Please review and approve the partner memo",
        participants=["Maya Patel", "You", "Jordan Lee"],
        message_count=2,
        unread_count=1,
        last_message_at="2026-04-08T16:00:00Z",
        messages=[
            EmailMessage(
                id="msg-1",
                from_name="Maya Patel",
                from_email="maya@example.com",
                to_recipients=["you@example.com"],
                cc_recipients=["jordan@example.com"],
                sent_at="2026-04-08T16:00:00Z",
                body_text=(
                    "Can you review the partner memo and approve the final version by 5pm today? "
                    "Please reply once done."
                ),
                is_unread=True,
            )
        ],
    )


def thread_for_ask_extraction_implicit() -> EmailThread:
    return EmailThread(
        id="thread-asks-implicit",
        subject="Pricing page copy follow-up",
        participants=["Priya Rao", "You", "Design"],
        message_count=2,
        unread_count=1,
        last_message_at="2026-04-09T10:00:00Z",
        messages=[
            EmailMessage(
                id="msg-1",
                from_name="Priya Rao",
                from_email="priya@example.com",
                to_recipients=["you@example.com"],
                cc_recipients=["design@example.com"],
                sent_at="2026-04-09T10:00:00Z",
                body_text=(
                    "Following up in case this got buried. We are blocked on the pricing page copy until you decide "
                    "which headline to ship."
                ),
                is_unread=True,
            )
        ],
    )


def thread_for_draft_generation() -> EmailThread:
    return EmailThread(
        id="thread-draft-generation",
        subject="Customer escalation response and board note",
        participants=["Chief of Staff", "Maya Patel", "You"],
        message_count=3,
        unread_count=2,
        last_message_at="2026-04-08T17:30:00Z",
        messages=[
            EmailMessage(
                id="msg-1",
                from_name="Chief of Staff",
                from_email="cos@example.com",
                to_recipients=["you@example.com"],
                cc_recipients=["maya@example.com"],
                sent_at="2026-04-08T15:00:00Z",
                body_text="Can you confirm the customer response posture today?",
                is_unread=True,
            ),
            EmailMessage(
                id="msg-2",
                from_name="Maya Patel",
                from_email="maya@example.com",
                to_recipients=["you@example.com"],
                cc_recipients=[],
                sent_at="2026-04-08T17:30:00Z",
                body_text="Please decide whether we can say Monday is still the target and reply once aligned.",
                is_unread=True,
            ),
        ],
    )


def unread_threads_for_catchup() -> list[EmailThread]:
    return [
        thread_needs_action_now(),
        thread_likely_needs_reply(),
        thread_important_fyi(),
        thread_copied_only(),
        thread_low_signal_noise(),
        thread_at_risk_of_being_missed(),
        thread_important_fyi(),
    ]
