"""Run the original pilot checks over a temporary, isolated Git snapshot."""
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent
CHECKS = ("append-only", "citations", "layer", "scope")


def safe_path(path):
    if not isinstance(path, str) or not path or "\\" in path or any(ord(c) < 32 or ord(c) == 127 for c in path):
        return False
    p = PurePosixPath(path)
    return not p.is_absolute() and str(p) == path and all(part not in (".", "..", ".git") for part in p.parts) and p.parts[0] == "instances" and len(p.parts) >= 4


def _run(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=30, check=True).stdout.strip()


def check_proposal(base_files, files, declared_scope, role="executor"):
    """Return named outcomes; infrastructure errors fail closed via exception.

    Neither proposed paths nor file contents are executed; a temporary repo is
    used solely because the original checks compare Git trees.
    """
    if not files or any(not safe_path(path) for path in (*base_files, *files, *declared_scope)):
        return {name: {"passed": False, "output": "Ruta inválida o propuesta vacía."} for name in CHECKS}
    with tempfile.TemporaryDirectory(prefix="apf-check-") as temp:
        root = Path(temp)
        _run(["git", "init", "-q"], root)
        _run(["git", "config", "user.name", "APF check"], root)
        _run(["git", "config", "user.email", "apf-check@invalid"], root)
        (root / "config").mkdir()
        (root / "config" / "layers.json").write_bytes((ROOT / "config" / "layers.json").read_bytes())
        for path, content in base_files.items():
            target = root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        _run(["git", "add", "--all"], root)
        _run(["git", "-c", "core.hooksPath=/dev/null", "commit", "-qm", "base", "--allow-empty"], root)
        base = _run(["git", "rev-parse", "HEAD"], root)
        for path, content in files.items():
            target = root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        _run(["git", "add", "--all"], root)
        _run(["git", "-c", "core.hooksPath=/dev/null", "commit", "-qm", "proposal", "--allow-empty"], root)
        head = _run(["git", "rev-parse", "HEAD"], root)
        body = root / "proposal-body.md"
        body.write_text("```apf-scope\n" + "\n".join(declared_scope) + "\n```\n", encoding="utf-8")
        results = {}
        for check in CHECKS:
            result = subprocess.run([sys.executable, str(ROOT / "scripts" / "pr_checks.py"),
                                     check, base, head, f"agent/{role}/local", str(body)],
                                    cwd=root, capture_output=True, text=True, timeout=30)
            # The original returns 1 for a red check. All other codes are errors.
            if result.returncode not in (0, 1) or (result.returncode == 1 and "RED " not in result.stdout):
                raise RuntimeError(f"Error ejecutando {check}: {result.stderr or result.stdout}")
            results[check] = {"passed": result.returncode == 0, "output": result.stdout.strip()}
        return results
