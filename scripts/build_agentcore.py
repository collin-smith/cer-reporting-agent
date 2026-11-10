"""Build the AgentCore Runtime zip (article 7, D55): one package, two Runtimes, two entry files at its root.

    agent_main.py   the reviewing agent behind the Runtime's HTTP contract (cer_agent.runtime)
    tools_main.py   the MCP server's public tools, stateless streamable HTTP (cer_agent.mcp_server --http)

AgentCore Runtime runs arm64 Linux only, so the dependencies are downloaded as manylinux aarch64 wheels by uv, at the
versions installed in this venv (the versions every eval ran on). The code keeps the repo's layout (src/cer_agent next
to docs/rules-spec.md), because agent.py finds the rules spec by its path in the repo. Files are 644 and directories
755, as the Runtime requires; no __pycache__.

Usage (from code/, needs uv and PyPI):  .venv/bin/python scripts/build_agentcore.py  ->  infra/build/agentcore.zip
"""

from __future__ import annotations

import importlib.metadata as md
import pathlib
import shutil
import subprocess
import sys
import zipfile

CODE = pathlib.Path(__file__).resolve().parents[1]
BUILD = CODE / "infra/build"
DEPS = BUILD / "agentcore-deps"
OUT = BUILD / "agentcore.zip"
PYTHON = "3.14"  # PYTHON_3_14 on the Runtime, the venv's version
TOP = ["boto3", "botocore", "strands-agents", "mcp"]  # runtime deps, botocore pinned too; uvicorn and starlette via mcp
FIXED = (2026, 1, 1, 0, 0, 0)
LIMIT_MB = 250  # the Runtime's zipped limit (750 MB unzipped)

ENTRY = '''"""AgentCore Runtime entry point (scripts/build_agentcore.py): {what}."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))
{body}
'''
ENTRIES = {
    "agent_main.py": ENTRY.format(what="the reviewing agent, HTTP on :8080",
                                  body="from cer_agent.runtime import main\n\nsys.exit(main())"),
    "tools_main.py": ENTRY.format(what="the MCP server's public tools, streamable HTTP on :8000/mcp",
                                  body="from cer_agent.mcp_server import build, serve_http\n\nserve_http(build())"),
}  # fmt: skip


def pins() -> list[str]:
    return [f"{p}=={md.version(p)}" for p in TOP]


def download() -> None:
    if DEPS.exists():
        shutil.rmtree(DEPS)
    cmd = ["uv", "pip", "install", "--python-platform", "aarch64-manylinux2014", "--python-version", PYTHON,
           "--target", str(DEPS), "--only-binary=:all:", "--quiet", *pins()]  # fmt: skip
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)


def _add(zf: zipfile.ZipFile, arcname: str, data: bytes) -> None:
    info = zipfile.ZipInfo(arcname, FIXED)
    info.external_attr = 0o100644 << 16  # a regular file, rw-r--r--
    info.compress_type = zipfile.ZIP_DEFLATED
    zf.writestr(info, data)


def files() -> list[tuple[str, bytes]]:
    out = [(name, text.encode()) for name, text in ENTRIES.items()]
    out += [(f"src/cer_agent/{p.name}", p.read_bytes()) for p in sorted((CODE / "src/cer_agent").glob("*.py"))]
    out.append(("docs/rules-spec.md", (CODE / "docs/rules-spec.md").read_bytes()))
    for p in sorted(DEPS.rglob("*")):
        if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc":
            out.append((p.relative_to(DEPS).as_posix(), p.read_bytes()))
    return out


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if "--no-download" not in argv:
        download()
    BUILD.mkdir(parents=True, exist_ok=True)
    items = files()
    with zipfile.ZipFile(OUT, "w") as zf:
        for arc, data in sorted(items):
            _add(zf, arc, data)
    mb = OUT.stat().st_size / 1e6
    print(f"{OUT} ({mb:.1f} MB, {len(items)} files; pins {', '.join(pins())})")
    if mb > LIMIT_MB:
        print(f"over the Runtime's {LIMIT_MB} MB zipped limit", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
