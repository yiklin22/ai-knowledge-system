# Customer discovery: using the project as a gateway to your own business

The goal of an FDE or AI-engineer job is paid access to customers. This doc turns the project into a way to learn what customers will pay for. Fill in the blanks with real findings; do not invent them.

## 1. Hypothesis (to be tested, not assumed)

> Small teams that must *defend* what they know (consultancies, compliance, research, legal-adjacent, support/ops) will pay for AI that cites verbatim evidence and keeps a human approving, because an unauditable chatbot is not allowed on their real work.

Narrow it to one buyer before building anything: ______ (role) at ______ (type of company) who currently ______ (manual process) costing ______ hours/week.

## 2. Where to find the first 10 conversations

- People you already know in business/ops roles (your `business` domain notes show interest).
- Small consultancies and agencies; your Python/automation work (Excel reconciliation, report generation) is an easier first door than "AI knowledge system".
- LinkedIn/Reddit/Slack communities of the target role. Ask for 20 minutes, not a sale.

## 3. Interview script (ask about the past, not your idea)

1. Walk me through the last time you had to find or verify a fact from documents. What did you do?
2. How long did it take? What happened when it was wrong?
3. What tools do you use now? What do you dislike about them?
4. Who else must trust the answer (boss, client, auditor)?
5. Have you paid for anything to fix this? How much? If not, why not?
6. Who signs off on new tools and data access? What would block it (security, privacy)?

Do not pitch in the first 15 minutes. Record the exact words people use; that becomes your landing page copy.

## 4. What counts as a signal

| Weak | Strong |
|---|---|
| "That sounds cool" | They describe a recent painful instance unprompted |
| "Send me a link" | They offer real documents for a pilot |
| Compliments | They ask about price, or who else must approve |
| | They already pay for a worse workaround |

Target: 10 conversations → 3 who offer data → 1 paid or committed pilot.

## 5. Pilot offer (small, fixed, paid)

- 2 weeks, one workflow, 50-200 of *their* documents, run on their machine or private cloud.
- Deliverables: working Ask + cited answers, an eval on 20 of *their* questions (same method as `docs/eval-results.md`), a security note, a handover session.
- Success metric agreed up front (e.g. hit@5 ≥ 90% on their questions; time-to-find cut by half).
- Price it, even if small. Free pilots teach you less.

## 6. What the job teaches you (log it weekly)

| Question | Answer from real customers |
|---|---|
| What do they actually pay for? | |
| What failed in deployment (data quality, access, trust)? | |
| Which integrations came up repeatedly? | |
| What did procurement/security ask for? | |
| What would I productise vs. keep as services? | |

Repeated answers become the product. One-off asks stay services.

## 7. Business path

1. **Services first:** automation + AI tooling for small teams (matches your profile positioning). Cash and customer access.
2. **Productise the repeated part:** the cited-answers pipeline with a hosted, multi-tenant, authenticated version (the gap listed in `docs/security.md`).
3. **Only then** raise prices, hire, or seek funding.

## 8. Before the first customer demo

- [ ] Commit the uncommitted work (one commit per approved batch).
- [ ] `./demo.sh` runs cleanly on a fresh machine.
- [ ] A 3-minute screen recording: add source → proposal → review → cited answer → show a rejected forged quote.
- [ ] Replace private-vault examples with the sample vault; never demo someone else's confidential data.
