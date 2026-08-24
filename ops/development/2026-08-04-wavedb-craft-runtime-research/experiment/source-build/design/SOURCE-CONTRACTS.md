# Source contracts

| ID | Source | Controls | Current identity |
| --- | --- | --- | --- |
| SC-SB-001 | `define/SPEC.md` | source-build scope, invariants, outputs, exclusions | SHA-256 `61fedd4389ecbba82fecf333e19dc70abe95f8a9a2ce4fa2d0f3e1627bbe932a` |
| SC-SB-002 | parent provenance decision | explicit alternate route and non-collapse with npm | SHA-256 `7beb196911f60ed19e9f348176916955c4192f6c65bf830be5d42b1ba2d3e947` |
| SC-SB-003 | provenance history reconstruction | reviewed commit, submodules, package relationship | SHA-256 `656f99ca59d56728b7feedece3d2a44a935c28759b153b860d9ae569a51bd7fe` |
| SC-SB-004 | parent findings | WP-0 toolchain/package gate and claim ceiling | SHA-256 `958ed1ae74cfad7483a70f6ca7a78ba5a970a97e928da4d88e40979f680b53f0` |
| SC-SB-005 | reviewed WaveDB `package-lock.json` | complete npm dependency resolution | execution must require SHA-256 `26fbf0839106a0521f1ad6785764cefa3d39aedd9ff8412c982689c09b109f95` |
| SC-SB-006 | reviewed WaveDB build surface | `package.json`, `binding.gyp`, `build.js`, `copy-sources.js` | SHA-256 `82e87aaaac10113cb1294732bf149356f6f7df76ecde0259181999c6a3fe9dc3`, `5a326bf16ce349808572fcd213344868edeabf70fb75a10f56c1c9f429d5b90f`, `ff00fe3c9c3dbfc5401c611feac70a8148a92f158bfaa6ec30acbfade214d1bc`, `466f86b07e370a4cfcde0ff3d4f4639564344247f08d480ba6ed4d2c6b3e420a` respectively |

SC-SB-005 and SC-SB-006 are external Git bytes. Their current hashes were
observed during Define and must be independently re-derived in full from the exact
checkout during Task Session; Design does not treat the observation as build
evidence.
