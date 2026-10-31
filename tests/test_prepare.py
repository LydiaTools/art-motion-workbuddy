import hashlib
import importlib.util
import io
from contextlib import redirect_stderr
from pathlib import Path
import stat
import tempfile
import unittest
from unittest.mock import patch
from zipfile import ZipFile, ZipInfo

SCRIPT = Path(__file__).parents[1] / 'skills/art-motion-workbuddy/scripts/prepare.py'
spec = importlib.util.spec_from_file_location('art_motion_prepare', SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class PrepareTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.original_sha = module.SHA256

    def tearDown(self):
        module.SHA256 = self.original_sha
        self.tmp.cleanup()

    def package(self, extra=()):
        archive = self.root / 'example.zip'
        with ZipFile(archive, 'w') as z:
            z.writestr('art-motion-workbuddy/SKILL.md', 'example skill')
            z.writestr('art-motion-workbuddy/scripts/local_engine.py', 'example adapter')
            for name, content in extra:
                z.writestr(name, content)
        module.SHA256 = hashlib.sha256(archive.read_bytes()).hexdigest()
        return archive

    def test_matching_archive_prepares_only_new_target(self):
        archive = self.package([('art-motion-workbuddy/references/示例.md', 'hello')])
        target = self.root / 'runtime'
        result = module.prepare(archive, target)
        self.assertEqual(result['files'], 3)
        self.assertEqual((target / 'references/示例.md').read_text(), 'hello')
        (target / 'sentinel').write_text('keep')
        with self.assertRaises(FileExistsError):
            module.prepare(archive, target)
        self.assertEqual((target / 'sentinel').read_text(), 'keep')

    def test_wrong_hash_does_not_create_target(self):
        archive = self.package()
        module.SHA256 = '0' * 64
        target = self.root / 'runtime'
        with self.assertRaisesRegex(ValueError, 'SHA-256'):
            module.prepare(archive, target)
        self.assertFalse(target.exists())

    def test_path_traversal_and_case_collisions_are_rejected(self):
        for extra in [
            [('art-motion-workbuddy/../../outside', 'bad')],
            [('art-motion-workbuddy/a.txt', 'a'), ('art-motion-workbuddy/A.txt', 'b')],
        ]:
            with self.subTest(extra=extra):
                archive = self.package(extra)
                target = self.root / 'runtime'
                with self.assertRaises(ValueError):
                    module.prepare(archive, target)
                self.assertFalse(target.exists())
        self.assertFalse((self.root / 'outside').exists())

    def test_symbolic_link_is_rejected(self):
        link = ZipInfo('art-motion-workbuddy/link')
        link.create_system = 3
        link.external_attr = (stat.S_IFLNK | 0o777) << 16
        archive = self.package([(link, '../outside')])
        with self.assertRaisesRegex(ValueError, 'symbolic link'):
            module.prepare(archive, self.root / 'runtime')
        self.assertFalse((self.root / 'runtime').exists())

    def test_cli_checks_missing_parent_before_network(self):
        args = ['prepare.py', '--target', str(self.root / 'missing-parent' / 'runtime')]
        with patch.object(module.sys, 'argv', args), patch.object(module, 'download') as download, redirect_stderr(io.StringIO()):
            self.assertEqual(module.main(), 1)
        download.assert_not_called()


if __name__ == '__main__':
    unittest.main()
