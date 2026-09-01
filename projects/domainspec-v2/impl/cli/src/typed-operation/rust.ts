import { canonicalJson } from "../input/source-manifest.js";
import type { RuleExpression, TypedParameter, TypedResultConstructor, TypedType, ValueExpression } from "./contracts.js";
import type { TypedOperationClosureV1 } from "./closure.js";

const RUST_KEYWORDS = new Set([
  "Self", "abstract", "as", "async", "await", "become", "box", "break", "const", "continue", "crate", "do", "dyn", "else", "enum", "extern", "false", "final", "fn", "for", "gen", "if", "impl", "in", "let", "loop", "macro", "match", "mod", "move", "mut", "override", "priv", "pub", "raw", "ref", "return", "safe", "self", "static", "struct", "super", "trait", "true", "try", "type", "typeof", "union", "unsafe", "unsized", "use", "virtual", "where", "while", "yield",
]);

function rustStringLiteral(value: string): string {
  let result = "\"";
  for (let index = 0; index < value.length;) {
    const codePoint = value.codePointAt(index)!;
    index += codePoint > 0xffff ? 2 : 1;
    if (codePoint >= 0xd800 && codePoint <= 0xdfff) throw new Error("Rust string literal contains an unpaired surrogate");
    if (codePoint === 0x22) result += "\\\"";
    else if (codePoint === 0x5c) result += "\\\\";
    else if (codePoint === 0x00) result += "\\0";
    else if (codePoint === 0x09) result += "\\t";
    else if (codePoint === 0x0a) result += "\\n";
    else if (codePoint === 0x0d) result += "\\r";
    else if (codePoint < 0x20 || (codePoint >= 0x7f && codePoint <= 0x9f)) result += `\\u{${codePoint.toString(16)}}`;
    else result += String.fromCodePoint(codePoint);
  }
  return `${result}\"`;
}

export function renderTypedRustCrateManifest(projectId: string, featureId: string, nodeId: string, libraryPath: string): string {
  const crateName = `${projectId}-${featureId}-${nodeId}`.replace(/[^a-z0-9-]+/g, "-").replace(/-+/g, "-").replace(/^-|-$/g, "");
  if (!crateName || libraryPath.includes("\\") || libraryPath.startsWith("/") || libraryPath.split("/").some((segment) => segment === "" || segment === "." || segment === "..")) {
    throw new Error("typed Rust crate identity or library path is invalid");
  }
  return `[package]\nname = ${rustStringLiteral(crateName)}\nversion = "0.0.0"\nedition = "2024"\npublish = false\n\n[lib]\npath = ${rustStringLiteral(libraryPath)}\n`;
}

function words(value: string): string[] {
  return value.split(/[^A-Za-z0-9]+/).filter(Boolean);
}

function pascal(value: string): string {
  const result = words(value).map((word) => `${word[0]?.toUpperCase() ?? ""}${word.slice(1)}`).join("") || "DomainNode";
  const candidate = /^[A-Za-z_]/.test(result) ? result : `Domain${result}`;
  return RUST_KEYWORDS.has(candidate) ? `Domain${candidate}` : candidate;
}

function snake(value: string): string {
  const result = words(value).map((word) => word.toLowerCase()).join("_") || "domain_node";
  const candidate = /^[A-Za-z_]/.test(result) ? result : `domain_${result}`;
  return RUST_KEYWORDS.has(candidate) ? `domain_${candidate}` : candidate;
}

function variantName(value: string): string {
  return RUST_KEYWORDS.has(value) ? `Domain${value}` : value;
}

function nodeName(selector: string): string {
  return pascal(selector.split(":")[1] ?? selector);
}

function rustType(type: TypedType): string {
  if (type.kind === "scalar") return type.name === "String" ? "String" : type.name === "Bool" ? "bool" : "u64";
  if (type.kind === "named") return nodeName(type.selector);
  if (type.kind === "set") return `BTreeSet<${rustType(type.element)}>`;
  if (type.kind === "list") return `Vec<${rustType(type.element)}>`;
  if (type.kind === "optional") return `Option<${rustType(type.element)}>`;
  throw new Error("anonymous sum types are unsupported in Rust properties; select a named sum node");
}

function sameType(left: TypedType, right: TypedType): boolean {
  return canonicalJson(left) === canonicalJson(right);
}

function isCopyType(type: TypedType): boolean {
  return type.kind === "scalar" && type.name !== "String";
}

function claimSymbol(registry: Map<string, string>, symbol: string, owner: string, label: string): void {
  const previous = registry.get(symbol);
  if (previous !== undefined && previous !== owner) throw new Error(`${label} values collide after Rust identifier normalization:${previous}:${owner}:${symbol}`);
  registry.set(symbol, owner);
}

function validateParameterSymbols(parameters: readonly TypedParameter[], owner: string): void {
  const symbols = new Map<string, string>();
  for (const parameter of parameters) claimSymbol(symbols, snake(parameter.name), parameter.name, `Rust parameter in ${owner}`);
}

type ValueOwnership = "borrowed" | "place" | "copy" | "owned" | "string-literal";

interface RenderedValue {
  readonly code: string;
  readonly type: TypedType;
  readonly ownership: ValueOwnership;
}

interface RustBooleanBlock {
  readonly statements: readonly string[];
  readonly result: string;
}

class RustNameAllocator {
  private nextId = 0;

  next(): string {
    const name = `__domainspec_rule_${String(this.nextId).padStart(3, "0")}`;
    this.nextId += 1;
    return name;
  }
}

function indentText(value: string, spaces: number): string {
  const indentation = " ".repeat(spaces);
  return value.split("\n").map((line) => `${indentation}${line}`).join("\n");
}

function blockBody(block: RustBooleanBlock): string {
  return [...block.statements, block.result].join("\n");
}

function blockExpression(block: RustBooleanBlock): string {
  if (block.statements.length === 0) return block.result;
  return `{\n${indentText(blockBody(block), 4)}\n}`;
}

function lazyBlockExpression(block: RustBooleanBlock): string {
  return `{\n${indentText(blockBody(block), 4)}\n}`;
}

function closureExpression(binding: string, block: RustBooleanBlock): string {
  return `|${binding}| {\n${indentText(blockBody(block), 8)}\n    }`;
}

function borrowValue(value: RenderedValue): string {
  return value.ownership === "borrowed" || value.ownership === "string-literal" ? value.code : `&${value.code}`;
}

export function renderTypedRustOperation(closure: TypedOperationClosureV1): string {
  const nodeContracts = new Map(closure.nodes.map((node) => [node.selector, node.typed_contract]));
  const properties = new Map<string, { readonly owner: string; readonly name: string; readonly type: TypedType }>();
  const variants = new Map<string, { readonly owner: string; readonly name: string; readonly payload: TypedType | null }>();
  const rules = new Map<string, Extract<(typeof closure.nodes)[number]["typed_contract"], { readonly schema_version: "domainspec.typed-rule/v1" }>>();
  const typeSymbols = new Map<string, string>();
  const callableSymbols = new Map<string, string>();

  for (const node of closure.nodes) {
    const contract = node.typed_contract;
    if (contract.schema_version === "domainspec.typed-record/v1" || contract.schema_version === "domainspec.typed-sum/v1") {
      claimSymbol(typeSymbols, nodeName(node.selector), node.selector, "Rust type");
    }
    if (contract.schema_version === "domainspec.typed-record/v1") {
      const fieldSymbols = new Map<string, string>();
      for (const property of contract.properties) {
        claimSymbol(fieldSymbols, snake(property.name), property.ontology_property, `Rust field in ${node.selector}`);
        properties.set(property.ontology_property, { owner: node.selector, name: property.name, type: property.type });
      }
    } else if (contract.schema_version === "domainspec.typed-sum/v1") {
      const memberSymbols = new Map<string, string>();
      for (const variant of contract.variants) {
        claimSymbol(memberSymbols, variantName(variant.name), variant.ontology_variant, `Rust variant in ${node.selector}`);
        variants.set(variant.ontology_variant, { owner: node.selector, name: variant.name, payload: variant.payload });
      }
    } else if (contract.schema_version === "domainspec.typed-rule/v1") {
      validateParameterSymbols(contract.parameters, node.selector);
      claimSymbol(callableSymbols, snake(node.selector.split(":")[1] ?? "rule"), node.selector, "Rust callable");
      rules.set(node.selector, contract);
    }
  }

  const guardNode = closure.nodes.find((node) => node.selector === closure.operation.guard);
  if (guardNode?.typed_contract.schema_version !== "domainspec.typed-rule/v1") throw new Error("typed Operation guard is not a typed Rule in the closure");
  const guardFunction = snake(guardNode.selector.split(":")[1] ?? "guard");
  const operationFunction = snake(closure.root_selector.split(":")[1] ?? "operation");
  claimSymbol(callableSymbols, operationFunction, closure.root_selector, "Rust callable");
  validateParameterSymbols(closure.operation.inputs, closure.root_selector);

  const renderValue = (value: ValueExpression, scopes: ReadonlyMap<string, TypedType>): RenderedValue => {
    if (value.op === "literal") {
      if (value.type === "String") return { code: rustStringLiteral(String(value.value)), type: { kind: "scalar", name: "String" }, ownership: "string-literal" };
      return { code: String(value.value), type: { kind: "scalar", name: value.type }, ownership: "copy" };
    }
    if (value.op === "variant") {
      const variant = variants.get(value.selector);
      if (!variant) throw new Error(`Rust Rule references unknown ontology variant:${value.selector}`);
      if (variant.payload !== null) throw new Error(`Rust Rule cannot construct payload variant as a value:${value.selector}`);
      return { code: `${nodeName(variant.owner)}::${variantName(variant.name)}`, type: { kind: "named", selector: variant.owner }, ownership: "owned" };
    }
    if (value.op === "to_set") {
      const source = renderValue(value.value, scopes);
      if (source.type.kind !== "list") throw new Error("Rust to_set requires a list value");
      const iterator = source.ownership === "owned" ? `${source.code}\n    .into_iter()` : `${source.code}\n    .iter()\n    .cloned()`;
      return { code: `${iterator}\n    .collect::<BTreeSet<_>>()`, type: { kind: "set", element: source.type.element }, ownership: "owned" };
    }
    let currentType = scopes.get(value.root);
    if (!currentType) throw new Error(`Rust Rule references unknown root:${value.root}`);
    let code = snake(value.root);
    for (let index = 0; index < value.properties.length; index += 1) {
      const propertySelector = value.properties[index]!;
      const property = properties.get(propertySelector);
      if (!property) throw new Error(`Rust Rule references unknown property:${propertySelector}`);
      if (currentType.kind === "set" || currentType.kind === "list") {
        if (currentType.element.kind !== "named" || currentType.element.selector !== property.owner) throw new Error(`Rust Rule projection owner mismatch:${propertySelector}`);
        if (index !== value.properties.length - 1) throw new Error(`Rust Rule supports one terminal collection projection:${propertySelector}`);
        const member = `projected.${snake(property.name)}`;
        const projected = isCopyType(property.type) ? member : `${member}.clone()`;
        const collection = currentType.kind === "set" ? "BTreeSet" : "Vec";
        return {
          code: `${code}\n    .iter()\n    .map(|projected| ${projected})\n    .collect::<${collection}<_>>()`,
          type: { kind: currentType.kind, element: property.type },
          ownership: "owned",
        };
      }
      if (currentType.kind !== "named" || currentType.selector !== property.owner) throw new Error(`Rust Rule property owner mismatch:${propertySelector}`);
      code = `${code}.${snake(property.name)}`;
      currentType = property.type;
    }
    return { code, type: currentType, ownership: value.properties.length === 0 ? "borrowed" : isCopyType(currentType) ? "copy" : "place" };
  };

  let names = new RustNameAllocator();
  const renderRule = (expression: RuleExpression, scopes: ReadonlyMap<string, TypedType>): RustBooleanBlock => {
    if (expression.op === "all" || expression.op === "any") {
      if (expression.terms.length === 1) return renderRule(expression.terms[0]!, scopes);
      const statements: string[] = [];
      let previous: string | null = null;
      for (const term of expression.terms) {
        const resultName = names.next();
        const termBlock = renderRule(term, scopes);
        const right = previous === null ? blockExpression(termBlock) : lazyBlockExpression(termBlock);
        statements.push(`let ${resultName} = ${previous === null ? right : `${previous} ${expression.op === "all" ? "&&" : "||"} ${right}`};`);
        previous = resultName;
      }
      return { statements, result: previous! };
    }
    if (expression.op === "not") {
      const term = renderRule(expression.term, scopes);
      return { statements: [], result: `!(${blockExpression(term)})` };
    }
    if (expression.op === "eq" || expression.op === "lt" || expression.op === "set_equal" || expression.op === "contains") {
      const left = renderValue(expression.left, scopes);
      const right = renderValue(expression.right, scopes);
      if (expression.op === "contains") {
        if (left.type.kind !== "set" || !sameType(left.type.element, right.type)) throw new Error("Rust contains operands are type-incompatible");
        return { statements: [], result: `${left.code}.contains(${borrowValue(right)})` };
      }
      if (!sameType(left.type, right.type)) throw new Error(`Rust ${expression.op} operands are type-incompatible`);
      return { statements: [], result: `${left.code} ${expression.op === "lt" ? "<" : "=="} ${right.code}` };
    }
    if (expression.op === "rule_ref") {
      const target = rules.get(expression.selector);
      if (!target) throw new Error(`Rust Rule references an unavailable typed Rule:${expression.selector}`);
      const supplied = new Map(expression.arguments.map((argument) => [argument.parameter, argument.value]));
      if (supplied.size !== target.parameters.length || target.parameters.some((parameter) => !supplied.has(parameter.name))) {
        throw new Error(`Rust Rule reference arguments do not exactly bind target parameters:${expression.selector}`);
      }
      const arguments_ = target.parameters.map((parameter) => {
        const rendered = renderValue(supplied.get(parameter.name)!, scopes);
        if (!sameType(rendered.type, parameter.type)) throw new Error(`Rust Rule reference argument is type-incompatible:${expression.selector}:${parameter.name}`);
        return borrowValue(rendered);
      });
      return { statements: [], result: `${snake(expression.selector.split(":")[1] ?? "rule")}(${arguments_.join(", ")})` };
    }
    if (expression.op !== "exactly_one" && expression.op !== "unique" && expression.op !== "exists") {
      throw new Error(`unsupported Rust Rule operator:${(expression as { readonly op: string }).op}`);
    }
    const collection = renderValue(expression.collection, scopes);
    if (collection.type.kind !== "set" && collection.type.kind !== "list") throw new Error(`Rust ${expression.op} requires a collection`);
    const nestedScopes = new Map(scopes);
    nestedScopes.set(expression.binding, collection.type.element);
    const binding = snake(expression.binding);
    if (expression.op === "unique") {
      if (expression.where.op !== "eq" || canonicalJson(expression.where.left) !== canonicalJson(expression.where.right) || expression.where.left.op !== "path") {
        throw new Error("Rust unique requires an identical path equality naming the uniqueness key");
      }
      const key = renderValue(expression.where.left, nestedScopes);
      const keyCode = key.ownership === "copy" ? key.code : borrowValue(key);
      return { statements: [], result: `${collection.code}\n    .iter()\n    .map(|${binding}| ${keyCode})\n    .collect::<BTreeSet<_>>()\n    .len() == ${collection.code}.len()` };
    }
    const predicate = renderRule(expression.where, nestedScopes);
    const closure = closureExpression(binding, predicate);
    if (expression.op === "exactly_one") return { statements: [], result: `${collection.code}\n    .iter()\n    .filter(${closure})\n    .count() == 1` };
    return { statements: [], result: `${collection.code}\n    .iter()\n    .any(${closure})` };
  };

  const dataDefinitions = closure.nodes.flatMap((node): string[] => {
    const contract = node.typed_contract;
    const name = nodeName(node.selector);
    if (contract.schema_version === "domainspec.typed-record/v1") {
      const fields = contract.properties.map((property) => `    pub ${snake(property.name)}: ${rustType(property.type)},`).join("\n");
      return [`#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord, Hash)]\npub struct ${name} {\n${fields}\n}`];
    }
    if (contract.schema_version === "domainspec.typed-sum/v1") {
      const members = contract.variants.map((variant) => `    ${variantName(variant.name)}${variant.payload === null ? "" : `(${rustType(variant.payload)})`},`).join("\n");
      return [`#[derive(Clone, Debug, PartialEq, Eq, PartialOrd, Ord, Hash)]\npub enum ${name} {\n${members}\n}`];
    }
    return [];
  });

  const ruleFunctions = closure.nodes.flatMap((node): string[] => {
    const contract = node.typed_contract;
    if (contract.schema_version !== "domainspec.typed-rule/v1") return [];
    names = new RustNameAllocator();
    const scopes = new Map(contract.parameters.map((parameter) => [parameter.name, parameter.type]));
    const parameters = contract.parameters.map((parameter) => `${snake(parameter.name)}: &${rustType(parameter.type)}`).join(", ");
    const block = renderRule(contract.expression, scopes);
    return [`#[rustfmt::skip]\npub fn ${snake(node.selector.split(":")[1] ?? "rule")}(${parameters}) -> bool {\n${indentText(blockBody(block), 4)}\n}`];
  });
  const outputType = rustType(closure.operation.output);
  const inputParameters = closure.operation.inputs.map((parameter) => `${snake(parameter.name)}: &${rustType(parameter.type)}`).join(", ");
  const inputArguments = closure.operation.inputs.map((parameter) => snake(parameter.name)).join(", ");

  const result = (constructor: TypedResultConstructor): string => {
    const outputSelector = closure.operation.output.kind === "named" ? closure.operation.output.selector : null;
    if (outputSelector === null) throw new Error("typed Rust Operation output must be a named sum");
    const outputContract = nodeContracts.get(outputSelector);
    if (outputContract?.schema_version !== "domainspec.typed-sum/v1") throw new Error("typed Rust Operation output must select a typed sum");
    const variant = outputContract.variants.find((candidate) => candidate.name === constructor.variant);
    if (!variant) throw new Error(`typed Rust result variant is missing:${constructor.variant}`);
    if (variant.payload === null) {
      if (constructor.payload_variant !== null) throw new Error("payload constructor supplied for payloadless result");
      return `${outputType}::${variantName(variant.name)}`;
    }
    if (variant.payload.kind !== "named" || constructor.payload_variant === null) throw new Error("typed Rust payload result requires one named payload variant");
    const payloadContract = nodeContracts.get(variant.payload.selector);
    if (payloadContract?.schema_version !== "domainspec.typed-sum/v1" || !payloadContract.variants.some((candidate) => candidate.name === constructor.payload_variant)) {
      throw new Error(`typed Rust payload variant is missing:${constructor.payload_variant}`);
    }
    return `${outputType}::${variantName(variant.name)}(${rustType(variant.payload)}::${variantName(constructor.payload_variant)})`;
  };

  const propertyBindings = closure.properties.map((row) => `    (${rustStringLiteral(row.ontology_property)}, ${rustStringLiteral(`${nodeName(row.domainspec_selector.split("#")[0]!)}::${snake(row.domainspec_selector.split("#")[1]!)}`)}),`).join("\n");
  const variantBindings = closure.variants.map((row) => `    (${rustStringLiteral(row.ontology_variant)}, ${rustStringLiteral(`${nodeName(row.domainspec_selector.split("#")[0]!)}::${variantName(row.domainspec_selector.split("#")[1]!)}`)}),`).join("\n");
  const ruleSelectors = closure.rules.map((row) => `    (${rustStringLiteral(row.ontology_rule)}, ${rustStringLiteral(row.domainspec_selector)}),`).join("\n");
  const ruleImplementationBindings = closure.rules.map((row) => `    (${rustStringLiteral(row.ontology_rule)}, ${rustStringLiteral(row.domainspec_selector)}, ${rustStringLiteral(snake(row.domainspec_selector.split(":")[1] ?? "rule"))}),`).join("\n");

  return `// domainspec-typed-closure-sha256: ${rustStringLiteral(closure.closure_sha256)}
use std::collections::BTreeSet;

pub const DOMAINSPEC_TYPED_CLOSURE_SHA256: &str =
    ${rustStringLiteral(closure.closure_sha256)};
#[rustfmt::skip]
pub const DOMAINSPEC_PROPERTY_BINDINGS: &[(&str, &str)] = &[
${propertyBindings}
];
#[rustfmt::skip]
pub const DOMAINSPEC_VARIANT_BINDINGS: &[(&str, &str)] = &[
${variantBindings}
];
#[rustfmt::skip]
pub const DOMAINSPEC_RULE_SELECTORS: &[(&str, &str)] = &[
${ruleSelectors}
];
#[rustfmt::skip]
pub const DOMAINSPEC_RULE_IMPLEMENTATION_BINDINGS: &[(&str, &str, &str)] = &[
${ruleImplementationBindings}
];

${dataDefinitions.join("\n\n")}

${ruleFunctions.join("\n\n")}

pub fn ${operationFunction}(${inputParameters}) -> ${outputType} {
    if ${guardFunction}(${inputArguments}) {
        ${result(closure.operation.success_result)}
    } else {
        ${result(closure.operation.failure_result)}
    }
}
`;
}
