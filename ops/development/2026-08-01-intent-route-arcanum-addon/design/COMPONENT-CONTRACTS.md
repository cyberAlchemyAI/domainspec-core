# Component contracts

## Canonical sigil closure

Required support files are schemas, pure core, JSON entrypoint, manifest,
synthetic fixtures, scans, and acceptance runners. Bootstrap must include this
closure for both profiles and bind a single closure digest.

## Generic resolver contract

The core consumes only JSON values. It produces a complete evaluated-route
trace and one terminal kind. It has no environment, filesystem, network,
model, agent-runtime, product, Dispatch, or effect dependency.

## Runtime adapter contract

The adapter pins one local executable and validates input ceiling, timeout,
exit, stdout document count and size, zero stderr, protocol/core/manifest/
catalog/content digests, result shape, and `authority_effect`. It returns a
trusted disposition or typed rejection. It does not modify the request and
does not retry semantically.

## Consumer contract

A consumer may display a trusted disposition, ask its exact clarification,
collect a new/updated intent, or stop. It may separately accept an already
confirmed existing Dispatch binding. Resolver output alone cannot invoke the
binding path.

