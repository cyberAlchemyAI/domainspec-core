'use strict';

const fs = require('node:fs');
const path = require('node:path');

const repositoryRoot = path.resolve(__dirname, '../../../');
const inventoryRoot = path.join(repositoryRoot, '.arcanum', 'inventory');
const recordPath = path.join(
  inventoryRoot,
  'tmp',
  'arcanum-addon-selection-revalidation-strategy-result-synthesis.record.json',
);
const indexPath = path.join(inventoryRoot, 'index.json');
const humanIndexPath = path.join(inventoryRoot, 'index.md');
const {
  facetPolicyFromIndex,
  normalizeEntry,
  serializeIndex,
  updateHumanIndex,
  updateIndex,
} = require(path.join(
  repositoryRoot,
  '.agents',
  'skills',
  'inventory',
  'lib',
  'inventory-update.cjs',
));

const timestamp = '2026-07-30T19:32:21Z';
const record = JSON.parse(fs.readFileSync(recordPath, 'utf8'));
const index = JSON.parse(fs.readFileSync(indexPath, 'utf8'));
const normalized = normalizeEntry(record, timestamp, facetPolicyFromIndex(index));
const indexTransition = updateIndex(index, normalized, timestamp);

if (indexTransition.disposition !== 'added') {
  throw new Error(`unexpected index disposition: ${indexTransition.disposition}`);
}

const humanIndex = fs.readFileSync(humanIndexPath, 'utf8');
const humanTransition = updateHumanIndex(humanIndex, normalized);
if (!humanTransition.changed || humanTransition.reason !== 'row-added') {
  throw new Error(`unexpected human-index disposition: ${humanTransition.reason}`);
}

fs.writeFileSync(indexPath, serializeIndex(indexTransition.index));
fs.writeFileSync(humanIndexPath, humanTransition.markdown);
process.stdout.write(
  `INVENTORY_PROJECTION=added\nENTRY_ID=${normalized.id}\nTIMESTAMP=${timestamp}\n`,
);
