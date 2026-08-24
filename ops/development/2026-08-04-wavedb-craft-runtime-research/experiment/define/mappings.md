# Mappings

## Canonical YAML to normalized model

1. Read exact bytes with no newline normalization.
2. Validate against the pinned Craft schema stack.
3. Parse using the pinned parser/version/options.
4. Normalize only schema-admitted values.
5. Serialize canonical JSON with recursively sorted object keys, retained array
   order, UTF-8, no insignificant whitespace, and no terminal newline.

## Normalized model to projection

- generation prefix: `/craft/v1/workspaces/<W>/generations/<H_L>/`;
- keys use NFC then RFC 3986 percent encoding for variable segments;
- source YAML bytes are preserved exactly;
- row values contain one normalized entity, canonical ID, and source selector;
- indexes contain ordered IDs/selectors only;
- derived bytes are comparisons, never authority;
- the manifest is written last and enumerates every non-manifest key/value.

Exact admitted key families and hash formulas remain those frozen in
`../../findings.md#exact-v0-key-value-and-codec-proposal`.
