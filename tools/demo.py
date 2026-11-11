"""Run the web app on the sample vault in demo/, in a throwaway folder. Your own vault, raw/ and data/ are not touched.

    ./demo            # http://127.0.0.1:8766
"""
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.kb import sandbox  # noqa: E402


def main():
    port = os.environ.get("KB_PORT", "8766")
    with tempfile.TemporaryDirectory(prefix="kb-demo-") as tmp:
        root = sandbox.build(Path(tmp) / "kb")
        env = {**os.environ, "KB_PORT": port}
        subprocess.run([sys.executable, "-m", "tools.kb", "build"], cwd=root, env=env, check=True)
        print(f"\nDemo running on the sample vault: http://127.0.0.1:{port}\nEverything you change is discarded when you stop it (Ctrl+C).\n")
        try:
            subprocess.run([sys.executable, "-m", "app.server"], cwd=root, env=env)
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
