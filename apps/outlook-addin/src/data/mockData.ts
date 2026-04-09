import type { EmailThread, TriageResponse } from "../../../../packages/shared-types/src";

export const sampleThread: EmailThread = {
  id: "thread-q2-launch",
  subject: "Q2 launch timeline and customer escalation follow-up",
  participants: ["Maya Patel", "Jordan Lee", "You"],
  messageCount: 5,
  unreadCount: 3,
  lastMessageAt: "2026-04-08T16:42:00Z",
  messages: [
    {
      id: "msg-1",
      from: "Maya Patel",
      sentAt: "2026-04-08T13:05:00Z",
      body:
        "Can you confirm whether we can move the launch review to Friday and send the customer-safe status update today?"
    },
    {
      id: "msg-2",
      from: "Jordan Lee",
      sentAt: "2026-04-08T14:15:00Z",
      body:
        "I can update the deck, but I need the revised timeline and the owner for the escalation response."
    },
    {
      id: "msg-3",
      from: "Maya Patel",
      sentAt: "2026-04-08T16:42:00Z",
      body:
        "Main blocker is deciding who sends the reply to the customer and whether we can commit to Monday for the fix."
    }
  ]
};

export const sampleTriageResponse: TriageResponse = {
  threadId: sampleThread.id,
  verdict: "Needs reply today",
  rationale:
    "The thread contains an open customer-facing commitment question and a scheduling decision that other teammates are waiting on.",
  summary: {
    overview:
      "The team is aligning on a revised launch review date and who should respond to a customer escalation.",
    bullets: [
      "Maya asked whether the launch review can move to Friday.",
      "Jordan needs the revised timeline and the reply owner.",
      "The unresolved decision is whether to promise a Monday fix to the customer."
    ]
  },
  directAsks: [
    {
      id: "ask-1",
      owner: "You",
      request: "Confirm whether the launch review should move to Friday."
    },
    {
      id: "ask-2",
      owner: "You",
      request: "Decide who will send the customer response and what timeline to commit to."
    }
  ],
  draftReply:
    "Hi Maya and Jordan,\n\nI agree we should move the launch review to Friday. I will send the customer update today and position Monday as our target pending final verification.\n\nI will share the revised timeline shortly.\n\nThanks,\nYou",
  catchUpList: [
    {
      id: "catch-up-1",
      title: "Reply needed",
      detail: "A customer-safe response owner and timeline are still unconfirmed."
    },
    {
      id: "catch-up-2",
      title: "Decision blocker",
      detail: "Jordan cannot finalize the deck until the revised timeline is shared."
    },
    {
      id: "catch-up-3",
      title: "Scheduling change",
      detail: "The launch review may move to Friday and needs explicit confirmation."
    }
  ]
};
