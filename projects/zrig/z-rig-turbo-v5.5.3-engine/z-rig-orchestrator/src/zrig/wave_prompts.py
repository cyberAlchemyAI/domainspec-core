"""Wave prompt templates for Z-Rig agent dispatch."""
from __future__ import annotations

import json
from typing import Any

from zrig.config import TaskDescription, RunConfig


class WavePromptBuilder:
    """Generates agent prompts for each Z-Rig wave."""

    def __init__(self, task: TaskDescription, run_config: RunConfig) -> None:
        self.task = task
        self.run_config = run_config

    def build_prompt(
        self, wave_id: str, role: str, seat_index: int, context: dict[str, Any],
        run_config: Any = None, manifest: Any = None,
    ) -> str:
        """Build full prompt for an agent in a given wave and role."""
        dispatch: dict[str, Any] = {
            "W1": self._w1_spec_prompt,
            "W2": self._w2_builder_prompt,
            "W3": self._w3_synthesis_prompt,
            "W4": self._w4_verifier_prompt,
            "W5": self._w5_redteam_prompt,
            "W5.5": self._w5_5_remediation_prompt,
            "W6": self._w6_consolidation_prompt,
            "W7": self._w7_deep_qa_prompt,
            "W8": self._w8_uat_prompt,
            "W9": self._w9_panel_prompt,
            "W10": self._w10_deploy_prompt,
            "W11": self._w11_sentinel_prompt,
        }
        builder_fn = dispatch.get(wave_id)
        if builder_fn is None:
            return self._generic_prompt(wave_id, role, context)
        return builder_fn(seat_index, context)

    # ------------------------------------------------------------------
    # Shared blocks
    # ------------------------------------------------------------------

    def _task_context_block(self) -> str:
        """Formats task summary, acceptance criteria, and target files."""
        criteria = "\n".join(f"- {c}" for c in self.task.acceptance_criteria)
        files = "\n".join(f"- {f}" for f in self.task.target_files)
        return (
            f"Task ID: {self.task.task_id}\n"
            f"Summary: {self.task.summary}\n"
            f"Requested Change: {self.task.requested_change}\n"
            f"Acceptance Criteria:\n{criteria}\n"
            f"Target Files:\n{files}\n"
            f"Artifact Type: {self.task.artifact_type}"
        )

    def _prior_wave_block(self, context: dict[str, Any], wave_ids: list[str]) -> str:
        """Extracts and serializes prior wave outputs."""
        prior = context.get("prior_waves", {})
        lines: list[str] = []
        for wid in wave_ids:
            if wid in prior:
                data = prior[wid]
                lines.append(f"=== Prior Wave {wid} Output ===")
                lines.append(json.dumps(data, indent=2))
                lines.append("")
        return "\n".join(lines) if lines else "No prior wave outputs available."

    def _output_schema_block(self, schema_desc: str) -> str:
        """Formats expected JSON output schema."""
        return f"OUTPUT SCHEMA (respond with ONLY this JSON structure):\n{schema_desc}"

    def _isolation_block(self) -> str:
        """Returns the isolation notice."""
        return (
            "ISOLATION NOTICE: You are working independently. "
            "Do not reference other agents, their outputs, or prior conversations. "
            "Your response must stand alone."
        )

    def _generic_prompt(self, wave_id: str, role: str, context: dict[str, Any]) -> str:
        """Fallback prompt for unknown waves."""
        task_block = self._task_context_block()
        isolation = self._isolation_block()
        return (
            f"You are {role} in a Z-Rig pipeline run.\n\n"
            f"{task_block}\n\n"
            f"Wave: {wave_id}\n"
            f"Seat Index: {context.get('seat_index', 0)}\n\n"
            f"{isolation}\n\n"
            f"Respond with ONLY the JSON object. No markdown, no explanation."
        )

    # ------------------------------------------------------------------
    # Wave-specific prompts
    # ------------------------------------------------------------------

    def _w1_spec_prompt(self, seat_index: int, context: dict[str, Any]) -> str:
        schema = json.dumps(
            {
                "requirements": ["string"],
                "failure_modes": ["string"],
                "rubric": {"dimension": "string"},
                "user_journeys": ["string"],
                "confidence": 0.0,
            },
            indent=2,
        )
        task_block = self._task_context_block()
        isolation = self._isolation_block()
        return (
            f"You are W1 Spec Planner (seat {seat_index}) in a Z-Rig pipeline run.\n\n"
            f"{task_block}\n\n"
            f"Wave W1 Instructions:\n"
            f"Produce a complete specification package for this task. "
            f"Define functional requirements, anticipated failure modes, "
            f"an evaluation rubric, and key user journeys.\n\n"
            f"{isolation}\n\n"
            f"{self._output_schema_block(schema)}\n\n"
            f"Respond with ONLY the JSON object. No markdown, no explanation."
        )

    def _w2_builder_prompt(self, seat_index: int, context: dict[str, Any]) -> str:
        schema = json.dumps(
            {
                "build_status": "success|partial|failed",
                "files": [{"path": "string", "content": "string"}],
                "residue": ["string"],
            },
            indent=2,
        )
        task_block = self._task_context_block()
        isolation = self._isolation_block()
        prior = self._prior_wave_block(context, ["W1"])
        return (
            f"You are W2 Builder (seat {seat_index}) in a Z-Rig pipeline run.\n\n"
            f"{task_block}\n\n"
            f"{prior}\n\n"
            f"Wave W2 Instructions:\n"
            f"Implement the requested change. Write complete, production-quality code "
            f"for all target files. Ensure every acceptance criterion is addressed. "
            f"Return all created or modified files with full content.\n\n"
            f"{isolation}\n\n"
            f"{self._output_schema_block(schema)}\n\n"
            f"Respond with ONLY the JSON object. No markdown, no explanation."
        )

    def _w3_synthesis_prompt(self, seat_index: int, context: dict[str, Any]) -> str:
        schema = json.dumps(
            {
                "primary_completed": True,
                "selection_basis": "string",
                "canonical_implementation": {"files": [{"path": "string", "content": "string"}]},
                "synthesis_confidence": 0.0,
                "residue": ["string"],
            },
            indent=2,
        )
        task_block = self._task_context_block()
        isolation = self._isolation_block()
        prior = self._prior_wave_block(context, ["W2"])
        return (
            f"You are W3 Synthesizer (seat {seat_index}) in a Z-Rig pipeline run.\n\n"
            f"{task_block}\n\n"
            f"{prior}\n\n"
            f"Wave W3 Instructions:\n"
            f"Compare all W2 builder outputs. Select the strongest implementation. "
            f"Produce a single canonical implementation that best satisfies the spec. "
            f"Document your selection rationale.\n\n"
            f"{isolation}\n\n"
            f"{self._output_schema_block(schema)}\n\n"
            f"Respond with ONLY the JSON object. No markdown, no explanation."
        )

    def _w4_verifier_prompt(self, seat_index: int, context: dict[str, Any]) -> str:
        schema = json.dumps(
            {
                "findings": [
                    {
                        "id": "string",
                        "severity": "critical|high|medium|low",
                        "description": "string",
                        "location": "string",
                    }
                ],
                "trace_matrix": {"criterion": "pass|fail"},
                "verification_confidence": 0.0,
            },
            indent=2,
        )
        task_block = self._task_context_block()
        isolation = self._isolation_block()
        prior = self._prior_wave_block(context, ["W3"])
        return (
            f"You are W4 Verifier (seat {seat_index}) in a Z-Rig pipeline run.\n\n"
            f"{task_block}\n\n"
            f"{prior}\n\n"
            f"Wave W4 Instructions:\n"
            f"Perform a rigorous verification of the canonical implementation against "
            f"the original task specification and acceptance criteria. "
            f"Produce a trace matrix and list all findings.\n\n"
            f"{isolation}\n\n"
            f"{self._output_schema_block(schema)}\n\n"
            f"Respond with ONLY the JSON object. No markdown, no explanation."
        )

    def _w5_redteam_prompt(self, seat_index: int, context: dict[str, Any]) -> str:
        schema = json.dumps(
            {
                "findings": ["string"],
                "attack_vectors_tested": ["string"],
                "overall_assessment": "string",
            },
            indent=2,
        )
        task_block = self._task_context_block()
        isolation = self._isolation_block()
        prior = self._prior_wave_block(context, ["W3", "W4"])
        return (
            f"You are W5 Red Team (seat {seat_index}) in a Z-Rig pipeline run.\n\n"
            f"{task_block}\n\n"
            f"{prior}\n\n"
            f"Wave W5 Instructions:\n"
            f"Conduct adversarial testing of the implementation. "
            f"Attempt to identify security, correctness, and robustness issues. "
            f"Document all attack vectors tested and resulting findings.\n\n"
            f"{isolation}\n\n"
            f"{self._output_schema_block(schema)}\n\n"
            f"Respond with ONLY the JSON object. No markdown, no explanation."
        )

    def _w5_5_remediation_prompt(self, seat_index: int, context: dict[str, Any]) -> str:
        schema = json.dumps(
            {
                "remediation_actions": [{"path": "string", "content": "string"}],
                "issues_addressed": ["string"],
                "remediation_status": "string",
            },
            indent=2,
        )
        task_block = self._task_context_block()
        isolation = self._isolation_block()
        prior = self._prior_wave_block(context, ["W5"])
        return (
            f"You are W5.5 Remediation (seat {seat_index}) in a Z-Rig pipeline run.\n\n"
            f"{task_block}\n\n"
            f"{prior}\n\n"
            f"Wave W5.5 Instructions:\n"
            f"Address all critical and high-severity findings from the red team. "
            f"Produce corrected implementation files. Document which issues were resolved.\n\n"
            f"{isolation}\n\n"
            f"{self._output_schema_block(schema)}\n\n"
            f"Respond with ONLY the JSON object. No markdown, no explanation."
        )

    def _w6_consolidation_prompt(self, seat_index: int, context: dict[str, Any]) -> str:
        schema = json.dumps(
            {
                "consolidated_findings": [
                    {
                        "id": "string",
                        "severity": "FATAL|critical|high|medium|low",
                        "description": "string",
                        "source_wave": "string",
                        "location": "string",
                    }
                ],
                "dedup_count": 0,
                "consolidation_confidence": 0.0,
            },
            indent=2,
        )
        task_block = self._task_context_block()
        isolation = self._isolation_block()
        prior = self._prior_wave_block(context, ["W4", "W5"])
        return (
            f"You are W6 Consolidator (seat {seat_index}) in a Z-Rig pipeline run.\n\n"
            f"{task_block}\n\n"
            f"{prior}\n\n"
            f"Wave W6 Instructions:\n"
            f"Merge and deduplicate all findings from W4 verification and W5 red team. "
            f"Produce a unified findings list with priority-ranked issues. "
            f"Each finding must retain its original source_wave and location.\n\n"
            f"{isolation}\n\n"
            f"{self._output_schema_block(schema)}\n\n"
            f"Respond with ONLY the JSON object. No markdown, no explanation."
        )

    def _w7_deep_qa_prompt(self, seat_index: int, context: dict[str, Any]) -> str:
        schema = json.dumps(
            {
                "qa_results": [
                    {
                        "finding_id": "string",
                        "confirmed": True,
                        "evidence": "string",
                        "severity_adjustment": "string",
                    }
                ],
                "false_positive_rate": 0.0,
                "qa_confidence": 0.0,
            },
            indent=2,
        )
        task_block = self._task_context_block()
        isolation = self._isolation_block()
        prior = self._prior_wave_block(context, ["W3", "W6"])
        return (
            f"You are W7 Deep QA Tester (seat {seat_index}) in a Z-Rig pipeline run.\n\n"
            f"{task_block}\n\n"
            f"{prior}\n\n"
            f"Wave W7 Instructions:\n"
            f"Perform deep testing of the canonical implementation (W3) against "
            f"the consolidated findings (W6). Independently verify each critical "
            f"finding is real and not a false positive. Provide evidence for each result.\n\n"
            f"{isolation}\n\n"
            f"{self._output_schema_block(schema)}\n\n"
            f"Respond with ONLY the JSON object. No markdown, no explanation."
        )

    def _w8_uat_prompt(self, seat_index: int, context: dict[str, Any]) -> str:
        schema = json.dumps(
            {
                "journey_results": [{"journey": "string", "status": "pass|fail", "notes": "string"}],
                "overall_pass": True,
                "findings": ["string"],
            },
            indent=2,
        )
        task_block = self._task_context_block()
        isolation = self._isolation_block()
        prior = self._prior_wave_block(context, ["W3", "W5.5"])
        return (
            f"You are W8 UAT Tester (seat {seat_index}) in a Z-Rig pipeline run.\n\n"
            f"{task_block}\n\n"
            f"{prior}\n\n"
            f"Wave W8 Instructions:\n"
            f"Execute all defined user journeys against the implementation. "
            f"Report pass/fail status and any observations for each journey.\n\n"
            f"{isolation}\n\n"
            f"{self._output_schema_block(schema)}\n\n"
            f"Respond with ONLY the JSON object. No markdown, no explanation."
        )

    def _w9_panel_prompt(self, seat_index: int, context: dict[str, Any]) -> str:
        schema = json.dumps(
            {
                "vote": "ACCEPT|REVISE|REJECT",
                "score": 0,
                "justification": "string",
                "critical_findings": ["string"],
                "residue": ["string"],
            },
            indent=2,
        )
        task_block = self._task_context_block()
        isolation = self._isolation_block()
        prior = self._prior_wave_block(context, ["W3", "W4", "W5.5", "W8"])
        return (
            f"You are W9 Panelist (seat {seat_index}) in a Z-Rig pipeline run.\n\n"
            f"{task_block}\n\n"
            f"{prior}\n\n"
            f"Wave W9 Instructions:\n"
            f"Review the complete artifact package. Cast a vote of ACCEPT, REVISE, or REJECT. "
            f"Provide a numeric score (0-100) and detailed justification.\n\n"
            f"{isolation}\n\n"
            f"{self._output_schema_block(schema)}\n\n"
            f"Respond with ONLY the JSON object. No markdown, no explanation."
        )

    def _w10_deploy_prompt(self, seat_index: int, context: dict[str, Any]) -> str:
        schema = json.dumps(
            {
                "deployment_actions": [
                    {"action": "write|delete|chmod", "path": "string", "content": "string"}
                ],
                "status": "success|partial|failed",
            },
            indent=2,
        )
        task_block = self._task_context_block()
        isolation = self._isolation_block()
        prior = self._prior_wave_block(context, ["W3", "W9"])
        return (
            f"You are W10 Deployer (seat {seat_index}) in a Z-Rig pipeline run.\n\n"
            f"{task_block}\n\n"
            f"{prior}\n\n"
            f"Wave W10 Instructions:\n"
            f"Execute the final deployment. Write all approved files to their target locations. "
            f"Report every action taken and final deployment status.\n\n"
            f"{isolation}\n\n"
            f"{self._output_schema_block(schema)}\n\n"
            f"Respond with ONLY the JSON object. No markdown, no explanation."
        )

    def _w11_sentinel_prompt(self, seat_index: int, context: dict[str, Any]) -> str:
        schema = json.dumps(
            {
                "sentinel_status": "healthy|degraded|failed",
                "findings": ["string"],
                "regression_detected": False,
            },
            indent=2,
        )
        task_block = self._task_context_block()
        isolation = self._isolation_block()
        prior = self._prior_wave_block(context, ["W10"])
        return (
            f"You are W11 Sentinel (seat {seat_index}) in a Z-Rig pipeline run.\n\n"
            f"{task_block}\n\n"
            f"{prior}\n\n"
            f"Wave W11 Instructions:\n"
            f"Perform post-deployment health verification. "
            f"Confirm no regressions were introduced and the system is operating correctly.\n\n"
            f"{isolation}\n\n"
            f"{self._output_schema_block(schema)}\n\n"
            f"Respond with ONLY the JSON object. No markdown, no explanation."
        )