import fs from 'fs';
import path from 'path';
import * as cheerio from 'cheerio';

const ROOT_DIR = process.cwd();
const PUBLIC_DIR = path.join(ROOT_DIR, 'stitch_tilth_os_institutional_shell 3');
const REPORT_PATH = path.join(ROOT_DIR, 'reports', 'interaction-audit', 'latest.md');

function getStitchScreenFolders() {
  const folders = fs.readdirSync(PUBLIC_DIR, { withFileTypes: true })
    .filter(dirent => dirent.isDirectory())
    .map(dirent => dirent.name);
  return folders;
}

const folders = getStitchScreenFolders();

const stitchNavRoutes = {
  home: "tilth_os_appshell_institutional_workstation",
  scout: "scout_mission_control_functional_openclaw_interface",
  discovery: "scout_mission_control_functional_openclaw_interface",
  openclaw: "scout_mission_control_functional_openclaw_interface",
  intake: "evidence_intake_forensic_identity_governance_mapping",
  eligibility: "eligibility_gates_fail_closed_protocol_3",
  "module mapper": "module_mapper_rfa_decomposition_requirements_4",
  mapper: "module_mapper_rfa_decomposition_requirements_4",
  drafting: "scribe_drafting_unified_execution_canvas",
  budget: "budget_allocator_validator_fiscal_compliance_grid",
  judge: "judge_scoring_multi_variable_forensic_decomposition",
  "red team": "red_team_review_adversarial_probe_trace_5",
  "sign-off": "final_packet_authorization_ready_for_authorization",
  "sign off": "final_packet_authorization_ready_for_authorization",
  "final packet authorization": "final_packet_authorization_ready_for_authorization",
  audit: "audit_trail_forensic_amendment_ledger",
  "audit ledger": "audit_trail_forensic_amendment_ledger",
  fids: "fid_browser_funder_intelligence_library",
  costs: "model_cost_dashboard_operational_visibility",
  "model costs": "model_cost_dashboard_operational_visibility",
  hybrid: "tilth_os_workstation_high_confidence_update",
  verified: "audit_trail_beneficiary_verified_ledger",
  "audit log": "audit_trail_forensic_amendment_ledger",
  "system health": "audit_trail_beneficiary_verified_ledger",
  "machine id": "audit_trail_beneficiary_verified_ledger",
  "refresh sam.gov connection": "eligibility_gates_fail_closed_protocol_3",
  "view full audit log": "audit_trail_forensic_amendment_ledger",
  "executive override": "eligibility_gates_fail_closed_protocol_3",
  "open eligibility": "eligibility_gates_fail_closed_protocol_3",
  "review requirement": "evidence_intake_forensic_identity_governance_mapping",
  "initialize openclaw": "scout_mission_control_functional_openclaw_interface",
};

// Mirror of server.mjs logic for resolving route to actual code.html path
function resolveRouteToFile(routePath) {
  if (routePath === '/') routePath = '/home';
  const cleanRoute = routePath.replace(/^\//, '').toLowerCase().replace(/%20/g, ' ');
  
  if (stitchNavRoutes[cleanRoute]) {
    return path.join(PUBLIC_DIR, stitchNavRoutes[cleanRoute], 'code.html');
  }

  return null;
}

async function run() {
  if (!fs.existsSync(REPORT_PATH)) {
    console.error(`Report not found at ${REPORT_PATH}`);
    process.exit(1);
  }

  const reportContent = fs.readFileSync(REPORT_PATH, 'utf-8');
  const lines = reportContent.split('\n');

  // Parse lines: - **/route** | Index 0 - <button> "RESCAN" -> `FAIL_VISUAL_ONLY_BUTTON`
  const regex = /^- \*\*(.*?)\*\* \| Index (\d+) - <(.*?)> ".*?" -> `(.*?)`/;
  
  const deletionsByRoute = {};

  for (const line of lines) {
    const match = line.match(regex);
    if (match) {
      const route = match[1];
      const index = parseInt(match[2], 10);
      const tag = match[3];
      const result = match[4];

      if (result === 'FAIL_VISUAL_ONLY_BUTTON') {
        if (!deletionsByRoute[route]) deletionsByRoute[route] = [];
        deletionsByRoute[route].push({ index, tag });
      }
    }
  }

  let totalRemoved = 0;

  for (const [route, removals] of Object.entries(deletionsByRoute)) {
    const htmlPath = resolveRouteToFile(route);
    if (!htmlPath || !fs.existsSync(htmlPath)) {
      console.warn(`Could not resolve HTML file for route ${route}`);
      continue;
    }

    const htmlContent = fs.readFileSync(htmlPath, 'utf-8');
    // We use cheerio without wrapping it inside a full HTML document if possible,
    // but Stitch outputs full HTML documents (with html, head, body).
    const $ = cheerio.load(htmlContent);

    // Get all interactive elements in the EXACT same way the crawler did
    // The crawler did: document.querySelectorAll('a, button')
    const elements = $('a, button');

    // Sort removals descending by index so we don't mess up indices when we remove?
    // Wait, cheerio `.remove()` just removes the element from the AST, it doesn't shift the array returned by `$('a, button')`.
    // The array `elements` is static.
    
    let removedCount = 0;
    for (const removal of removals) {
      const el = elements[removal.index];
      if (el) {
        $(el).remove();
        removedCount++;
        totalRemoved++;
      } else {
        console.warn(`Could not find element at index ${removal.index} in ${route}`);
      }
    }

    if (removedCount > 0) {
      // Write back
      fs.writeFileSync(htmlPath, $.html(), 'utf-8');
      console.log(`Pruned ${removedCount} dead elements from ${route}`);
    }
  }

  console.log(`\nPruning complete! Removed ${totalRemoved} dead elements in total.`);
}

run().catch(console.error);
