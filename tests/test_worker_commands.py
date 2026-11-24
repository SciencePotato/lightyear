import re
import unittest
from pathlib import Path


class WorkerCommandTests(unittest.TestCase):
    def test_standalone_recipe_worker_imports_the_module_the_recipe_creates(self):
        readme = Path(__file__).resolve().parents[1].joinpath("README.md").read_text()
        module = re.search(r"Create `(\w+)\.py` containing:\s*\n\s*```\s*\nfrom celeryForProject", readme).group(1)
        targets = re.findall(r"celery -A ([\w.]+) worker", readme)
        self.assertTrue(targets)
        self.assertEqual(targets, [f"{module}.celery"] * len(targets))


if __name__ == "__main__":
    unittest.main()
