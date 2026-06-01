<!--
  admin_risk_register_audit_decisions.md

  One row per term in admin_risk_register.yaml.
  Operator workflow:
    1. Fill audit_status for each row:
         - confirmed_avoid_all   → AVOID-everywhere is the right
                                   default for this term across all 8 CLCs
                                   (empty per_clc_register on the register entry)
         - confirmed_per_clc     → operator populated per_clc_register on the
                                   register entry with explicit per-CLC values
    2. Run scripts/run_tests.sh (or equivalent) on a fixture to verify
       the gate is happy with the current per_clc_register state.
    3. Run `python pipeline/scripts/audit_term_signer.py --key <path>`
       to fill the signature_hex + pubkey_hex columns.
    4. Commit + run the LOCK ceremony.

  Canonical bytes the per-term signature covers:
    json.dumps({"audit_status": <s>, "term": <t>, "term_hash": <h>},
               sort_keys=True, separators=(",", ":"),
               ensure_ascii=False).encode("utf-8")

  Authority: §4 v2.x apolitical_dialect §4.X.6 + Cycle 2 fold-ins
  C2-H-4 (per-term Ed25519) + C2-NEW-MED-2 (audit_status closed set)
  + C2-NEW-MED-4 (try/except on missing file).
-->

# admin_risk_register migration — per-term audit decisions

| term | term_hash | audit_status | operator_ed25519_signature_hex | operator_pubkey_ed25519_hex |
|------|-----------|--------------|--------------------------------|-----------------------------|
| DEI | c0459bc9137951678dcae7662f57af371fe8f18b7651ebfa5ada083950122a98 | <PENDING> | <PENDING> | <PENDING> |
| equity | 903ba94cd3fd59ded3b6f329a363b8364f8632cebe0b657697a66471d7412ecf | <PENDING> | <PENDING> | <PENDING> |
| environmental justice | cc276c15a5796e06daefe9c230e16900a009b96bda24b266dc57b64435d0a76d | <PENDING> | <PENDING> | <PENDING> |
| climate justice | 018d5c5d7441038b257f24ff94ddff4a0017993403538ec97936da1ad5139996 | <PENDING> | <PENDING> | <PENDING> |
| transgender | 258867f5f3937cbc37d9084fa507038ef1320daa942b221441346432f4ebec4d | <PENDING> | <PENDING> | <PENDING> |
| LGBTQ | 48e2b4e26d23c7a3c363a568c7290b64fe0389cd449b1a1a91f7e44e1fb3faea | <PENDING> | <PENDING> | <PENDING> |
| gender identity | 25ec036acc1b26b1f9f22d8c746983a6a97b4dc06a9b41810bb593797fd685a8 | <PENDING> | <PENDING> | <PENDING> |
| gender-affirming | 777f96e59dd44657f1276bd03d19735f175d9bfe51845b228e39456369a3d1b1 | <PENDING> | <PENDING> | <PENDING> |
| gender ideology | eb7d4e70bb902adfd9229a1eb96f25cdb6bd7a1d4183c9855abaa61615d8df44 | <PENDING> | <PENDING> | <PENDING> |
| sexual orientation | a27ad05803c77e76779027b76db8d5d1007e15d6fed38acc64d924d55d646024 | <PENDING> | <PENDING> | <PENDING> |
| underrepresented | d859b9adcad099b7c7a0192ffb768b8e9a9e5eb20380c1e35236906e3f03ee46 | <PENDING> | <PENDING> | <PENDING> |
| women | a92a82e5c0c5a4996062e4cdd878f5427196318fdd73516cd815ab461d2613ed | <PENDING> | <PENDING> | <PENDING> |
| minority | b2cd9d4a4d0134a792956e053191b55f74c37310f58f3a3dbbbba4afcfbe9a1b | <PENDING> | <PENDING> | <PENDING> |
| systemic racism | 1aec1984dbdb0dbf76a410926ee52aab2d1e3e4e5974b93958719e43824e655f | <PENDING> | <PENDING> | <PENDING> |
| social justice | 8b67eca1612fe6b9bfe645f7e8de14c244baf233483457021609f2ba5a0f89df | <PENDING> | <PENDING> | <PENDING> |
| transformative justice | 1e9f1865b4652d70968695902d500c1b8a58ade9ba2eb3374c946bf0bca3ea22 | <PENDING> | <PENDING> | <PENDING> |
| BIPOC | ac4516ac9618ea466b38a1e63de0f66a4bbff922ed8f1af1ee9c4af843d13751 | <PENDING> | <PENDING> | <PENDING> |
| anti-racism | d554e1f6175f137a5df46a8d85ce2fdc05607fc7488398e93febdf2f506b9c10 | <PENDING> | <PENDING> | <PENDING> |
| decolonize | 57fc6aba1485680aa9c94a5767787105d8e4b33924051a74e161597f75a40c0a | <PENDING> | <PENDING> | <PENDING> |
| reparations | 4307964c4a7ffcfb723978206d9000757a897e5bec02304db63ab2a3da6b6b38 | <PENDING> | <PENDING> | <PENDING> |
| marginalized | f2e25b833bd58eaf4fff8004796626bfa1747111328bfa3498bc936591cc6e38 | <PENDING> | <PENDING> | <PENDING> |
| diversity | 68812a66f0e0116de01b683232b876c7c940be2d3cf2417d8e344868b42d387b | <PENDING> | <PENDING> | <PENDING> |
| inclusion | 33a041e0b666dd16a7db008192119205d3d470b8687473a7f3db30f6511ce978 | <PENDING> | <PENDING> | <PENDING> |
| critical race theory | 6cb0ba91a47c6b0900a29a304d5d50bcfabe0e455ca692320bb0145936b75a5a | <PENDING> | <PENDING> | <PENDING> |
| woke | 675c8996b8251d2bcce9f0f0800da1143276b4715a67a9657c5d18e267cdd633 | <PENDING> | <PENDING> | <PENDING> |
| disparities | f5742f0e2b4343b72de857fc76fc97ac4a6e105520987d97184d0ba19e4dbe95 | <PENDING> | <PENDING> | <PENDING> |
| sense of belonging | 9d2e45f9d7acca75c9dbadffb2e1ceaeff626ff67536a69b36e7204a1fddd0f2 | <PENDING> | <PENDING> | <PENDING> |
| institutional | a581b0dbc76fc2709bca8ffebb82c15334c4c28af0a74dbf8268bd258d53670b | <PENDING> | <PENDING> | <PENDING> |
| activism | 9318d030c18af75a0446c4478b5e77f6f432314191f5308fe73b51acf1e61f24 | <PENDING> | <PENDING> | <PENDING> |
| prejudice | 25c83ec0d91ff200943ed96611d5e6a0c98d13effca507e06d77b713058e1d3c | <PENDING> | <PENDING> | <PENDING> |
| privilege | a4613ec03ab2a3785466c5875c74d8af26b47bfc2f77e03fd861c23403e6d60f | <PENDING> | <PENDING> | <PENDING> |
| disabilities | 97849ab8c57c12182029dd58af62c082e5048138b6e5eb574bd5ee0b28ac4901 | <PENDING> | <PENDING> | <PENDING> |
| underserved | 62d745b5ef12177151382785e48a9bf7e21a26949d96b9db49eddab99af726ae | <PENDING> | <PENDING> | <PENDING> |
| female | c243f43f442722ce6a5508cd8bda16597444559a19c7d2391e07ff8039ea49ee | <PENDING> | <PENDING> | <PENDING> |
| equal opportunity | 36eb7fde2391c8aa63f7cfaced58c1e463662ce5b1cf109df5485807f862d0f9 | <PENDING> | <PENDING> | <PENDING> |
| food sovereignty | 93d54c627ddd9b655269b1119e3077cb425a880b5f8fb6b2ceb0a6bec32433a7 | <PENDING> | <PENDING> | <PENDING> |
| land back | d54a1e84fb5a29884db98392e790343cad50d3761ae8a851d06de9353dc2e021 | <PENDING> | <PENDING> | <PENDING> |
| solidarity economy | 3c3c02d8b2c02e29090c87131f799d6cca7101200e9f8e5a22f8e84bf4f11161 | <PENDING> | <PENDING> | <PENDING> |
| mutual aid | cf32611c8dfb1c50f4538fd805efc013e97ec5358395efb2a62835cc17d85428 | <PENDING> | <PENDING> | <PENDING> |
| abolition | 3a4b478b262453189cc2a195d3eb3644b0c2e41977014ce2a1c48c546fb695d5 | <PENDING> | <PENDING> | <PENDING> |
| intersectional | 7baf4245234a48c0a2b5a0aa57e28c306e34db403225e6da6e22cc5fe89c574b | <PENDING> | <PENDING> | <PENDING> |
| climate change | 4c2fc42fddcec26cd8954249ae012fc09c82e857f9e0b6eb484005a7bd6a3009 | <PENDING> | <PENDING> | <PENDING> |
| green | c38bada4e644886e9858385044f6fc64c189ce603b56e0e20ff1fc9317a7f969 | <PENDING> | <PENDING> | <PENDING> |
| ESG | 2f87df0d5cd3e49f70bda9406e00f0a188cbbbf9ce9f6f43f5b30eadc34dae60 | <PENDING> | <PENDING> | <PENDING> |
| renewable energy | 664973e3f9406751d8150117e74892938729431c1e4c28260141ade0ab01ab43 | <PENDING> | <PENDING> | <PENDING> |
| clean energy | 5c4a51aae2448119d90ef7101c7acaeeed6d7af03d4390e3302e4546376f36b9 | <PENDING> | <PENDING> | <PENDING> |
| carbon | e6058e6fb28a044db82e3c491fdc9e62326bf7045fd692ddd911602b23bb7ad7 | <PENDING> | <PENDING> | <PENDING> |
| net-zero | 3276cd2040d184965775a99d0d479e5b807bbffa0acf2de54c98ba92645171b4 | <PENDING> | <PENDING> | <PENDING> |
| decarbonization | 42137abd9a7f27f79fc5ae4fc48527217bfd65ae879f10a0c82c18296583c651 | <PENDING> | <PENDING> | <PENDING> |
| greenhouse gas | 9560403a63043ba006dcd9cba9856a7bfcb9d0fea4d8f160895c62e1f34765bf | <PENDING> | <PENDING> | <PENDING> |
| environmental justice | cc276c15a5796e06daefe9c230e16900a009b96bda24b266dc57b64435d0a76d | <PENDING> | <PENDING> | <PENDING> |
| just transition | 9590687f41e35590bdc2dffab8a2eed94ad51f6076ba069ec5093607817ad178 | <PENDING> | <PENDING> | <PENDING> |
| health equity | bd6b59bc06abd90cc0697ef2d22ae6e5c94fc863c5f8e6f1e261a4f70b37784b | <PENDING> | <PENDING> | <PENDING> |
| structural racism | 126931a6dd34bf355215b4fbf2a74b02e93677ae2f19a69adcec1e7d9358c550 | <PENDING> | <PENDING> | <PENDING> |
| social determinants of health | faf9e9c77c86e50a699bd6ba75f816f3eacc68d45c2afd0a7588dcd54260f7fd | <PENDING> | <PENDING> | <PENDING> |
| reproductive rights | 30931de69cbb4a06f4baf2b0614adf572b92f40d23b2cf1ad61b7ec79fddbc1d | <PENDING> | <PENDING> | <PENDING> |
| reproductive justice | 8364d12ff137adea772cdaecbd8f6e2e913ae6512af6884ba094eca11abd15a5 | <PENDING> | <PENDING> | <PENDING> |
| abortion | d0c8adbf2d706f70788a0875a415fb178f7823cba99416cf2765c17354eb8585 | <PENDING> | <PENDING> | <PENDING> |
| sustainability | ca006833ad99d85d5a3fb0682cd28533ea1728267a457cd6757b6a19178c5ce1 | <PENDING> | <PENDING> | <PENDING> |
| climate resilience | e6badfdb508588de284efadeccf2a6ca3d061776b56d05b0ee7be569acbe53cc | <PENDING> | <PENDING> | <PENDING> |
| global warming | 79a8a42e674a8f0deb2a05c07837188739f17e812de53111844f9476777f47c8 | <PENDING> | <PENDING> | <PENDING> |
| impact investing | ffde65a4fbe778c63d14bc0afec13d10032eea75fa002669515ae0a153fda58d | <PENDING> | <PENDING> | <PENDING> |
| stakeholder capitalism | e0c6ce405b24d1e2e4104af8737d04afc588de9a938fed0895f6792026f5fb63 | <PENDING> | <PENDING> | <PENDING> |
| triple bottom line | 4e95938255de962fcf36c91a2e49ba7abbeecb4f4d102242cd74ea07743489ab | <PENDING> | <PENDING> | <PENDING> |
| community-centered | 06aede09fac8f09604ad56dd460b8233da46ece4a01a487707573e538f075e00 | <PENDING> | <PENDING> | <PENDING> |
| culturally responsive | 16419b258a8430ccc9456cd1f82f77b9d223b1dc618086365fcf2c2ee9a5b050 | <PENDING> | <PENDING> | <PENDING> |
| lived experience | 6b12e80a354fcd2f06ac42bd46b753351cffcaef672b84edf59d8a1b28ea2523 | <PENDING> | <PENDING> | <PENDING> |
| amplify | 605cc2ab0df1ac90513a725adf82c15ab944a04e50ebd45dc5d585ad80915ddb | <PENDING> | <PENDING> | <PENDING> |
| center | 1d9349b18892e77d50066816fc75d71270d95e834a7e7a1a4fe43de3e5124e1c | <PENDING> | <PENDING> | <PENDING> |
| representation | 1c400b7ba2214b7af814d071e30de7c8ccd9e70dd52ce5d334d763dd9f1b72ae | <PENDING> | <PENDING> | <PENDING> |
| allyship | ee08adbb091dfe86dcd498aae3e1713d52d5a9bf4d07f49540fd3202e8ad0d52 | <PENDING> | <PENDING> | <PENDING> |
| safe space | a82afe8b4be4ebf6152eb50603f22db0e92414e3797bb223264c63faeeb6c42f | <PENDING> | <PENDING> | <PENDING> |
| microaggressions | 1377536ffffe418457cae20576f3cf49d9cbefcee136a58c2285a3d0bc456825 | <PENDING> | <PENDING> | <PENDING> |
| positionality | e1af3e420e889de0cc9c32381bfd37dc83bb60b6ae5d35ca4e3b5b8c2dc50ae4 | <PENDING> | <PENDING> | <PENDING> |
| white privilege | fc01022d2ab093bad8a7e261201cc418e5e0d7cc9dbbba49f756c243e9ad7ac0 | <PENDING> | <PENDING> | <PENDING> |
| white supremacy | fbd19adebf8869caa97c5fc24d68892aed647e6089f8d5625aded4377b8ff8a9 | <PENDING> | <PENDING> | <PENDING> |
| cisgender | 4cbe292632c472e77a03c6f136b5bfac44188e4da13b2e2ec7bab0627a98f3f2 | <PENDING> | <PENDING> | <PENDING> |
| patriarchy | 2a5ae4f9430ea312b56061683ab0bfe8c93459a88c3cef67ed08c6116463c65a | <PENDING> | <PENDING> | <PENDING> |
| DACA | de1d1868660ac3cb9011ca775ce942a31a8a412841096d41ec392a0b28ed88c2 | <PENDING> | <PENDING> | <PENDING> |
| undocumented | e1a2381e8e1ba941b92ff7ed6e895085076ac62af4dfa1408ff7974f90bab1e2 | <PENDING> | <PENDING> | <PENDING> |
| sanctuary | 4952ed316f5a8777943db3571826ef04063f6ab3c8b18b8f51434c434657d130 | <PENDING> | <PENDING> | <PENDING> |
| asylum seeker | 11ab2b9b0d287ff4a2508ae7074d42f26be2e4204f29f0b5ea0d2ae32e23f33a | <PENDING> | <PENDING> | <PENDING> |
| trauma-informed | 073fb32bd1a7247d72cae37249d0a986e4d30e3d60b6d03b019eb875b7ed31ee | <PENDING> | <PENDING> | <PENDING> |
| social-emotional learning | 012113beb932e9aee314c62b7003d3e7920402af31d2fe58de66df22d856e7e0 | <PENDING> | <PENDING> | <PENDING> |
| harm reduction | efa4b4895da50cc7cf8e687f702be6adc2324308cec698f5d88b9f5989645d9c | <PENDING> | <PENDING> | <PENDING> |
| infrastructure | a9fc1675fa345e1604d724c7f99016aee3cf3a6e6736748ba8ce534c56fa45ff | <PENDING> | <PENDING> | <PENDING> |
| scalability | 88345953271901f76999cb1a4777e3532c8c78d0683d46d33ed5b89273d32e97 | <PENDING> | <PENDING> | <PENDING> |
| capacity building | bc7b17fde03f4f9cdbb51f5b138fd641ece26d8d1bcc64f4d9d8d52acc6024d5 | <PENDING> | <PENDING> | <PENDING> |
| innovation | 0f09e6489637d4330f00043265441368cea1810f29ddac6a34c519f4863e5f88 | <PENDING> | <PENDING> | <PENDING> |
| transformation | 9dd8a9c116e8875733df928c1dc68b63f3a669b5e2eff1cd384ba5dd3ec83da5 | <PENDING> | <PENDING> | <PENDING> |
| stakeholder | 1aed213d7e9b9d66839acf545d807b630428348463377eb61ecdf8fb853c3074 | <PENDING> | <PENDING> | <PENDING> |
