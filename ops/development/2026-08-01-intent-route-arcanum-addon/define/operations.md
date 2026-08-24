# Operations

| Operation | Input | Output | Effect boundary |
|---|---|---|---|
| validate request | request bytes and protocol versions | typed request or rejection | pure |
| validate catalog | frozen catalog bytes and expected bindings | admitted catalog or invalid | pure |
| resolve route | admitted request and catalog | one disposition | pure and non-authorizing |
| run JSON port | one bounded stdin document | one bounded stdout document and numeric exit | local process only |
| project runtime intent | runtime-local capture and mapping profile | request or typed rejection | runtime-owned; no semantic repair |
| generate runtime package | accepted canonical sigil closure and profile | generated package | Bootstrap-owned projection |
| consume disposition | trusted response | display/clarification or stop | consumer-owned; no automatic bind |

