import argparse
import json
import os
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--q', help="Full-text search query")
    parser.add_argument('--category', help="Filter by category")
    parser.add_argument('--priority', help="Filter by priority")
    parser.add_argument('--status', help="Filter by status")
    parser.add_argument('--verification-status', help="Filter by verification status")
    parser.add_argument('--idea-foundry-fit', help="Filter by idea foundry fit")
    parser.add_argument('--golden-quill-relevance', help="Filter by golden quill relevance")
    parser.add_argument('--geography', help="Filter by geography")
    parser.add_argument('--limit', type=int, default=10, help="Limit number of results")
    parser.add_argument('--format', choices=['markdown', 'json'], default='markdown', help="Output format")
    parser.add_argument('--catalog', default='vault_shared/cached_opportunities/master_workbook.jsonl', help="Override JSONL path")
    args = parser.parse_args()

    if not os.path.exists(args.catalog):
        print(f"ERROR: Catalog not found at {args.catalog}", file=sys.stderr)
        exit(1)

    records = []
    with open(args.catalog, 'r') as f:
        for line in f:
            if not line.strip(): continue
            records.append(json.loads(line))

    results = []
    for r in records:
        if args.q:
            search_fields = [r.get('source_name'), r.get('funder_or_program'), r.get('category'), r.get('fit_summary'), r.get('notes'), r.get('use_cases')] + r.get('tags', [])
            search_text = " ".join([str(v) for v in search_fields if v]).lower()
            if args.q.lower() not in search_text:
                continue

        def match_field(field, arg_val):
            if not arg_val: return True
            val = r.get(field)
            if not val: return False
            return arg_val.lower() in str(val).lower()

        if not match_field('category', args.category): continue
        if not match_field('priority', args.priority): continue
        if not match_field('status', args.status): continue
        if not match_field('verification_status', args.verification_status): continue
        if not match_field('idea_foundry_fit', args.idea_foundry_fit): continue
        if not match_field('golden_quill_relevance', args.golden_quill_relevance): continue
        if not match_field('geography', args.geography): continue

        results.append(r)

    results = results[:args.limit]

    if args.format == 'json':
        print(json.dumps(results, indent=2))
    else:
        for i, r in enumerate(results, 1):
            print(f"### {i}. {r.get('source_name', 'Unnamed')}")
            print(f"- Category: {r.get('category', 'N/A')}")
            print(f"- Priority: {r.get('priority', 'N/A')}")
            print(f"- Status: {r.get('status', 'N/A')}")
            print(f"- Verification: {r.get('verification_status', 'N/A')}")
            print(f"- Golden Quill relevance: {r.get('golden_quill_relevance', 'N/A')}")
            print(f"- Idea Foundry fit: {r.get('idea_foundry_fit', 'N/A')}")
            print(f"- URL: {r.get('url', 'N/A')}")
            print(f"- Notes: {r.get('notes', 'N/A')}\n")

if __name__ == "__main__":
    main()
