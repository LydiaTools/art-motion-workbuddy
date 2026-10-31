import contextlib
import importlib.util
import io
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).parents[1] / 'scripts/local_engine.py'
spec = importlib.util.spec_from_file_location('local_engine', SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class EncoderGuardTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.skill = self.root / 'skill'
        self.source = self.skill / 'upstream/scripts/engine'
        self.source.mkdir(parents=True)
        for page in ('index.html', 'clip.html'):
            (self.source / page).write_text('<head></head>', encoding='utf-8')

    def tearDown(self):
        self.tmp.cleanup()

    def test_late_encoder_failure_is_nonzero_and_hides_no_success(self):
        render = self.source / 'render.py'
        render.write_text('import subprocess, sys\nfrom pathlib import Path\n'
            'vid = sys.argv[1]\n'
            'ff = subprocess.Popen([sys.executable, "-c", "import sys; sys.stdin.buffer.read(); sys.exit(17)"], stdin=subprocess.PIPE)\n'
            'if True:\n        ff.stdin.close(); ff.wait()\n        print("done")\n', encoding='utf-8')
        with patch.object(module, 'SKILL', self.skill), contextlib.redirect_stdout(io.StringIO()):
            module.init(self.root / 'project')
        installed = self.root / 'project/production/engine/render.py'
        result = subprocess.run([sys.executable, str(installed), str(self.root / 'out.mp4')], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('FFmpeg failed with exit code 17', result.stderr)
        self.assertNotIn('done', result.stdout)

    def test_unknown_renderer_is_refused_before_creating_project(self):
        (self.source / 'render.py').write_text('print("unknown")\n', encoding='utf-8')
        project = self.root / 'project'
        with patch.object(module, 'SKILL', self.skill):
            with self.assertRaisesRegex(RuntimeError, 'Unsupported upstream renderer'):
                module.init(project)
        self.assertFalse(project.exists())

    def test_zero_byte_output_is_not_reported_as_success(self):
        render = self.source / 'render.py'
        render.write_text('import subprocess, sys\nfrom pathlib import Path\n'
            'vid = sys.argv[1]\nPath(vid).touch()\n'
            'ff = subprocess.Popen([sys.executable, "-c", "import sys; sys.stdin.buffer.read()"], stdin=subprocess.PIPE)\n'
            'if True:\n        ff.stdin.close(); ff.wait()\n        print("done")\n', encoding='utf-8')
        with patch.object(module, 'SKILL', self.skill), contextlib.redirect_stdout(io.StringIO()):
            module.init(self.root / 'project')
        installed = self.root / 'project/production/engine/render.py'
        result = subprocess.run([sys.executable, str(installed), str(self.root / 'out.mp4')], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('FFmpeg produced no video output', result.stderr)
        self.assertNotIn('done', result.stdout)


if __name__ == '__main__':
    unittest.main()
