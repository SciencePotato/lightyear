import os
from pathlib import Path
import subprocess
import tempfile
import unittest


class RunnerTests(unittest.TestCase):
    def test_runners_use_their_checkout_and_preserve_process_errors(self):
        source = Path(__file__).resolve().parents[1]
        for name, program in [
            ("listener_runner.sh", "listenerMain.py"),
            ("weekly_runner.sh", "weekly_writers_main.py"),
        ]:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                checkout = root / "checkout with spaces"
                (checkout / "venv" / "bin").mkdir(parents=True)
                (checkout / "venv" / "bin" / "activate").write_text(
                    'python3() { printf "%s\\n" "$PWD" "$@"; return 7; }\ndeactivate() { return 0; }\n'
                )
                script = checkout / name
                script.write_text((source / name).read_text())
                run = subprocess.run(
                    ["bash", str(script), "argument with spaces"],
                    cwd=root, env={**os.environ, "HOME": str(root)},
                    text=True, capture_output=True, timeout=5,
                )
                self.assertEqual(run.returncode, 7, run.stderr)
                self.assertEqual(run.stdout.splitlines(), [
                    str(checkout), program, *([] if name.startswith("listener") else ["argument with spaces"])
                ])


if __name__ == "__main__":
    unittest.main()
