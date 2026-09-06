import type { Expr, FunctionModel } from './function-runtime.js';
export declare function parseFunctionExpression(source: string): Expr;
export declare function parseFunctionSource(source: string, allowModules?: boolean): {
    model: FunctionModel;
    coreSource: string;
    bindings: any;
};
