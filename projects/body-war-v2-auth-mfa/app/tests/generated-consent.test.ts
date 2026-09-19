import { test } from "node:test";
import assert from "node:assert/strict";
import { evidenceConsentRequired } from "../src/compiled/generated/src/domainspec/typescript/body-war-pilot/evidence-consent-required.js";

test("compiled consent rule rejects every incomplete boolean combination", () => {
  for (let mask=0;mask<8;mask++) {
    const result=evidenceConsentRequired({consent_acknowledged:Boolean(mask&1),activity_present:Boolean(mask&2),consent_text_present:Boolean(mask&4)});
    assert.equal(result,mask===7,`combination ${mask}`);
  }
});
test("compiled rule refuses missing consent input",()=>{
 assert.throws(()=>evidenceConsentRequired({activity_present:true,consent_text_present:true}),/missing Rule parameter/);
});
