#!/usr/bin/env python
"""Pre-flight check. Verifies the environment before a multi-day run starts."""
import _bootstrap  # noqa: F401
import importlib
import json
import sys


def main() -> int:
    report = {"python": sys.version.split()[0], "ok": True, "checks": {}}

    def check(name, fn):
        try:
            report["checks"][name] = fn()
        except Exception as e:
            report["checks"][name] = f"FAIL: {e}"
            report["ok"] = False

    check("numpy", lambda: importlib.import_module("numpy").__version__)
    check("scipy", lambda: importlib.import_module("scipy").__version__)
    check("pandas", lambda: importlib.import_module("pandas").__version__)
    check("statsmodels", lambda: importlib.import_module("statsmodels").__version__)
    check("PIL", lambda: importlib.import_module("PIL").__version__)
    check("matplotlib", lambda: importlib.import_module("matplotlib").__version__)
    check("guiprim", lambda: importlib.import_module("guiprim").__version__)

    def torch_check():
        t = importlib.import_module("torch")
        return {"version": t.__version__, "cuda": t.cuda.is_available(),
                "n_gpu": t.cuda.device_count() if t.cuda.is_available() else 0}
    try:
        report["checks"]["torch"] = torch_check()
    except Exception as e:
        report["checks"]["torch"] = f"absent ({e}) - fine for pure-python parts"

    print(json.dumps(report, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
