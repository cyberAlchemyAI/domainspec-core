"""WPFA buyer-facing PDF emitter — Code phase realization. [§17.7]

Renders an operator-attested CycleReceipt to a brand-consistent PDF via
weasyprint (HTML→PDF). Always-local. PRE-emit gates fire before render.

This module realizes the Code-phase work for §17.7:

1. ``weasyprint_render`` — Jinja2 template binding + HTML→PDF conversion.
   Default callable lives in this module; tests may inject a stub.
2. ``scan_indirect_template_data`` — RT-C2-02 fold-in. Walks HTML text
   nodes + CSS ``content:`` property values + inline JS string literals
   on the rendered template against the classification register.
3. Three-layer defense (Layer 3 runtime gate):
   - F-WPFA-OPERATOR-SIGNATURE-MISSING
   - F-WPFA-PDF-CONFIDENTIAL-LEAK
   - F-WPFA-SPAN-PROVENANCE-MISSING.pdf_claim_unlinked

Layer 1 = R-WPFA-NO-AUTOSIGN AST-lint.
Layer 2 = Cedar policy ``cycle_receipt_operator_attestation``.
Layer 4 = TTY-gating at the ``tilth wpfa pdf emit`` CLI verb.
"""

from __future__ import annotations

import html as _html
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final, Iterable, Mapping, Optional

from pipeline.logician.gates.f_wpfa_operator_signature_missing import (
    check_f_wpfa_operator_signature_missing,
)
from pipeline.logician.gates.f_wpfa_pdf_confidential_leak import (
    check_f_wpfa_pdf_confidential_leak,
)
from pipeline.logician.gates.f_wpfa_span_provenance_missing import (
    check_pdf_claim_unlinked,
)
from pipeline.vault.sub_kinds.cycle_receipts import CycleReceipt


TEMPLATE_PATH: Final[Path] = (
    Path(__file__).parent / "templates" / "buyer_facing_pdf.html"
)

# Per §17.7.5 — every dollar/kWh claim in the PDF MUST link to a claim key
# present in span_provenance.per_claim_span_ids. These are the canonical
# claim keys the buyer-facing PDF template renders.
PDF_RENDERED_CLAIMS_V0_1: Final[tuple[str, ...]] = (
    "actual.dollars_total",
    "actual.watt_hours_total",
    "counterfactual.dollars_total",
    "counterfactual.watt_hours_total",
    "delta.dollars_saved",
    "delta.watt_hours_saved",
)


# ---------------------------------------------------------------------------
# Result + render context
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class PdfEmitResult:
    success: bool
    output_path: Optional[Path]
    failure_codes: tuple[str, ...]
    detail: str


@dataclass(frozen=True, kw_only=True)
class PdfRenderContext:
    """All values the Jinja2 template binds + the field-path map.

    ``rendered_field_paths`` is the explicit set of classification-register
    field paths the template renders (e.g., ``client.name``). Every entry
    is checked against the register PRE-emit. ``rendered_field_values`` is
    the value-side that the indirect-template-data scan compares against
    the register's known confidential value strings.
    """

    client_name: str
    operator_display_name: str
    signing_key_id_display: str
    methodology_url: str
    delta_dollars_display: str
    delta_kwh_display: str
    percent_local_display: str
    per_cycle_rows: tuple[Mapping[str, str], ...]
    rendered_field_paths: tuple[str, ...]
    # Confidential field-path → value pairs. The indirect scan uses these to
    # detect leakage where the template (or future template change) embeds
    # the literal value in CSS / static text / JS literal.
    confidential_value_strings: tuple[str, ...] = ()


# ---------------------------------------------------------------------------
# Indirect-template-data scan (RT-C2-02 fold-in, §17.7.6)
# ---------------------------------------------------------------------------


# CSS `content: "..."` and `content: '...'` patterns. Multiline OK; the
# weasyprint engine resolves `content:` into the final byte stream, so
# scanning the post-template HTML+CSS catches these.
_CSS_CONTENT_RE: Final[re.Pattern[str]] = re.compile(
    r"content\s*:\s*(?P<q>['\"])(?P<value>.*?)(?P=q)",
    re.DOTALL,
)
# Inline `<script>...</script>` blocks. Find any string literal embedded in
# JS source. Limited to single + double-quoted single-line strings; template
# literals (backticks) covered separately. Future template versions adding
# scripts are caught by this scan.
_JS_BLOCK_RE: Final[re.Pattern[str]] = re.compile(
    r"<script\b[^>]*>(?P<body>.*?)</script>",
    re.DOTALL | re.IGNORECASE,
)
_JS_STRING_LITERAL_RE: Final[re.Pattern[str]] = re.compile(
    r"(?P<q>['\"`])(?P<value>(?:\\.|(?!(?P=q)).)*)(?P=q)"
)
# Tag-stripper for HTML text-node extraction. Crude but adequate — we strip
# tags, then run the residual text through the value-string match.
_HTML_TAG_RE: Final[re.Pattern[str]] = re.compile(r"<[^>]+>", re.DOTALL)
_HTML_COMMENT_RE: Final[re.Pattern[str]] = re.compile(r"<!--.*?-->", re.DOTALL)


def _strip_tags(html_text: str) -> str:
    """Strip HTML tags + comments + script/style blocks; return text nodes."""
    body = _HTML_COMMENT_RE.sub(" ", html_text)
    # Strip <script>...</script> and <style>...</style> bodies entirely.
    body = re.sub(
        r"<script\b[^>]*>.*?</script>", " ", body, flags=re.DOTALL | re.IGNORECASE
    )
    body = re.sub(
        r"<style\b[^>]*>.*?</style>", " ", body, flags=re.DOTALL | re.IGNORECASE
    )
    body = _HTML_TAG_RE.sub(" ", body)
    return _html.unescape(body)


def scan_indirect_template_data(
    *,
    rendered_html: str,
    confidential_value_strings: Iterable[str],
) -> tuple[str, ...]:
    """Walk rendered HTML/CSS/JS for confidential-value leakage.

    Returns a tuple of confidential value strings found embedded in any of
    three indirect vectors:

    1. **HTML text nodes** — values bleed through ``{{ x | e }}`` despite
       Jinja2 escaping if the value itself IS a confidential string.
    2. **CSS ``content:`` declarations** — weasyprint resolves these to
       printed glyphs in the PDF.
    3. **Inline ``<script>`` JS string literals** — future template
       versions with scripts MUST be caught; v0.1 templates have none.

    A confidential value string is one whose classification-register entry
    is ``confidential`` AND whose textual value (e.g. an EIN, dollar
    figure, person name) might appear verbatim in the rendered template.
    The CLI/operator surfaces resolve register entries to value strings
    BEFORE invoking the emit.

    Pure-string search. No DOM parsing dep; the operator-controlled v0.1
    template is small enough that regex-and-strip is sufficient.
    """
    if not isinstance(rendered_html, str):
        raise TypeError(
            f"rendered_html must be str, got {type(rendered_html).__name__}"
        )
    confidential_values = {
        v.strip() for v in confidential_value_strings if isinstance(v, str) and v.strip()
    }
    if not confidential_values:
        return ()

    found: set[str] = set()

    # Vector 1: HTML text nodes (after stripping tags + style + script blocks)
    text_nodes = _strip_tags(rendered_html)
    for v in confidential_values:
        if v in text_nodes:
            found.add(v)

    # Vector 2: CSS content: '...' values inside <style> blocks AND inline
    # style attributes. Walk both.
    style_block_re = re.compile(
        r"<style\b[^>]*>(.*?)</style>", re.DOTALL | re.IGNORECASE
    )
    style_inline_re = re.compile(
        r"\bstyle\s*=\s*(['\"])(.*?)\1", re.DOTALL | re.IGNORECASE
    )
    css_haystacks: list[str] = []
    for m in style_block_re.finditer(rendered_html):
        css_haystacks.append(m.group(1))
    for m in style_inline_re.finditer(rendered_html):
        css_haystacks.append(m.group(2))
    for haystack in css_haystacks:
        for cm in _CSS_CONTENT_RE.finditer(haystack):
            literal = cm.group("value")
            for v in confidential_values:
                if v in literal:
                    found.add(v)

    # Vector 3: inline <script> JS string literals.
    for sm in _JS_BLOCK_RE.finditer(rendered_html):
        body = sm.group("body")
        for jm in _JS_STRING_LITERAL_RE.finditer(body):
            literal = jm.group("value")
            for v in confidential_values:
                if v in literal:
                    found.add(v)

    return tuple(sorted(found))


# ---------------------------------------------------------------------------
# Default weasyprint render callable
# ---------------------------------------------------------------------------


def default_weasyprint_render(
    *,
    receipt: CycleReceipt,
    context: PdfRenderContext,
    template_path: Path,
    output_path: Path,
) -> tuple[Path, str]:
    """Render via Jinja2 + weasyprint. Returns (output_path, rendered_html).

    The rendered HTML is returned so the caller can run the
    indirect-template-data scan AFTER render but BEFORE write_pdf — except
    weasyprint accepts an in-memory string, so we render once here and
    return the bytes. The scan runs against this string.
    """
    # Imports are lazy so the module remains importable on hosts that don't
    # have weasyprint installed (e.g., minimal test sandboxes). The CLI
    # surface depends on it; unit tests inject a stub.
    from jinja2 import Environment, FileSystemLoader, select_autoescape

    env = Environment(
        loader=FileSystemLoader(str(template_path.parent)),
        autoescape=select_autoescape(["html", "xml"]),
        keep_trailing_newline=False,
    )
    template = env.get_template(template_path.name)
    rendered_html = template.render(
        receipt=receipt,
        client_name=context.client_name,
        operator_display_name=context.operator_display_name,
        signing_key_id_display=context.signing_key_id_display,
        methodology_url=context.methodology_url,
        delta_dollars_display=context.delta_dollars_display,
        delta_kwh_display=context.delta_kwh_display,
        percent_local_display=context.percent_local_display,
        per_cycle_rows=context.per_cycle_rows,
    )
    return output_path, rendered_html


def _write_pdf_with_weasyprint(rendered_html: str, output_path: Path) -> None:
    """Convert rendered HTML to PDF via weasyprint. Lazy import."""
    from weasyprint import HTML  # type: ignore[import-not-found]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=rendered_html, base_url=str(TEMPLATE_PATH.parent)).write_pdf(
        target=str(output_path)
    )


# ---------------------------------------------------------------------------
# Top-level emit
# ---------------------------------------------------------------------------


def emit_buyer_facing_pdf(
    *,
    receipt: CycleReceipt,
    context: PdfRenderContext,
    output_dir: Path,
    classification_register: Optional[Mapping[str, str]],
    weasyprint_render: Optional[Any] = None,
    write_pdf: Optional[Any] = None,
) -> PdfEmitResult:
    """PRE-PDF-emit: three-layer defense + render + indirect-scan.

    ``weasyprint_render`` and ``write_pdf`` are dependency-injection seams
    for tests. Default values use the module-level callables.

    Order of operations (binding):
      1. Layer 3 Gate 1 — operator signature.
      2. Layer 3 Gate 2 — classification register confidential leak (explicit field paths).
      3. Layer 3 Gate 3 — PDF claim provenance.
      4. Render HTML via Jinja2.
      5. Indirect-template-data scan against confidential value strings.
      6. write_pdf via weasyprint.
    """
    failures: list[str] = []
    details: list[str] = []

    # Gate 1 — operator signature
    op_sig = check_f_wpfa_operator_signature_missing(
        signed_by_operator_ed25519=receipt.signed_by_operator_ed25519,
        target_artifact="pdf",
    )
    if not op_sig.success:
        failures.append(op_sig.failure_code or "F-WPFA-OPERATOR-SIGNATURE-MISSING")
        details.append(op_sig.detail)

    # Gate 2 — classification register confidential leak (explicit field paths)
    cl_leak = check_f_wpfa_pdf_confidential_leak(
        rendered_field_paths=context.rendered_field_paths,
        classification_register=classification_register,
    )
    if not cl_leak.success:
        failures.append(cl_leak.failure_code or "F-WPFA-PDF-CONFIDENTIAL-LEAK")
        details.append(cl_leak.detail)

    # Gate 3 — every rendered claim links to span_provenance
    sp_unlinked = check_pdf_claim_unlinked(
        pdf_rendered_claims=PDF_RENDERED_CLAIMS_V0_1,
        per_claim_span_ids=receipt.span_provenance.per_claim_span_ids,
    )
    if not sp_unlinked.success:
        failures.append(
            sp_unlinked.failure_code or "F-WPFA-SPAN-PROVENANCE-MISSING"
        )
        details.append(sp_unlinked.detail)

    if failures:
        return PdfEmitResult(
            success=False,
            output_path=None,
            failure_codes=tuple(failures),
            detail="; ".join(details),
        )

    # Render — Jinja2 binding
    out_path = output_dir / f"{receipt.cycle_id}.pdf"
    renderer = weasyprint_render or default_weasyprint_render
    try:
        result = renderer(
            receipt=receipt,
            context=context,
            template_path=TEMPLATE_PATH,
            output_path=out_path,
        )
    except Exception as exc:  # noqa: BLE001 — fail-closed
        return PdfEmitResult(
            success=False,
            output_path=None,
            failure_codes=("F-WPFA-PDF-RENDER-FAILED",),
            detail=f"render raised {type(exc).__name__}: {exc}",
        )

    # Renderer contract: returns (output_path, rendered_html). Permit a
    # legacy single-Path return for compatibility, but the scan REQUIRES
    # the rendered HTML.
    if (
        isinstance(result, tuple)
        and len(result) == 2
        and isinstance(result[1], str)
    ):
        out_path, rendered_html = result  # type: ignore[assignment]
    else:
        return PdfEmitResult(
            success=False,
            output_path=None,
            failure_codes=("F-WPFA-PDF-RENDER-FAILED",),
            detail=(
                "weasyprint_render contract violated — must return "
                "(output_path: Path, rendered_html: str). RT-C2-02 indirect "
                "scan requires the HTML byte stream."
            ),
        )

    # RT-C2-02 indirect-template-data scan (§17.7.6 Cycle 2 fold-in)
    leaked = scan_indirect_template_data(
        rendered_html=rendered_html,
        confidential_value_strings=context.confidential_value_strings,
    )
    if leaked:
        return PdfEmitResult(
            success=False,
            output_path=None,
            failure_codes=("F-WPFA-PDF-CONFIDENTIAL-LEAK",),
            detail=(
                f"indirect-template-data scan detected "
                f"{len(leaked)} confidential value string(s) embedded "
                f"in rendered HTML/CSS/JS (RT-C2-02 indirect_static_template_data): "
                f"{leaked[:5]!r}" + ("…" if len(leaked) > 5 else "")
            ),
        )

    # Write PDF via weasyprint
    writer = write_pdf or _write_pdf_with_weasyprint
    try:
        writer(rendered_html, out_path)
    except Exception as exc:  # noqa: BLE001 — fail-closed
        return PdfEmitResult(
            success=False,
            output_path=None,
            failure_codes=("F-WPFA-PDF-RENDER-FAILED",),
            detail=f"write_pdf raised {type(exc).__name__}: {exc}",
        )

    return PdfEmitResult(
        success=True,
        output_path=out_path,
        failure_codes=(),
        detail=f"PDF emitted to {out_path!s}",
    )


def build_pdf_render_context(
    *,
    receipt: CycleReceipt,
    client_name: str,
    operator_display_name: str,
    signing_key_id_display: str,
    methodology_url: str,
    grant_identifier: str = "—",
    confidential_value_strings: tuple[str, ...] = (),
) -> PdfRenderContext:
    """Helper to compose a PdfRenderContext from a CycleReceipt.

    Derives delta + percent displays from the receipt's integer fields per
    A12 Decimal discipline. Caller-provided ``client_name`` + display names
    are operator-controlled (white-glove configured).
    """
    delta_dollars_display = (
        f"{receipt.delta.dollars_saved_minor_units / 100:.2f}"
    )
    # micro-Wh → kWh: divide by 10^9
    delta_kwh_display = (
        f"{receipt.delta.watt_hours_saved_micro / 1_000_000_000:.3f}"
    )
    # percent local: tokens from is_local models / total tokens
    total_tokens = sum(
        m.input_tokens + m.output_tokens for m in receipt.actual_per_model
    )
    local_tokens = sum(
        m.input_tokens + m.output_tokens
        for m in receipt.actual_per_model
        if m.is_local
    )
    if total_tokens == 0:
        percent_local_display = "0"
    else:
        percent_local_display = f"{(local_tokens * 100) // total_tokens}"
    per_cycle_rows = (
        {
            "cycle_id": receipt.cycle_id,
            "grant_identifier": grant_identifier,
            "actual_dollars": f"${receipt.actual.dollars_total_minor_units / 100:.2f}",
            "counterfactual_dollars": (
                f"${receipt.counterfactual.dollars_total_minor_units / 100:.2f}"
            ),
            "delta_dollars": f"${receipt.delta.dollars_saved_minor_units / 100:.2f}",
            "trace_id_ref": (
                receipt.span_provenance.trace_ids[0]
                if receipt.span_provenance.trace_ids
                else "—"
            ),
        },
    )
    return PdfRenderContext(
        client_name=client_name,
        operator_display_name=operator_display_name,
        signing_key_id_display=signing_key_id_display,
        methodology_url=methodology_url,
        delta_dollars_display=delta_dollars_display,
        delta_kwh_display=delta_kwh_display,
        percent_local_display=percent_local_display,
        per_cycle_rows=per_cycle_rows,
        rendered_field_paths=(),
        confidential_value_strings=confidential_value_strings,
    )


__all__ = [
    "TEMPLATE_PATH",
    "PDF_RENDERED_CLAIMS_V0_1",
    "PdfEmitResult",
    "PdfRenderContext",
    "build_pdf_render_context",
    "default_weasyprint_render",
    "emit_buyer_facing_pdf",
    "scan_indirect_template_data",
]
