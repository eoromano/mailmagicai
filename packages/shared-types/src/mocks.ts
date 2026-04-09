import type {
  CatchUpBriefingItem,
  CatchUpOverview,
  DraftReplySet,
  EmailThread,
  AskExtractionResult,
  ExtractedAsk,
  ThoughtPartnerResult,
  ThreadSummary,
  TriageResult,
  UserSettings
} from "./contracts";

export const exampleEmailThread: EmailThread = {
  id: "thread-q2-launch",
  subject: "Q2 launch timeline and customer escalation follow-up",
  participants: ["Maya Patel", "Jordan Lee", "You"],
  messageCount: 5,
  unreadCount: 3,
  lastMessageAt: "2026-04-08T16:42:00Z",
  messages: [
    {
      id: "msg-1",
      fromName: "Maya Patel",
      fromEmail: "maya@example.com",
      toRecipients: ["you@example.com"],
      ccRecipients: ["jordan@example.com"],
      sentAt: "2026-04-08T13:05:00Z",
      bodyText:
        "Can you confirm whether we can move the launch review to Friday and send the customer-safe status update today?",
      isUnread: false
    },
    {
      id: "msg-2",
      fromName: "Jordan Lee",
      fromEmail: "jordan@example.com",
      toRecipients: ["maya@example.com", "you@example.com"],
      ccRecipients: [],
      sentAt: "2026-04-08T14:15:00Z",
      bodyText:
        "I can update the deck, but I need the revised timeline and the owner for the escalation response.",
      isUnread: true
    },
    {
      id: "msg-3",
      fromName: "Maya Patel",
      fromEmail: "maya@example.com",
      toRecipients: ["you@example.com"],
      ccRecipients: [],
      sentAt: "2026-04-08T16:42:00Z",
      bodyText:
        "Main blocker is deciding who sends the reply to the customer and whether we can commit to Monday for the fix.",
      isUnread: true
    }
  ]
};

export const exampleThreadSummary: ThreadSummary = {
  summary:
    "The team is aligning on a revised launch review date and who should respond to a customer escalation.",
  latestChange:
    "Maya's latest note says the main blocker is deciding who sends the customer reply and whether Monday can be named as the target fix date.",
  unresolvedItems: [
    "Confirm whether the launch review should move to Friday.",
    "Decide who will send the customer response.",
    "Decide whether Monday is safe to mention as the target fix date."
  ],
  whoIsWaitingOnWhom: [
    "Jordan is waiting on you for the revised timeline and reply owner.",
    "Maya is waiting on you for a customer-safe response decision."
  ],
  deadlines: ["today", "Monday"],
  importantContext: [
    "The customer update has external visibility risk.",
    "The launch deck cannot be finalized until ownership and timing are clear."
  ]
};

export const exampleExtractedAsks: ExtractedAsk[] = [
  {
    id: "ask-1",
    text: "Confirm whether the launch review should move to Friday.",
    askType: "confirm",
    owner: "You",
    targetPerson: "Maya Patel",
    dueDate: "Today",
    urgency: "high",
    sourceSnippet: "Can you confirm whether we can move the launch review to Friday..."
  },
  {
    id: "ask-2",
    text: "Decide who will send the customer response and what timeline to commit to.",
    askType: "decide",
    owner: "You",
    targetPerson: "Maya Patel",
    dueDate: "Before end of day",
    urgency: "high",
    sourceSnippet: "Main blocker is deciding who sends the reply to the customer..."
  }
];

export const exampleAskExtractionResult: AskExtractionResult = {
  asks: exampleExtractedAsks,
  inferredMissingReplies: [
    "A direct reply to Maya is still missing on the launch review timing.",
    "The customer response owner has not replied with a commitment yet."
  ],
  inferredBlockers: [
    "Jordan cannot finish the deck until the revised timeline is confirmed.",
    "The customer-safe reply cannot go out until an owner and timeline are chosen."
  ]
};

export const exampleDraftReplySet: DraftReplySet = {
  shortReply:
    "Hi Maya and Jordan,\n\nI am reviewing this now and will send the customer-safe update shortly.\n\nThanks,\nYou",
  strategicReply:
    "Hi Maya and Jordan,\n\nI agree we should move the launch review to Friday. I will send the customer update today and position Monday as our working target pending final verification. I will share the revised timeline shortly.\n\nThanks,\nYou",
  clarifyingReply:
    "Hi Maya and Jordan,\n\nBefore I send the customer update, I want to confirm two points: should we explicitly move the review to Friday, and are we comfortable naming Monday as the target fix date?\n\nThanks,\nYou",
  notesOnWhenToUseEach: {
    shortReply: "Use when you need to acknowledge quickly and buy time without adding new commitments.",
    strategicReply: "Use when you are ready to set direction and align the group on the next move.",
    clarifyingReply: "Use when the thread is missing key facts and a precise follow-up question is safer than committing."
  }
};

const actionBriefingItem: CatchUpBriefingItem = {
  id: "brief-1",
  threadId: "thread-q2-launch",
  subject: "Q2 launch timeline and customer escalation follow-up",
  bucket: "needs_action_now",
  whyItMatters: "A direct decision and customer-facing update are still waiting on you.",
  latestChange:
    "Maya says the blocker is deciding who sends the customer reply and whether Monday is still the target.",
  suggestedNextMove: "Acknowledge now, then lock the owner and safe timeline.",
  waitingOnUser: true
};

export const exampleCatchUpOverview: CatchUpOverview = {
  overview: {
    totalItems: 6,
    needsActionNowCount: 1,
    likelyNeedsReplyCount: 2,
    importantFyiCount: 1,
    copiedOnlyCount: 1,
    lowSignalNoiseCount: 0,
    atRiskCount: 1
  },
  topActionItems: [actionBriefingItem],
  importantFyiItems: [
    {
      id: "brief-2",
      threadId: "thread-fyi",
      subject: "Weekly launch status update",
      bucket: "important_fyi",
      whyItMatters: "Useful context, but no direct ask is waiting on you.",
      latestChange: "Launch Ops shared the weekly milestone summary.",
      suggestedNextMove: "Scan quickly and move on.",
      waitingOnUser: false
    }
  ],
  copiedOnlyItems: [
    {
      id: "brief-3",
      threadId: "thread-copied-only",
      subject: "Vendor contract review",
      bucket: "copied_only",
      whyItMatters: "You are copied for visibility while Procurement owns the next step.",
      latestChange: "Legal asked Procurement to review the redlines.",
      suggestedNextMove: "Monitor only if you get pulled in directly.",
      waitingOnUser: false
    }
  ],
  riskItems: [
    {
      id: "brief-4",
      threadId: "thread-at-risk",
      subject: "Quick decision on pricing page copy",
      bucket: "at_risk_of_being_missed",
      whyItMatters: "The thread is older, still unread, and the sender is following up.",
      latestChange: "Priya says the team is blocked until a decision is made.",
      suggestedNextMove: "Read next and send a catch-up reply.",
      waitingOnUser: true
    }
  ],
  themes: [
    "Several unread threads are waiting on explicit decisions from you.",
    "Customer-facing timing appears in the highest-priority work."
  ],
  suggestedFirst10ToRead: [
    actionBriefingItem,
    {
      id: "brief-4",
      threadId: "thread-at-risk",
      subject: "Quick decision on pricing page copy",
      bucket: "at_risk_of_being_missed",
      whyItMatters: "Older follow-up that may slip further.",
      latestChange: "Priya says the pricing page is blocked.",
      suggestedNextMove: "Read second and respond.",
      waitingOnUser: true
    }
  ]
};

export const exampleThoughtPartnerResult: ThoughtPartnerResult = {
  issue: {
    evidence: [
      "Maya says the blocker is deciding who sends the customer reply.",
      "The thread asks whether Monday can still be named as the target fix date."
    ],
    inference:
      "The real issue is not just scheduling. The team needs an owner and a safe external commitment before they can move."
  },
  explicitAsks: [
    "Confirm whether the launch review should move to Friday.",
    "Decide who sends the customer response.",
    "Decide whether Monday is safe to mention as the target date."
  ],
  implicitDynamics: {
    evidence: [
      "Jordan needs the revised timeline before finishing the deck.",
      "Maya frames the owner and commitment decision as the blocker."
    ],
    inference:
      "Others are waiting on your decision, and the thread has both internal coordination pressure and external customer-risk pressure."
  },
  risks: [
    "If you do nothing, the customer update may stall and the team will keep waiting on ownership.",
    "If you move too quickly, you may overcommit to a Monday target before final verification."
  ],
  options: [
    "Send a short acknowledgment now and buy time for final alignment.",
    "Assign yourself as reply owner and frame Monday as a working target pending verification.",
    "Ask one clarifying question before sending anything externally."
  ],
  recommendedMove:
    "Send a short alignment reply now, take ownership of the customer update, and frame Monday as provisional until verification is complete.",
  confidenceNotes:
    "High confidence on the need for a reply and an owner decision. Lower confidence on whether Monday is a safe commitment because the thread does not confirm final validation."
};

export const exampleTriageResult: TriageResult = {
  threadId: exampleEmailThread.id,
  bucket: "needs_action_now",
  confidence: 0.93,
  verdict: "Needs reply today",
  topReasons: [
    "The user is directly addressed in the latest messages.",
    "The thread includes a request to confirm and decide next steps.",
    "A same-day deadline is mentioned."
  ],
  summary: exampleThreadSummary,
  extractedAsks: exampleExtractedAsks,
  detectedDeadlines: ["today", "Monday"],
  suggestedNextMove:
    "Send a short alignment reply, confirm the Friday review, and frame Monday as the working target pending verification.",
  draftReplySet: exampleDraftReplySet,
  catchUpOverview: exampleCatchUpOverview,
  thoughtPartner: exampleThoughtPartnerResult
};

export const exampleUserSettings: UserSettings = {
  displayName: "You",
  emailAddress: "you@example.com",
  signature: "Thanks,\nYou",
  replyTone: "neutral",
  includeDraftReplies: true,
  showThoughtPartner: true,
  vipSenders: ["maya@example.com", "priya@example.com"],
  priorityDomains: ["example.com", "customer.example.com"],
  urgencyKeywords: ["today", "asap", "before 5pm", "blocker"],
  copiedOnlyKeywords: ["for visibility", "fyi", "no action needed"],
  draftVoicePreferences: ["concise", "executive", "direct but calm"],
  saveHistory: true,
  mockMode: true
};

export const exampleUnreadThreads: EmailThread[] = [
  exampleEmailThread,
  {
    id: "thread-fyi",
    subject: "Weekly launch status update",
    participants: ["Launch Ops", "Team", "You"],
    messageCount: 1,
    unreadCount: 1,
    lastMessageAt: "2026-04-08T09:00:00Z",
    messages: [
      {
        id: "msg-fyi-1",
        fromName: "Launch Ops",
        fromEmail: "launch-ops@example.com",
        toRecipients: ["team@example.com"],
        ccRecipients: ["you@example.com"],
        sentAt: "2026-04-08T09:00:00Z",
        bodyText: "FYI: weekly status update. No action needed, but sharing the latest milestone summary.",
        isUnread: true
      }
    ]
  },
  {
    id: "thread-at-risk",
    subject: "Quick decision on pricing page copy",
    participants: ["Priya Rao", "You"],
    messageCount: 1,
    unreadCount: 1,
    lastMessageAt: "2026-03-31T09:00:00Z",
    messages: [
      {
        id: "msg-risk-1",
        fromName: "Priya Rao",
        fromEmail: "priya@example.com",
        toRecipients: ["you@example.com"],
        ccRecipients: [],
        sentAt: "2026-03-31T09:00:00Z",
        bodyText: "Following up in case this got buried. Could you decide on the pricing page copy when you can?",
        isUnread: true
      }
    ]
  }
];
