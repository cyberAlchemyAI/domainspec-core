import {composeDefineContext} from "./context-adapter.mjs";
import {digest} from "./canonical.mjs";
import {runDefineSession} from "./session-runtime.mjs";

const YES = new Set(["y", "yes", "confirm", "confirmed", "looks right", "correct"]);

function normalized(value, fallback = null) {
  const text = String(value ?? "").trim();
  return text || fallback;
}

function renderScope(scope) {
  return [
    "\nHere is the scope I heard:",
    `  Domain: ${normalized(scope.domain, "not named")}`,
    `  Subject: ${normalized(scope.subject, "not named")}`,
    `  Project: ${normalized(scope.project, "not named")}`,
    `  Context: ${normalized(scope.context, "not named")}`,
    `  Desired outcome: ${normalized(scope.desired_outcome, "not named")}`,
    `  Intent: ${normalized(scope.intent, "not named")}`,
    `  Consumer: ${normalized(scope.consumer, "human:define-cli")}`,
  ].join("\n");
}

function renderOption(option, index, total) {
  return [
    `\nOption ${index + 1} of ${total}: ${option.term}`,
    `  Why it matters: ${option.why_it_matters}`,
    `  Candidate meaning: ${normalized(option.candidate_definition, "No meaning proposed yet")}`,
    `  Boundary: ${normalized(option.boundary, "Candidate only; no canonical or effect status")}`,
    "  Actions: [a]ccept  [d]iscuss  [e]dit  [o]pen/defer  [q]uit",
  ].join("\n");
}

function exactScope(scope, consumer) {
  const contextParts = [
    scope.domain && `Domain: ${scope.domain}`,
    scope.subject && `Subject: ${scope.subject}`,
    scope.project && `Project: ${scope.project}`,
    scope.context && `Context: ${scope.context}`,
  ].filter(Boolean);
  return {
    goal: normalized(scope.desired_outcome),
    intent: normalized(scope.intent),
    context: contextParts.join("\n"),
    consumer: normalized(scope.consumer, consumer),
  };
}

function missingScopeFields(scope) {
  return ["context", "desired_outcome", "intent"].filter((field) => !normalized(scope?.[field]));
}

function optionConcept(option) {
  const term = option.term.trim();
  return {
    concept_id: `concept:${digest(term).slice(0, 16)}`,
    term,
    question: option.question,
    owner_route: "Definitions Governance owner",
  };
}

export async function runDefineConversation(input) {
  const {agent, ask, write, repository_root: repositoryRoot} = input;
  const consumer = input.consumer ?? "human:define-cli";
  let userText = normalized(input.opening);
  if (!userText) userText = normalized(await ask("What are you working on? You can begin with a domain, subject, context, or project.\n> "));
  if (!userText) return {ok: false, stopped: true, reason_codes: ["define-conversation.opening-required"], authority_effect: "none"};

  let scope = null;
  let options = [];
  let turnCount = 0;
  write("\nDefine — conversational meaning discovery\nStart broadly. I will reflect what I hear, ask one useful question at a time, then let you review each candidate option.\n");
  while (!scope) {
    if (++turnCount > 24) return {ok: false, stopped: true, reason_codes: ["define-conversation.turn-limit"], authority_effect: "none"};
    write("\nDefine is considering that...\n");
    const turn = await agent.respond({mode: "discovery", user_input: userText, scope_confirmed: false});
    write(`\nDefine: ${turn.message}\n`);
    const missingScope = missingScopeFields(turn.scope);
    if (turn.scope_ready !== true || missingScope.length > 0) {
      if (turn.question) write(`\n${turn.question}\n`);
      else if (missingScope.length > 0) write(`\nBefore scope review, tell me more about: ${missingScope.join(", ")}.\n`);
      userText = normalized(await ask("\nYou: "));
      if (userText === "/quit") return {ok: false, stopped: true, reason_codes: ["define-conversation.user-stopped"], authority_effect: "none"};
      if (userText === "/review") userText = "Summarize the scope now and expose anything still missing.";
      continue;
    }
    write(`${renderScope(turn.scope)}\n`);
    const confirmation = normalized(await ask("\nIs this the scope you mean? [y]es, or tell me what to change\n> "));
    if (YES.has(confirmation.toLowerCase())) {
      scope = turn.scope;
      options = turn.options;
      break;
    }
    if (confirmation === "/quit") return {ok: false, stopped: true, reason_codes: ["define-conversation.user-stopped"], authority_effect: "none"};
    userText = `The proposed scope is not confirmed. Revise it using this correction: ${confirmation}`;
  }

  if (options.length === 0) {
    write("\nDefine is preparing the review options...\n");
    const prepared = await agent.respond({mode: "prepare-options", user_input: "The scope is confirmed. Prepare the bounded meaning options for review.", scope_confirmed: true, confirmed_scope: scope});
    write(`\nDefine: ${prepared.message}\n`);
    options = prepared.options;
  }
  if (options.length === 0) return {ok: false, stopped: true, reason_codes: ["define-conversation.no-options"], authority_effect: "none"};

  const concepts = [];
  const responses = [];
  for (let index = 0; index < options.length; index += 1) {
    let option = options[index];
    let resolved = false;
    while (!resolved) {
      write(`${renderOption(option, index, options.length)}\n`);
      const choice = normalized(await ask("> "), "o").toLowerCase();
      const concept = optionConcept(option);
      if (choice === "a" || choice === "accept") {
        if (!normalized(option.candidate_definition)) {
          write("\nThere is no candidate meaning to accept. Discuss, edit, or leave it open.\n");
          continue;
        }
        concepts.push(concept);
        responses.push({concept_id: concept.concept_id, action: "propose", payload: {definition: option.candidate_definition, plain_explanation: option.candidate_definition, boundary: normalized(option.boundary)}});
        resolved = true;
      } else if (choice === "e" || choice === "edit") {
        const revised = normalized(await ask("Your exact candidate meaning:\n> "));
        if (!revised) continue;
        concepts.push(concept);
        responses.push({concept_id: concept.concept_id, action: "propose", payload: {definition: revised, plain_explanation: revised, boundary: normalized(option.boundary)}});
        resolved = true;
      } else if (choice === "o" || choice === "open" || choice === "defer") {
        const reason = normalized(await ask("Why should this remain open? (optional)\n> "), "Deferred during one-by-one review");
        concepts.push(concept);
        responses.push({concept_id: concept.concept_id, action: "defer", payload: {reason}});
        resolved = true;
      } else if (choice === "d" || choice === "discuss") {
        const comment = normalized(await ask("What feels wrong or unclear?\n> "));
        write("\nDefine is reconsidering this option...\n");
        const discussed = await agent.respond({mode: "discuss-option", user_input: comment, scope_confirmed: true, confirmed_scope: scope, current_option: option});
        write(`\nDefine: ${discussed.message}\n`);
        if (discussed.options.length > 0) option = discussed.options[0];
      } else if (choice === "q" || choice === "quit") {
        return {ok: false, stopped: true, reason_codes: ["define-conversation.user-stopped-during-review"], authority_effect: "none"};
      } else {
        write("\nChoose accept, discuss, edit, open, or quit.\n");
      }
    }
  }

  const finish = normalized(await ask("\nCreate the candidate Definition Pack from these reviewed options? [y/n]\n> "), "n").toLowerCase();
  if (!YES.has(finish)) return {ok: false, stopped: true, reason_codes: ["define-conversation.pack-not-confirmed"], authority_effect: "none"};
  const sessionScope = exactScope(scope, consumer);
  if (!sessionScope.goal || !sessionScope.intent || !sessionScope.context) {
    return {ok: false, stopped: true, reason_codes: ["define-conversation.confirmed-scope-incomplete"], authority_effect: "none"};
  }
  const contextResult = composeDefineContext(sessionScope, repositoryRoot);
  if (!contextResult.ok) return contextResult;
  return runDefineSession({...sessionScope, concepts, responses, context_result: contextResult});
}
