"""Operações de casos e registro de arquivos."""
import hashlib
import os
import stat
from datetime import datetime, timezone
from pathlib import Path
from typing import Protocol
from uuid import uuid4

from berga_forensics.core.models import Case, Evidence


class Store(Protocol):
    def add_case(self, case: Case) -> None: ...
    def get_case(self, case_id: str) -> Case: ...
    def list_cases(self) -> list[Case]: ...
    def add_evidence(self, evidence: Evidence) -> None: ...
    def list_evidence(self, case_id: str) -> list[Evidence]: ...


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


class ForensicsService:
    def __init__(self, store: Store):
        self.store = store

    def create_case(self, name: str, description: str = "") -> Case:
        name = name.strip()
        if not name:
            raise ValueError("O nome do caso não pode estar vazio.")
        case = Case(str(uuid4()), name, description, timestamp())
        self.store.add_case(case)
        return case

    def register_evidence(self, case_id: str, path: Path, source: str = "") -> Evidence:
        self.store.get_case(case_id)
        path = path.resolve(strict=True)
        if not path.is_file():
            raise ValueError("A evidência deve ser um arquivo regular.")
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            before = os.fstat(stream.fileno())
            if not stat.S_ISREG(before.st_mode):
                raise ValueError("A evidência deve ser um arquivo regular.")
            size = 0
            while chunk := stream.read(1024 * 1024):
                digest.update(chunk)
                size += len(chunk)
            after = os.fstat(stream.fileno())
        current = path.stat()
        def signature(value):
            return (value.st_dev, value.st_ino, value.st_size,
                    value.st_mtime_ns, value.st_ctime_ns)
        if signature(before) != signature(after) or signature(after) != signature(current) or size != after.st_size:
            raise ValueError("O arquivo mudou durante a leitura; registro cancelado.")
        evidence = Evidence(str(uuid4()), case_id, str(path), source,
                            size, digest.hexdigest(), timestamp())
        self.store.add_evidence(evidence)
        return evidence
