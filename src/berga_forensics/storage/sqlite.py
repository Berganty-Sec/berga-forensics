"""Persistência local usando a biblioteca padrão."""
import sqlite3
from pathlib import Path

from berga_forensics.core.models import Case, Evidence


class SQLiteStore:
    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(path)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON")
        self.connection.executescript("""
            CREATE TABLE IF NOT EXISTS cases (
                id TEXT PRIMARY KEY, name TEXT NOT NULL,
                description TEXT NOT NULL, created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS evidence (
                id TEXT PRIMARY KEY,
                case_id TEXT NOT NULL REFERENCES cases(id),
                path TEXT NOT NULL, source TEXT NOT NULL,
                size INTEGER NOT NULL, sha256 TEXT NOT NULL,
                registered_at TEXT NOT NULL
            );
        """)

    def close(self):
        self.connection.close()

    def add_case(self, case: Case):
        with self.connection:
            self.connection.execute(
                "INSERT INTO cases VALUES (?, ?, ?, ?)",
                (case.id, case.name, case.description, case.created_at),
            )

    def get_case(self, case_id: str) -> Case:
        row = self.connection.execute(
            "SELECT * FROM cases WHERE id = ?", (case_id,)
        ).fetchone()
        if row is None:
            raise ValueError(f"Caso não encontrado: {case_id}")
        return Case(**dict(row))

    def list_cases(self) -> list[Case]:
        return [Case(**dict(row)) for row in self.connection.execute(
            "SELECT * FROM cases ORDER BY created_at, id"
        )]

    def add_evidence(self, evidence: Evidence):
        with self.connection:
            self.connection.execute(
                "INSERT INTO evidence VALUES (?, ?, ?, ?, ?, ?, ?)",
                (evidence.id, evidence.case_id, evidence.path, evidence.source,
                 evidence.size, evidence.sha256, evidence.registered_at),
            )

    def list_evidence(self, case_id: str) -> list[Evidence]:
        self.get_case(case_id)
        return [Evidence(**dict(row)) for row in self.connection.execute(
            "SELECT * FROM evidence WHERE case_id = ? ORDER BY registered_at, id",
            (case_id,),
        )]
