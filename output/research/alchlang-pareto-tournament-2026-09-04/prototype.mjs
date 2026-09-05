import { readFile, writeFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = dirname(fileURLToPath(import.meta.url));
const fixture = JSON.parse(await readFile(join(root, "fixtures.json"), "utf8"));

const meaningfullyBetter = (a, b, objective) => objective.direction === "min"
  ? a < b - objective.epsilon
  : a > b + objective.epsilon;

const noWorse = (a, b, objective) => objective.direction === "min"
  ? a <= b + objective.epsilon
  : a >= b - objective.epsilon;

const dominates = (a, b) => {
  const comparisons = fixture.objectives.map((objective) => ({
    objective,
    a: a.values[objective.id],
    b: b.values[objective.id],
  }));
  return comparisons.every(({ a: av, b: bv, objective }) => noWorse(av, bv, objective))
    && comparisons.some(({ a: av, b: bv, objective }) => meaningfullyBetter(av, bv, objective));
};

const ineligible = fixture.candidates.filter((candidate) => !candidate.hard_gates_pass);
const notEvaluable = fixture.candidates.filter((candidate) => candidate.hard_gates_pass && !candidate.evidence_complete);
const eligible = fixture.candidates.filter((candidate) => candidate.hard_gates_pass && candidate.evidence_complete);

const remaining = new Map(eligible.map((candidate) => [candidate.id, candidate]));
const layers = [];
while (remaining.size) {
  const population = [...remaining.values()];
  const frontier = population.filter((candidate) => !population.some((other) => other.id !== candidate.id && dominates(other, candidate)));
  layers.push(frontier.map((candidate) => candidate.id).sort());
  for (const candidate of frontier) remaining.delete(candidate.id);
}

const frontier = layers[0];
const pairings = [];
for (let left = 0; left < frontier.length; left += 1) {
  for (let right = left + 1; right < frontier.length; right += 1) {
    pairings.push({ left: frontier[left], right: frontier[right], randomize_order: true, allow_tie: true });
  }
}

const result = {
  schema_version: "alchlang-pareto-prototype-result/v1",
  status: "fixture_pass",
  ineligible: ineligible.map((candidate) => candidate.id).sort(),
  not_evaluable: notEvaluable.map((candidate) => candidate.id).sort(),
  pareto_layers: layers,
  frontier,
  pairings,
  single_winner: frontier.length === 1,
  claim_ceiling: "Algorithm and fixture evidence only; no live variant, participant, usability, or product approval evidence."
};

const assertions = {
  ineligible: JSON.stringify(result.ineligible) === JSON.stringify([...fixture.expected.ineligible].sort()),
  not_evaluable: JSON.stringify(result.not_evaluable) === JSON.stringify([...fixture.expected.not_evaluable].sort()),
  frontier: JSON.stringify(result.frontier) === JSON.stringify([...fixture.expected.frontier].sort()),
  dominated: fixture.expected.dominated.every((id) => !result.frontier.includes(id)),
  single_winner: result.single_winner === fixture.expected.single_winner,
  frontier_round_robin: result.pairings.length === fixture.expected.pairing_count,
  broken_candidate_cannot_win: !result.frontier.includes("broken-fast"),
};
result.assertions = assertions;
result.status = Object.values(assertions).every(Boolean) ? "fixture_pass" : "fixture_fail";

await writeFile(join(root, "fixture-result.json"), `${JSON.stringify(result, null, 2)}\n`);
console.log(JSON.stringify(result, null, 2));
if (result.status !== "fixture_pass") process.exitCode = 1;
