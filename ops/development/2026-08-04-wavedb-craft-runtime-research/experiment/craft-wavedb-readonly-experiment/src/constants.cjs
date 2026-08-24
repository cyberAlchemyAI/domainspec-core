'use strict';

const path = require('node:path');

const REPO_ROOT = path.resolve(__dirname, '../../../../../..');
const EXPERIMENT_ROOT = path.join(
  REPO_ROOT,
  'ops/development/2026-08-04-wavedb-craft-runtime-research/experiment/craft-wavedb-readonly-experiment'
);
const ACCEPTED_RECEIPT = path.join(
  REPO_ROOT,
  'ops/development/2026-08-04-wavedb-craft-runtime-research/experiment/craft-ledger-import/execution/wcli-20260805-node26-0.15.9-03/receipt.json'
);
const ORIGINAL_STORE = path.join(
  REPO_ROOT,
  'ops/development/2026-08-04-wavedb-craft-runtime-research/experiment/craft-ledger-import/.work/wcli-20260805-node26-0.15.9-03/store'
);
const WAVEDB_MODULE = path.join(
  REPO_ROOT,
  'ops/development/2026-08-04-wavedb-craft-runtime-research/experiment/source-build/.work/wcnd-20260805-node26-02/consumer/node_modules/@vijayee/wavedb/lib/wavedb.js'
);
const WAVEDB_PACKAGE_ROOT = path.dirname(path.dirname(WAVEDB_MODULE));
const WAVEDB_ADDON = path.join(WAVEDB_PACKAGE_ROOT, 'build/Release/wavedb.node');
const NODE_BINARY = '/home/vrondelli/.nvm/versions/node/v26.6.0/bin/node';

const EXPECTED = Object.freeze({
  nodeVersion: 'v26.6.0',
  nodeBinarySha256: '02deeca25470eb95255f60147927a1b9785dcb784c9d7690cc712f359331ac8e',
  acceptedReceiptSha256: '544e6bcd81ede733c2e313e18f04ca61a6b5da76e2cc21aff15ddde5d26f046f',
  packageName: '@vijayee/wavedb',
  packageVersion: '0.15.9',
  tarballSha256: 'e8156c107117c8bc7f3394ceb16dff439c87c0cb4f8991033dad960b13ae396f',
  addonSha256: '4846a91117cfeaee42011e401e65448216d85c0ebd04fc860585e3a32e17bb3b',
  moduleSha256: '19726116fb4a4c7f3aeedc67d0af11bd95418de3cc737c1a7a4bb6d73760da7b',
  manifestKey: 'craft/manifest/v2',
  manifestSha256: '780aa8e586eab13bb7478e47783a95017162b41f4834a6be1c7f097aad155014',
  storeDigest: '7ce467aa44b6504347eaef89f601eb04b49647613649314f09fffbe8862289b2',
  storeFileCount: 3,
  storeTotalBytes: 947034,
  ledgerCount: 28,
  totalSourceBytes: 814003,
  recordCount: 57
});

module.exports = Object.freeze({
  ACCEPTED_RECEIPT,
  EXPECTED,
  EXPERIMENT_ROOT,
  NODE_BINARY,
  ORIGINAL_STORE,
  REPO_ROOT,
  WAVEDB_ADDON,
  WAVEDB_MODULE,
  WAVEDB_PACKAGE_ROOT
});
