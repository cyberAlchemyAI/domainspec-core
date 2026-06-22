"""
Z-Rig Orchestrator CLI Entry Point

Usage:
    python -m zrig run --config run_config.json --task task_description.json [--output-dir ./runs]
    python -m zrig run --config run_config.json --task task_description.json --live
    python -m zrig validate --config run_config.json --task task_description.json
    python -m zrig classify --config run_config.json --task task_description.json
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import sys
import time
from pathlib import Path

from . import __version__, __spec_version__
from .config import Mode, RunConfig, TaskDescription, FamilyRegistry, ConfigValidationError
from .classifier import mode_select
from .pipeline import run_pipeline


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="zrig",
        description=f"Z-Rig Turbo v{__spec_version__} Pipeline Orchestrator (v{__version__})",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # --- run command ---
    run_parser = subparsers.add_parser("run", help="Execute a pipeline run")
    run_parser.add_argument("--config", required=True, help="Path to run_config.json")
    run_parser.add_argument("--task", required=True, help="Path to task_description.json")
    run_parser.add_argument("--registry", help="Path to family_registry.json (optional)")
    run_parser.add_argument("--output-dir", default=".", help="Output directory for run artifacts")
    run_parser.add_argument("--verbose", "-v", action="store_true", help="Verbose logging")
    run_parser.add_argument(
        "--live",
        action="store_true",
        help="Enable live agent dispatch via OpenClaw bridge (default: stub executor)",
    )

    # --- validate command ---
    val_parser = subparsers.add_parser("validate", help="Validate configuration files")
    val_parser.add_argument("--config", required=True, help="Path to run_config.json")
    val_parser.add_argument("--task", required=True, help="Path to task_description.json")

    # --- classify command ---
    cls_parser = subparsers.add_parser("classify", help="Classify task into mode")
    cls_parser.add_argument("--config", required=True, help="Path to run_config.json")
    cls_parser.add_argument("--task", required=True, help="Path to task_description.json")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Configure logging
    log_level = logging.DEBUG if getattr(args, "verbose", False) else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    if args.command == "run":
        return _cmd_run(args)
    elif args.command == "validate":
        return _cmd_validate(args)
    elif args.command == "classify":
        return _cmd_classify(args)
    else:
        parser.print_help()
        return 1


def _cmd_run(args: argparse.Namespace) -> int:
    """Execute a pipeline run."""
    try:
        run_config = RunConfig.from_file(args.config)
        task = TaskDescription.from_file(args.task)
    except ConfigValidationError as e:
        print(f"❌ Configuration validation failed:", file=sys.stderr)
        for err in e.errors:
            print(f"  • {err}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"❌ Failed to load configuration: {e}", file=sys.stderr)
        return 1

    registry = None
    if args.registry:
        try:
            registry = FamilyRegistry.from_file(args.registry)
        except Exception as e:
            print(f"❌ Failed to load registry: {e}", file=sys.stderr)
            return 1

    # Wire live executor when --live is set
    wave_executor = None
    if args.live:
        from .wave_prompts import WavePromptBuilder
        from .live_executor import LiveWaveExecutor

        run_dir = Path(args.output_dir) / run_config.run_id
        prompts = WavePromptBuilder(task, run_config)
        executor = LiveWaveExecutor(run_dir, prompts)
        wave_executor = executor

    print(f"🔧 Z-Rig Turbo v{__spec_version__} — Pipeline Orchestrator v{__version__}")
    print(f"📋 Run ID: {run_config.run_id}")
    print(f"🎯 Mode: {run_config.mode.value}")
    print(f"📁 Output: {args.output_dir}")

    if args.live:
        print(f"⚡ Live Mode: ENABLED — dispatching real agents via OpenClaw bridge")
    else:
        print(f"🧪 Dry-run Mode: using stub executor")

    print()

    start_time = time.monotonic()

    result = asyncio.run(run_pipeline(
        run_config=run_config,
        task=task,
        registry=registry,
        output_dir=args.output_dir,
        wave_executor=wave_executor,
    ))

    duration_s = time.monotonic() - start_time

    # Print result using run_summary if available
    from .run_summary import print_run_summary
    from .manifest import RunManifest

    # Try to load the manifest for a richer summary
    manifest_loaded = False
    if result.manifest_path:
        try:
            manifest_path = Path(result.manifest_path)
            run_dir = manifest_path.parent
            manifest = RunManifest.load(run_dir)
            print_run_summary(manifest, duration_s)
            manifest_loaded = True
        except Exception:
            pass

    if not manifest_loaded:
        # Fallback to the basic summary
        print()
        print("=" * 60)
        if result.status == "COMPLETED":
            print(f"✅ Pipeline COMPLETED — {result.run_id}")
        elif result.status == "HALTED":
            print(f"🛑 Pipeline HALTED — {result.run_id}")
            print(f"   Reason: {result.halt_reason}")
        elif result.status == "PAUSED":
            print(f"⏸️  Pipeline PAUSED — {result.run_id}")
            print(f"   Reason: {result.halt_reason}")
        else:
            print(f"❓ Pipeline {result.status} — {result.run_id}")

        print(f"   Mode: {result.mode}")
        print(f"   Waves completed: {len(result.waves_completed)}")
        print(f"   Waves failed: {len(result.waves_failed)}")
        if result.manifest_path:
            print(f"   Manifest: {result.manifest_path}")
        print("=" * 60)

    return 0 if result.status == "COMPLETED" else 1


def _cmd_validate(args: argparse.Namespace) -> int:
    """Validate configuration files."""
    errors: list[str] = []

    try:
        run_config = RunConfig.from_file(args.config)
        print(f"✅ run_config.json valid (run_id={run_config.run_id}, mode={run_config.mode.value})")
    except ConfigValidationError as e:
        errors.extend(e.errors)
        print(f"❌ run_config.json invalid:")
        for err in e.errors:
            print(f"  • {err}")
    except Exception as e:
        errors.append(str(e))
        print(f"❌ run_config.json error: {e}")

    try:
        task = TaskDescription.from_file(args.task)
        print(f"✅ task_description.json valid (task_id={task.task_id})")
    except ConfigValidationError as e:
        errors.extend(e.errors)
        print(f"❌ task_description.json invalid:")
        for err in e.errors:
            print(f"  • {err}")
    except Exception as e:
        errors.append(str(e))
        print(f"❌ task_description.json error: {e}")

    if errors:
        print(f"\n{len(errors)} validation error(s) found.")
        return 1
    print("\n✅ All configuration files valid.")
    return 0


def _cmd_classify(args: argparse.Namespace) -> int:
    """Classify task into mode."""
    try:
        run_config = RunConfig.from_file(args.config)
        task = TaskDescription.from_file(args.task)
    except ConfigValidationError as e:
        print(f"❌ Validation failed:", file=sys.stderr)
        for err in e.errors:
            print(f"  • {err}", file=sys.stderr)
        return 1

    result = mode_select(run_config, task)

    print(f"🎯 Mode Classification (MECH-003)")
    print(f"   Requested: {run_config.mode.value}")
    print(f"   Selected:  {result.selected_mode.value}")
    if result.recommended_mode is not None:
        print(f"   Recommended: {result.recommended_mode.value}")

    if result.advisory:
        print(f"   {result.advisory}")

    if result.auto_escalated:
        if run_config.mode == Mode.MICRO:
            print(f"   ⬆️  Auto-escalated from MICRO → {result.selected_mode.value}")
        elif run_config.mode == Mode.AUTO:
            print(f"   ⬆️  AUTO classification escalated to {result.selected_mode.value}")
        else:
            print(f"   ⬆️  Auto-escalated")
        print(f"   Reason: {result.escalation_reason}")

    if result.micro_result:
        mr = result.micro_result
        print(f"\n   MICRO_ELIGIBLE (MECH-031):")
        print(f"     eligible:         {mr.eligible}")
        for clause, ok in mr.all_clauses.items():
            symbol = "✅" if ok else "❌"
            print(f"     {symbol} {clause}: {ok}")
        if mr.failing_clauses:
            print(f"     Failing clauses:")
            for fc in mr.failing_clauses:
                print(f"       • {fc}")
        if mr.operator_override_applied:
            print(f"     ⚠️  Operator override applied")

    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
