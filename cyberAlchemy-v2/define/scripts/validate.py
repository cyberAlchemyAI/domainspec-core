#!/usr/bin/env python3
"""Deterministic, check-only validator for the private Define bridge package."""
from __future__ import annotations
import hashlib, json, subprocess, sys
from pathlib import Path
from typing import Any
PACKAGE=Path(__file__).resolve().parents[1]
REPO=PACKAGE.parents[1]
MATERIAL_FILES=("README.md","definitions.json","docs/AUTHORITY.md","docs/DEFINE.md","docs/DEFINITION-PACK.md","docs/INTERACTION.md","docs/LIFECYCLE.md","documents.json","migration/invoke.json","nodes.json","profile.json","relations.json","residue.jsonl","schemas/define-package.schema.json","scripts/validate.py","sources.json","views.json")
checks=[]
def add(i,o,d): checks.append({"check_id":i,"outcome":o,"detail":d})
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def readj(rel): return json.loads((PACKAGE/rel).read_text(encoding="utf-8"))
def unique(v): return len(v)==len(set(v))
def authority_none(v):
 if isinstance(v,dict): return all((k!="authority_effect" or x=="none") and authority_none(x) for k,x in v.items())
 if isinstance(v,list): return all(authority_none(x) for x in v)
 return True
def child_nodes(child_id):
 if child_id=="business": return {x["id"] for x in readj("business-ontology/NODES.json")["nodes"]}
 return {x["node_id"] for x in readj("system-ontology/NODES.json")["nodes"]}
def run_child(row):
 path=PACKAGE/row["validator_path"]
 one=subprocess.run([sys.executable,str(path)],cwd=REPO,capture_output=True)
 two=subprocess.run([sys.executable,str(path)],cwd=REPO,capture_output=True)
 deterministic=one.returncode==two.returncode and one.stdout==two.stdout and one.stderr==two.stderr
 try: output=json.loads(one.stdout)
 except Exception: output={}
 expected=(0,"PASS") if row["child_id"]=="business" else (2,"FLAG")
 outcome_ok=one.returncode==expected[0] and output.get("overall")==expected[1]
 output_hash=hashlib.sha256(one.stdout).hexdigest(); material=output.get("material_digest")
 current=[]
 for rp in sorted(PACKAGE.glob(row["receipt_glob"])):
  try:r=json.loads(rp.read_text())
  except Exception:continue
  if r.get("ontology_id")==row["ontology_id"] and r.get("material_digest")==material and r.get("validation_output_sha256")==output_hash and r.get("authority_effect")=="none":current.append(r)
 return deterministic and outcome_ok and len(current)==1, one.returncode, output, output_hash, len(current)
profile=readj("profile.json"); sources_doc=readj("sources.json"); definitions=readj("definitions.json"); documents=readj("documents.json"); nodes_doc=readj("nodes.json"); relations_doc=readj("relations.json"); views_doc=readj("views.json"); migration=readj("migration/invoke.json"); schema=readj("schemas/define-package.schema.json")
residue=[json.loads(x) for x in (PACKAGE/"residue.jsonl").read_text().splitlines() if x]
# Parent inventory excludes declared nested packages, append-only receipts, and package-local collaboration evidence.
actual=[]
for path in PACKAGE.rglob("*"):
 if not path.is_file():continue
 rel=path.relative_to(PACKAGE); top=rel.parts[0]
 if top=="receipts" or top in profile.get("nested_package_roots",[]) or str(rel) in profile.get("collaboration_files",[]):continue
 actual.append(str(rel))
inventory_ok=sorted(actual)==sorted(MATERIAL_FILES) and profile.get("material_files")==list(MATERIAL_FILES) and profile.get("nested_package_roots")==["business-ontology","system-ontology"] and profile.get("collaboration_files")==[".craft/ledger.yml","CRAFT.md"]
add("closed-parent-inventory-and-nested-boundaries","PASS" if inventory_ok else "BLOCK",f"{len(actual)} parent material files; 2 excluded child package roots")
profile_ok=profile.get("package_id")=="cav2.define" and profile.get("package_version")=="0.4.0-candidate" and profile.get("ontology_type")=="business-system-bridge" and profile.get("current_lifecycle_state")=="candidate-authored" and profile.get("visibility")=="private" and profile.get("authority_effect")=="none"
add("bridge-profile-identity","PASS" if profile_ok else "BLOCK","parent owns only the business-system bridge")
children=profile.get("child_packages",[]); child_map={x.get("child_id"):x for x in children}; child_shape=set(child_map)=={"business","system"} and all(x.get("branch")==x.get("child_id") and x.get("visibility")=="private" and x.get("authority_effect")=="none" for x in children)
add("child-package-declarations","PASS" if child_shape else "BLOCK","business and system children have explicit identity, owner, validator, and receipt bindings")
branches=profile.get("branches",[]); branch_ok={x.get("branch_id") for x in branches}=={"business","system","bridge"} and all(x.get("ownership")==("parent-package" if x.get("branch_id")=="bridge" else "child-package") for x in branches)
add("branch-ownership-separation","PASS" if branch_ok else "BLOCK","business and system are child-owned; bridge is parent-owned")
required_defs={"sourceRef","branch","childPackage","profile","source","sourceRegistry","canonicalBinding","definitionProposal","definitionRegistry","documentAdmission","document","documentRegistry","node","nodeRegistry","relation","relationRegistry","view","viewRegistry","residueEntry","migrationSurface","migrationPhase","migration","validationReceipt"}
add("schema-definition-surface","PASS" if schema.get("$schema")=="https://json-schema.org/draft/2020-12/schema" and set(schema.get("$defs",{}))>=required_defs else "BLOCK","owned schema includes child-package and bridge bindings")
source_ids=[x["id"] for x in sources_doc.get("sources",[])]; add("source-id-uniqueness","PASS" if unique(source_ids) else "BLOCK",f"{len(source_ids)} parent evidence sources")
drift=[]; selector_fail=[]
for row in sources_doc.get("sources",[]):
 p=(REPO/row["path"]).resolve(); current=p.is_file() and REPO in p.parents and sha(p)==row["sha256"] and p.stat().st_size==row["size"]
 if not current:drift.append(row["id"]);continue
 try:text=p.read_text(encoding="utf-8")
 except Exception:text=""
 if not all(x in text for x in row["selectors"]):selector_fail.append(row["id"])
add("source-digest-and-size-currency","PASS" if not drift else "BLOCK","current" if not drift else "drift: "+", ".join(drift))
add("source-selector-resolution","PASS" if not selector_fail else "BLOCK","all selectors resolve" if not selector_fail else "missing selectors: "+", ".join(selector_fail))
# Retain the existing definition/document/migration contracts without granting promotion.
bindings=definitions.get("canonical_bindings",[]); proposals=definitions.get("proposals",[]); definition_ok=len(bindings)==10 and len(proposals)==3 and all(x.get("authority_effect")=="none" for x in bindings+proposals)
add("definition-bindings-and-candidates","PASS" if definition_ok else "BLOCK","10 canonical bindings and 3 unpromoted candidates")
docs=documents.get("documents",[]); docs_ok=len(docs)==5 and documents.get("canonical_admission",{}).get("status")=="blocked"
for row in docs:
 p=PACKAGE/row.get("path",""); text=p.read_text(encoding="utf-8") if p.is_file() else ""; docs_ok &= text.startswith("# "+row.get("title","")+"\n") and all(h in text for h in row.get("required_headings",[])) and row.get("canonical_status")=="not-admitted" and row.get("authority_effect")=="none"
add("perennial-document-closure","PASS" if docs_ok else "BLOCK","five non-admitted perennial candidate documents")
phase_ids=[x.get("id") for x in migration.get("phases",[])]; migration_ok=phase_ids==["source-substrate-pinned","cav2-candidate-package-authored","cav2-package-validated","cav2-definitions-promoted","cav2-runtime-adopted","invoke-migration-decided","invoke-migration-executed"] and migration.get("public_change",{}).get("status")=="not-performed" and migration.get("authority_effect")=="none"
add("migration-order-and-public-ceiling","PASS" if migration_ok else "BLOCK","public Invoke remains unchanged and later phases pending")
# Validate child identities before resolving qualified endpoints.
child_profile_ok=True
for cid,row in child_map.items():
 try: cp=readj(row["profile_path"])
 except Exception: child_profile_ok=False;continue
 child_profile_ok &= cp.get("ontology_id")==row["ontology_id"] and cp.get("ontology_type")==row["ontology_type"] and cp.get("branch")==row["branch"] and cp.get("owner_route")==row["owner_route"] and cp.get("visibility")==row["visibility"] and cp.get("authority_effect")=="none"
add("child-profile-identity-bindings","PASS" if child_profile_ok else "BLOCK","declared child identities match exact profiles")
business_ids=child_nodes("business"); system_ids=child_nodes("system"); external={*("business::"+x for x in business_ids),*("system::"+x for x in system_ids)}
local_nodes=nodes_doc.get("nodes",[]); local_ids={x.get("id") for x in local_nodes}; local_ok=len(local_nodes)==1 and local_ids=={"BR-DEFINE-PRODUCT-RUNTIME"} and all(x.get("branch")=="bridge" and x.get("role")=="alignment" and x.get("authority_effect")=="none" for x in local_nodes)
add("parent-bridge-node-ownership","PASS" if local_ok else "BLOCK",f"{len(local_nodes)} parent-owned bridge node; no duplicate business/system nodes")
rels=relations_doc.get("relations",[]); rel_ids=[x.get("id") for x in rels]; universe=local_ids|external
rel_ok=len(rels)==10 and unique(rel_ids) and all(x.get("branch")=="bridge" and x.get("source") in universe and x.get("target") in universe and x.get("source")!=x.get("target") and x.get("type") in profile.get("allowed_relation_types",[]) and x.get("authority_effect")=="none" and all(r.get("source_id") in source_ids for r in x.get("source_refs",[])) for x in rels)
add("cross-package-relation-endpoint-closure","PASS" if rel_ok else "BLOCK",f"{len(rels)} bridge relations close over current child records")
views=views_doc.get("views",[]); view=views[0] if len(views)==1 else {}; view_ok=view.get("branch")=="bridge" and set(view.get("relation_ids",[]))==set(rel_ids) and set(view.get("node_ids",[]))=={x for r in rels for x in (r.get("source"),r.get("target"))}
add("bridge-view-total-coverage","PASS" if view_ok else "BLOCK","one parent bridge view covers all edges and endpoints")
subject_universe=universe|local_ids|{x.get("candidate_id") for x in proposals}|{x.get("id") for x in bindings}|{x.get("id") for x in docs}|{"cav2.define",migration.get("migration_id")}
residue_ok=unique([x.get("id") for x in residue]) and all(set(x.get("subject_refs",[]))<=subject_universe and all(r.get("source_id") in source_ids for r in x.get("source_refs",[])) and x.get("authority_effect")=="none" for x in residue)
add("residue-reference-closure","PASS" if residue_ok else "BLOCK",f"{len(residue)} residue records including 2 unsupported former bridge claims")
child_runs={}
for cid,row in child_map.items():
 ok,code,out,out_hash,current=run_child(row); child_runs[cid]={"exit":code,"overall":out.get("overall"),"output_sha256":out_hash,"current_receipts":current}; add(f"child-validator-and-current-receipt:{cid}","PASS" if ok else "BLOCK",f"exit {code}, {out.get('overall')}, {current} current receipt, deterministic two-run output")
all_docs=[profile,sources_doc,definitions,documents,nodes_doc,relations_doc,views_doc,residue,migration]
add("authority-effect-none","PASS" if all(authority_none(x) for x in all_docs) else "BLOCK","no parent, child binding, model, residue, or migration record grants authority")
# Historical parent receipts stay immutable history and need not match the new bridge bytes.
history=[]; history_ok=True
for rp in sorted((PACKAGE/"receipts").glob("validation-*.json")):
 try:r=json.loads(rp.read_text())
 except Exception:history_ok=False;continue
 history.append(rp.name); history_ok &= r.get("package_id")=="cav2.define" and r.get("authority_effect")=="none" and r.get("status")=="pass"
add("historical-receipt-integrity","PASS" if history_ok else "BLOCK",f"{len(history)} immutable historical PASS receipts; none stretched over current bytes")
h=hashlib.sha256()
for rel in sorted(MATERIAL_FILES):h.update(rel.encode());h.update(b"\0");h.update((PACKAGE/rel).read_bytes());h.update(b"\0")
blocked=sum(x["outcome"]=="BLOCK" for x in checks); out={"schema_version":"cav2-define-validation/v2","package_id":"cav2.define","package_version":profile.get("package_version"),"overall":"PASS" if not blocked else "BLOCK","material_digest":h.hexdigest(),"summary":{"checks":len(checks),"passed":sum(x["outcome"]=="PASS" for x in checks),"blocked":blocked,"parent_nodes":len(local_nodes),"bridge_relations":len(rels),"views":len(views),"residue":len(residue),"source_drift":len(drift)},"child_runs":child_runs,"checks":checks,"blockers":[{"kind":"source-drift","source_ids":drift}] if drift else [],"authority_effect":"none","claim_ceiling":"Cross-package structure, source checks, and bridge traceability only; no child promotion, implementation, conformance, acceptance, execution, publication, release, deployment, migration, or external effect."}
print(json.dumps(out,indent=2,sort_keys=True));raise SystemExit(0 if not blocked else 1)
