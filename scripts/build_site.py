#!/usr/bin/env python3
"""Validate the canonical JSON and build the existing static lookup site."""

import argparse
import hashlib
import json
from pathlib import Path
import shutil


def build(source, output, sync_data=False):
    json_path = source / "advocatedata.json"
    records = json.loads(json_path.read_text(encoding="utf-8"))
    if not isinstance(records, list) or not records:
        raise ValueError("advocatedata.json must contain a nonempty array of records")
    fields = ("licenceNo", "name", "englishName", "address", "sex", "type", "issueDate")
    for index, record in enumerate(records, 1):
        if not isinstance(record, dict) or any(not isinstance(record.get(key), str) for key in fields):
            raise ValueError(f"Record {index} must contain all seven text fields")
        if not record["licenceNo"].strip() or not record["name"].strip():
            raise ValueError(f"Record {index} requires a licence number and name")

    # Retain every JSON field and the synchronous global used by index.html.
    data_script = (
        "/* Generated from advocatedata.json by scripts/build_site.py.\n"
        " * Edit the JSON source; GitHub Actions rebuilds the published data. */\n"
        "window.ADVOCATE_DATA = "
        + json.dumps(records, ensure_ascii=False, separators=(",", ":"))
        + ";\n"
    ).encode("utf-8")
    digest = hashlib.sha256(data_script).hexdigest()[:16]
    versioned_name = f"advocatedata.{digest}.js"
    html = (source / "index.html").read_bytes()
    script_tag = b'<script src="advocatedata.js"></script>'
    if html.count(script_tag) != 1:
        raise ValueError("index.html must load advocatedata.js exactly once")

    output.mkdir(parents=True, exist_ok=True)
    (output / "index.html").write_bytes(html.replace(
        script_tag, f'<script src="{versioned_name}"></script>'.encode("utf-8")
    ))
    (output / "advocatedata.js").write_bytes(data_script)
    (output / versioned_name).write_bytes(data_script)
    shutil.copyfile(json_path, output / json_path.name)
    (output / ".nojekyll").touch()
    if sync_data:
        (source / "advocatedata.js").write_bytes(data_script)
    print(f"Built {len(records):,} records; data asset: {versioned_name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path)
    parser.add_argument("--sync-data", action="store_true", help="Also refresh advocatedata.js for local/offline use")
    args = parser.parse_args()
    source = args.source.resolve()
    build(source, (args.output or source / "dist").resolve(), args.sync_data)
