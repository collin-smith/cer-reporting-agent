"""Build the approval Lambda's zip (article 6, D51): the cer_agent package plus the OpenTelemetry API it imports
(tracing is a no-op unless set up). boto3 comes with the Lambda runtime.

Usage (from code/):  .venv/bin/python scripts/build_lambda.py   ->  infra/build/approval.zip

The zip is built from the venv's installed packages (pure Python), so no download is needed. Entry metadata is
fixed, so the same sources give the same zip and Terraform's source_code_hash only changes when the code does.
"""

from __future__ import annotations

import pathlib
import sys
import sysconfig
import zipfile

CODE = pathlib.Path(__file__).resolve().parents[1]
OUT = CODE / "infra/build/approval.zip"
MODULES = ["__init__", "approval", "drafter", "extract", "rules", "tracing", "workflow"]
FIXED = (2026, 1, 1, 0, 0, 0)
SKIP = {"sdk", "instrumentation", "semconv", "__pycache__"}  # the API only


def _add(zf: zipfile.ZipFile, path: pathlib.Path, arcname: str):
    info = zipfile.ZipInfo(arcname, FIXED)
    info.external_attr = 0o644 << 16
    info.compress_type = zipfile.ZIP_DEFLATED
    zf.writestr(info, path.read_bytes())


def main() -> int:
    site = pathlib.Path(sysconfig.get_paths()["purelib"])
    otel = [d for d in sorted((site / "opentelemetry").iterdir()) if d.is_dir() and d.name not in SKIP]
    deps = [*otel, site / "typing_extensions.py", *site.glob("opentelemetry_api-*.dist-info"),
            *site.glob("typing_extensions-*.dist-info")]  # fmt: skip
    OUT.parent.mkdir(parents=True, exist_ok=True)
    files = [(CODE / f"src/cer_agent/{m}.py", f"cer_agent/{m}.py") for m in MODULES]
    for d in deps:
        if not d.exists():
            print(f"missing {d}", file=sys.stderr)
            return 1
        items = [d] if d.is_file() else sorted(p for p in d.rglob("*") if p.is_file() and "__pycache__" not in p.parts)
        files += [(p, p.relative_to(site).as_posix()) for p in items]
    with zipfile.ZipFile(OUT, "w") as zf:
        for path, arc in sorted(files, key=lambda x: x[1]):
            _add(zf, path, arc)
    print(f"{OUT} ({OUT.stat().st_size // 1024} KB, {len(files)} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
