#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


KIND_SCORE = {"instruction": 100, "target": 90, "caller": 80, "test": 75, "contract": 70, "golden": 60}


def slice_context(data):
    candidates = data.get("candidates", [])
    max_files = int(data.get("max_files", 8))
    max_lines = int(data.get("max_lines_per_file", 200))
    if max_files < 1 or max_lines < 1:
        raise ValueError("budgets must be positive")
    by_path = {}
    for item in candidates:
        path, reason = item.get("path"), item.get("reason")
        if not path or not str(reason or "").strip():
            raise ValueError("every candidate needs path and reason")
        if path in by_path:
            raise ValueError("candidate paths must be unique")
        by_path[path] = dict(item)
    expansions = data.get("expand", [])
    expanded = {}
    for item in expansions:
        if not item.get("path") or not str(item.get("reason", "")).strip():
            raise ValueError("every expansion requires path and reason")
        if item["path"] not in by_path:
            raise ValueError(f"expansion path is not a candidate: {item['path']}")
        if by_path[item["path"]].get("kind") == "unrelated":
            raise ValueError("unrelated files cannot be expanded; reclassify scope explicitly first")
        expanded[item["path"]] = item["reason"]
    required = [item for item in candidates if item.get("required") or item.get("mandatory")]
    if len(required) > max_files:
        raise ValueError("required items exceed file budget")
    eligible, deferred = [], []
    for item in candidates:
        kind, path = item.get("kind", "other"), item["path"]
        if kind == "generated" and not item.get("source"):
            raise ValueError("generated candidate requires source")
        if kind in {"generated", "unrelated"} and not item.get("required") and not item.get("mandatory"):
            deferred.append({**item, "disposition": "source-first" if kind == "generated" else "out-of-scope", "source_path": item.get("source")})
        else:
            score = int(item.get("score", KIND_SCORE.get(kind, 10)))
            eligible.append({**item, "score": score, "expansion_reason": expanded.get(path)})
    eligible.sort(key=lambda item: (not (item.get("required") or item.get("mandatory")), -item["score"], item["path"]))
    selected_raw = eligible[:max_files]
    expansion_items = []
    for path, reason in expanded.items():
        if path not in {item["path"] for item in selected_raw}:
            item = {**by_path[path], "score": int(by_path[path].get("score", KIND_SCORE.get(by_path[path].get("kind", "other"), 10))), "expansion_reason": reason}
            expansion_items.append(item)
    if len(selected_raw) + len(expansion_items) > max_files:
        raise ValueError("expansion exceeds file budget; increase max_files or explicitly remove context")
    selected_raw.extend(expansion_items)
    selected_paths = {item["path"] for item in selected_raw}
    deferred = [item for item in deferred if item["path"] not in selected_paths]
    for item in eligible[max_files:]:
        deferred.append({**item, "disposition": "budget"})
    selected = []
    for item in selected_raw:
        lines = int(item.get("lines", max_lines))
        if lines > max_lines and not item.get("ranges") and not item.get("symbols"):
            raise ValueError(f"{item['path']} exceeds line budget; provide ranges or symbols")
        selected.append({**item, "included_lines": min(lines, max_lines)})
    return {
        "selected": selected,
        "deferred": deferred,
        "expansions": [{"path": path, "reason": reason, "selected": path in selected_paths} for path, reason in expanded.items()],
        "budget": {"max_files": max_files, "max_lines_per_file": max_lines},
    }


def main():
    parser = argparse.ArgumentParser(description="Select a bounded context manifest")
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    data = json.loads(args.input.read_text(encoding="utf-8"))
    print(json.dumps(slice_context(data), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
