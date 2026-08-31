# Route 1 language audition — concrete work shapes

Transport: `interactive_guided_class` (candidate / unproven)

Intent state: volatile

Human gate: pending

## Moment 1 — Opening

**A release day with two different risks**

### What must stay independent?

It is 3:20 p.m. Priya is preparing Lantern's booking app for a 4 p.m. release when two work cards arrive.

Nora, a customer using her phone, cannot tap **Reserve** because the button disappears under a consent banner. At the same time, Lantern's new **Delete my account** flow is waiting for a release decision.

Someone suggests, “Start a team of agents for both. More people will be faster.” But speed is not Priya's first problem. One card needs a cause she can inspect. The other needs two judgments that must not collapse into one.

Read both cards. What safeguard does each problem actually need?

## Moment 2 — Tension

### Work card A — Nora cannot finish her booking

Priya needs someone to reproduce Nora's problem on a small screen, identify the exact component or style rule hiding the button, and return a screenshot plus the file and line. Nobody has permission to change the code. Priya will inspect the report before deciding what happens next.

**Which setup is enough for this request?**

- One investigator returns one evidence report for Priya to inspect before deciding.
- Two reviewers return separate evidence reports for Priya to compare before deciding.

### Work card B — account deletion must be safe and honest

Before release, one review must check whether Lantern actually removes the stored data it promises to remove. Another must check whether a keyboard or screen-reader user can complete or cancel the flow without being trapped. Priya needs both reports separately before the go/no-go decision; one report cannot stand in for the other.

**Which setup preserves what this request needs?**

- One investigator returns one evidence report for Priya to inspect before deciding.
- Two reviewers return separate evidence reports for Priya to compare before deciding.

**Check both decisions**

## Moment 3 — Reveal

### What each answer protects

For Nora's booking problem:

- If you chose one investigator: **Yes.** This job traces one visible symptom to one inspectable cause. Priya needs one clear evidence report, not a second judgment protecting a different decision.
- If you chose two reviewers: Look at what Priya must decide. She needs the cause of one defect and evidence she can inspect. A second report would add a person, but it would not preserve another required judgment.

For the account-deletion decision:

- If you chose two reviewers: **Yes.** The data promise and the accessible escape path protect different parts of the release decision. Keeping the reports separate lets Priya see whether both obligations were actually examined.
- If you chose one investigator: One person doing both reviews would turn two required judgments into one person's combined judgment. Priya could no longer tell whether each safeguard had its own examination.

Think of a **repair bench** and a **two-key cabinet**. At the repair bench, one technician can trace one fault and show the owner the failed part. The cabinet uses two keys because one person's action must not replace the other's. The comparison ends there: reviewers do not literally turn keys, not every multi-person job needs independent approval, and two people without named roles, checks, and stop points are simply two people.

Now name the distinction:

1. A decision, permission, or responsibility that must stay separate is a **boundary**.
2. One person with one clearly limited job whose result the parent can inspect is a **bounded helper**.
3. A coordinated job with separate roles, checks, and stop points is a **governed dispatch**.
4. Permission to make a change or claim is **authority**.

Nora's defect report fits one bounded helper: it asks for one limited, inspectable result. The deletion decision fits a governed dispatch: its privacy and accessibility judgments must remain distinct and later meet in Priya's decision. Neither choice gives anyone permission to edit, approve the release, register a route, or start work. More agents do not create more authority.

### Try the distinction somewhere else

A community hall has a flickering exit sign. One electrician is asked to identify the failed part, photograph it, and report to the organizer before any repair is approved. At the same fundraiser, the cashier and a second counter must record the donation total separately before the treasurer accepts it.

Which problem needs one bounded helper? Which needs a governed dispatch? What safeguard would disappear if the two cash counts became one person's judgment?

### Carry one question forward

Priya kept the privacy and accessibility reviews separate. Before the release decision may rely on their results, what must be true of both results?

Hold that question for Lesson 3. It asks when separate reports become usable evidence, not which work shape produced them.

`arcanum/arcana/subagent-strategy/SKILL.md` describes when a multi-agent route is justified, when material confirmation is needed, and which lifecycle separations stay visible. Reading it does not authorize, register, or execute a route. This activity records a local answer; it does not prove comprehension or operational readiness.

Return to 3:20 p.m. When someone says “start more agents,” the useful first question is no longer “how many?” It is: **what necessary safeguard would disappear if these roles were combined?**
