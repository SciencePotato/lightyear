import re
import types
import unittest
from pathlib import Path
from unittest.mock import patch


class ReadmeExampleTests(unittest.TestCase):
    def test_documented_app_constructs_and_route_receives_its_arguments(self):
        blocks = re.findall(r"```\n(.*?)```", (Path(__file__).parents[1] / "README.md").read_text(), re.S)
        helper = next(block for block in blocks if "def make_celery" in block)
        project = next(block for block in blocks if "app = Flask" in block)
        queued = []

        class Flask:
            def __init__(self, name):
                self.import_name = name
                self.config = {}
                self.routes = {}

            def route(self, path):
                def register(handler):
                    self.routes[path] = handler
                    return handler
                return register

        class Celery:
            Task = object

            def __init__(self, name, backend, broker):
                self.conf = {}
                self.backend = backend
                self.broker = broker

            def task(self, **kwargs):
                def register(handler):
                    handler.delay = lambda *args: queued.append(args)
                    return handler
                return register

        helper_module = types.ModuleType("celeryForProject")
        with patch.dict("sys.modules", {
            "celery": types.SimpleNamespace(Celery=Celery),
            "flask": types.SimpleNamespace(Flask=Flask),
            "celeryForProject": helper_module,
        }):
            exec(compile(helper, "celeryForProject.py", "exec"), helper_module.__dict__)
            namespace = {"__name__": "readme_example"}
            exec(compile(project, "project.py", "exec"), namespace)
        result = namespace["app"].routes["/<int:a>/<int:b>"](2, 3)
        self.assertIn("5", result)
        self.assertEqual(queued, [(2, 3)])
        self.assertEqual(namespace["celery"].backend, "rpc://")


if __name__ == "__main__":
    unittest.main()
