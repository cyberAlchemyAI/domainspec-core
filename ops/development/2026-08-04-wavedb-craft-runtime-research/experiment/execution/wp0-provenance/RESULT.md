# SWU-WCP-001 Provenance Result

- Result: `BLOCK`
- Failure code: `PACKAGE_PROVENANCE_MISMATCH`
- Package: `@vijayee/wavedb@0.15.8`
- Registry tarball integrity: pass
- Registry SHA-1: pass
- Registry-declared Git head: `54832130f408c44637ad84f35cb93003b0f238c4`
- Package version at that Git head: `0.15.7`
- Reviewed source commit: `01c77e8b70f71de9b72480e73a3a179f6e93a009`
- Package version at reviewed commit: `0.15.8`
- Install/build/addon load: none

Thirty-four shipped binding files matched the reviewed source only after CRLF
normalization. That similarity does not repair the registry metadata/source
contradiction or establish exact provenance for the 192-file packaged C source
tree. The WP-0 rule therefore stops before dependency resolution or native
execution.

The remaining frontier `SWU-WCP-002` through `SWU-WCP-008` was not executed.
No conclusion about projection correctness, WaveDB runtime compatibility,
failure behavior, recovery, or performance is available.
