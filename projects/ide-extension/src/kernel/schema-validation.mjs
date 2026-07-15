import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import Ajv2020 from 'ajv/dist/2020.js';

const PROJECT_ROOT = path.resolve(fileURLToPath(new URL('../..', import.meta.url)));
const DEFAULT_SCHEMA_DIR = path.join(PROJECT_ROOT, 'schemas');

export const SCHEMA_FILES = Object.freeze({
  'agent-envelope': 'agent-envelope.schema.json',
  'approval-record': 'approval-record.schema.json',
  'approve-request': 'approve-request.schema.json',
  'bridge-claim-request': 'bridge-claim-request.schema.json',
  'bridge-interrupt-request': 'bridge-interrupt-request.schema.json',
  'bridge-release-request': 'bridge-release-request.schema.json',
  'bridge-result-request': 'bridge-result-request.schema.json',
  'bridge-target-request': 'bridge-target-request.schema.json',
  'canvas-interaction-request': 'canvas-interaction-request.schema.json',
  'canvas-navigation-ack-request': 'canvas-navigation-ack-request.schema.json',
  'canvas-navigation-request': 'canvas-navigation-request.schema.json',
  'canvas-pruning-commit-request': 'canvas-pruning-commit-request.schema.json',
  'canvas-pruning-preview-request': 'canvas-pruning-preview-request.schema.json',
  'canvas-publish-request': 'canvas-publish-request.schema.json',
  'content-operation-request': 'content-operation-request.schema.json',
  'module-manifest': 'module-manifest.schema.json',
  'operations-interaction-request': 'operations-interaction-request.schema.json',
  'operations-surface-derive-request': 'operations-surface-derive-request.schema.json',
  'prepare-request': 'prepare-request.schema.json',
  receipt: 'receipt.schema.json',
  'reject-request': 'reject-request.schema.json'
});

function stableErrors(errors = []) {
  return errors.map((error) => ({
    instance_path: error.instancePath,
    schema_path: error.schemaPath,
    keyword: error.keyword,
    message: error.message || '',
    params: error.params
  }));
}

function unknownSchema(schemaName) {
  const error = new Error(`unknown schema: ${schemaName}`);
  error.code = 'unknown_schema';
  error.schema_name = schemaName;
  error.available_schemas = Object.keys(SCHEMA_FILES);
  return error;
}

export async function createSchemaValidators(options = {}) {
  const schemaDir = options.schemaDir || DEFAULT_SCHEMA_DIR;
  const ajv = new Ajv2020({ allErrors: true, strict: true });
  const validators = {};

  for (const [schemaName, file] of Object.entries(SCHEMA_FILES)) {
    const schemaPath = path.join(schemaDir, file);
    const schema = JSON.parse(await readFile(schemaPath, 'utf8'));
    validators[schemaName] = ajv.compile(schema);
  }

  function validate(schemaName, value) {
    const validator = validators[schemaName];
    if (!validator) throw unknownSchema(schemaName);

    const valid = validator(value);
    return {
      valid,
      errors: valid ? [] : stableErrors(validator.errors)
    };
  }

  function assert(schemaName, value, source = '<memory>') {
    const result = validate(schemaName, value);
    if (result.valid) return value;

    const error = new Error(`${source}: ${schemaName} schema validation failed`);
    error.code = 'schema_validation_failed';
    error.schema_name = schemaName;
    error.source = source;
    error.validation_errors = result.errors;
    throw error;
  }

  return Object.freeze({
    schema_names: Object.freeze(Object.keys(SCHEMA_FILES)),
    validate,
    assert
  });
}

let defaultValidatorsPromise;

export function getSchemaValidators() {
  defaultValidatorsPromise ||= createSchemaValidators();
  return defaultValidatorsPromise;
}

export async function validateSchema(schemaName, value) {
  return (await getSchemaValidators()).validate(schemaName, value);
}

export async function assertSchema(schemaName, value, source) {
  return (await getSchemaValidators()).assert(schemaName, value, source);
}

export function validateAgentEnvelope(value) {
  return validateSchema('agent-envelope', value);
}

export function validateModuleManifest(value) {
  return validateSchema('module-manifest', value);
}

export function validateApprovalRecord(value) {
  return validateSchema('approval-record', value);
}

export function validateApproveRequest(value) {
  return validateSchema('approve-request', value);
}

export function validatePrepareRequest(value) {
  return validateSchema('prepare-request', value);
}

export function validateBridgeClaimRequest(value) {
  return validateSchema('bridge-claim-request', value);
}

export function validateBridgeInterruptRequest(value) {
  return validateSchema('bridge-interrupt-request', value);
}

export function validateBridgeReleaseRequest(value) {
  return validateSchema('bridge-release-request', value);
}

export function validateBridgeResultRequest(value) {
  return validateSchema('bridge-result-request', value);
}

export function validateBridgeTargetRequest(value) {
  return validateSchema('bridge-target-request', value);
}

export function validateCanvasInteractionRequest(value) {
  return validateSchema('canvas-interaction-request', value);
}

export function validateCanvasNavigationAckRequest(value) {
  return validateSchema('canvas-navigation-ack-request', value);
}

export function validateCanvasNavigationRequest(value) {
  return validateSchema('canvas-navigation-request', value);
}

export function validateCanvasPruningCommitRequest(value) {
  return validateSchema('canvas-pruning-commit-request', value);
}

export function validateCanvasPruningPreviewRequest(value) {
  return validateSchema('canvas-pruning-preview-request', value);
}

export function validateCanvasPublishRequest(value) {
  return validateSchema('canvas-publish-request', value);
}

export function validateContentOperationRequest(value) {
  return validateSchema('content-operation-request', value);
}

export function validateOperationsSurfaceDeriveRequest(value) {
  return validateSchema('operations-surface-derive-request', value);
}

export function validateOperationsInteractionRequest(value) {
  return validateSchema('operations-interaction-request', value);
}

export function validateRejectRequest(value) {
  return validateSchema('reject-request', value);
}

export function validateReceipt(value) {
  return validateSchema('receipt', value);
}

export function assertAgentEnvelope(value, source) {
  return assertSchema('agent-envelope', value, source);
}

export function assertModuleManifest(value, source) {
  return assertSchema('module-manifest', value, source);
}

export function assertApprovalRecord(value, source) {
  return assertSchema('approval-record', value, source);
}

export function assertApproveRequest(value, source) {
  return assertSchema('approve-request', value, source);
}

export function assertPrepareRequest(value, source) {
  return assertSchema('prepare-request', value, source);
}

export function assertBridgeClaimRequest(value, source) {
  return assertSchema('bridge-claim-request', value, source);
}

export function assertBridgeInterruptRequest(value, source) {
  return assertSchema('bridge-interrupt-request', value, source);
}

export function assertBridgeReleaseRequest(value, source) {
  return assertSchema('bridge-release-request', value, source);
}

export function assertBridgeResultRequest(value, source) {
  return assertSchema('bridge-result-request', value, source);
}

export function assertBridgeTargetRequest(value, source) {
  return assertSchema('bridge-target-request', value, source);
}

export function assertCanvasInteractionRequest(value, source) {
  return assertSchema('canvas-interaction-request', value, source);
}

export function assertCanvasNavigationAckRequest(value, source) {
  return assertSchema('canvas-navigation-ack-request', value, source);
}

export function assertCanvasNavigationRequest(value, source) {
  return assertSchema('canvas-navigation-request', value, source);
}

export function assertCanvasPruningCommitRequest(value, source) {
  return assertSchema('canvas-pruning-commit-request', value, source);
}

export function assertCanvasPruningPreviewRequest(value, source) {
  return assertSchema('canvas-pruning-preview-request', value, source);
}

export function assertCanvasPublishRequest(value, source) {
  return assertSchema('canvas-publish-request', value, source);
}

export function assertContentOperationRequest(value, source) {
  return assertSchema('content-operation-request', value, source);
}

export function assertOperationsSurfaceDeriveRequest(value, source) {
  return assertSchema('operations-surface-derive-request', value, source);
}

export function assertOperationsInteractionRequest(value, source) {
  return assertSchema('operations-interaction-request', value, source);
}

export function assertRejectRequest(value, source) {
  return assertSchema('reject-request', value, source);
}

export function assertReceipt(value, source) {
  return assertSchema('receipt', value, source);
}
