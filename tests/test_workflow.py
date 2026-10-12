import hashlib
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path
from unittest.mock import patch

from berga_forensics.cli.main import main
from berga_forensics.core.service import ForensicsService
from berga_forensics.storage.sqlite import SQLiteStore


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.db = self.root / 'cases.sqlite3'
        self.store = SQLiteStore(self.db)
        self.addCleanup(self.store.close)
        self.service = ForensicsService(self.store)
        self.file = self.root / 'evidence.bin'
        self.file.write_bytes(b'abc')

    def test_hash_and_persistence(self):
        case = self.service.create_case('Caso de teste', 'Descrição')
        item = self.service.register_evidence(case.id, self.file, 'Coleta local')
        self.assertEqual(item.sha256, hashlib.sha256(b'abc').hexdigest())
        self.assertEqual(item.size, 3)
        self.assertEqual(self.file.read_bytes(), b'abc')
        other = SQLiteStore(self.db)
        try:
            self.assertEqual(other.list_cases(), [case])
            self.assertEqual(other.list_evidence(case.id), [item])
        finally:
            other.close()

    def test_invalid_inputs_do_not_register(self):
        with self.assertRaises(ValueError):
            self.service.create_case('  ')
        with self.assertRaises(ValueError):
            self.service.register_evidence('missing', self.file)
        case = self.service.create_case('Teste')
        with self.assertRaises(FileNotFoundError):
            self.service.register_evidence(case.id, self.root / 'missing')
        with self.assertRaises(ValueError):
            self.service.register_evidence(case.id, self.root)
        self.assertEqual(self.store.list_evidence(case.id), [])

    def test_change_during_hash_cancels_registration(self):
        case = self.service.create_case('Teste')
        real_sha256 = hashlib.sha256
        file = self.file
        class ChangingDigest:
            def __init__(self):
                self.digest = real_sha256()
            def update(self, chunk):
                self.digest.update(chunk)
                file.write_bytes(b'changed')
            def hexdigest(self):
                return self.digest.hexdigest()
        with patch('berga_forensics.core.service.hashlib.sha256', ChangingDigest):
            with self.assertRaisesRegex(ValueError, 'mudou'):
                self.service.register_evidence(case.id, self.file)
        self.assertEqual(self.store.list_evidence(case.id), [])

    def command(self, *args):
        output = io.StringIO()
        errors = io.StringIO()
        with redirect_stdout(output), redirect_stderr(errors):
            status = main(['--db', str(self.db), *args])
        return status, output.getvalue(), errors.getvalue()

    def test_cli_workflow(self):
        status, output, _ = self.command('case', 'create', 'Investigação')
        self.assertEqual(status, 0)
        case_id = json.loads(output)['id']
        status, output, _ = self.command('evidence', 'add', str(self.file), '--case', case_id)
        self.assertEqual(status, 0)
        evidence_id = json.loads(output)['id']
        status, output, _ = self.command('evidence', 'list', '--case', case_id)
        self.assertEqual(status, 0)
        self.assertEqual(json.loads(output)[0]['id'], evidence_id)
        status, _, error = self.command('evidence', 'list', '--case', 'missing')
        self.assertEqual(status, 1)
        self.assertIn('Caso não encontrado', error)


if __name__ == '__main__':
    unittest.main()
