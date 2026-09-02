export const LEAF_NODES = ["fact_ref", "literal", "entity_ref", "actor_ref", "state_ref"];
export const UNARY_OPERATORS = ["not", "exists", "absent"];
export const BINARY_OPERATORS = ["eq", "neq", "lt", "lte", "gt", "gte", "in", "contains", "and", "or"];
export class CompilationRejected extends Error {
    issues;
    constructor(issues) {
        super(issues.map((issue) => `${issue.code} at ${issue.path}: ${issue.message}`).join("\n"));
        this.issues = issues;
        this.name = "CompilationRejected";
    }
}
