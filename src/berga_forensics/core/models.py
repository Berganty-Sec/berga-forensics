"""Registros independentes das interfaces e da persistência."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Case:
    id: str
    name: str
    description: str
    created_at: str


@dataclass(frozen=True)
class Evidence:
    id: str
    case_id: str
    path: str
    source: str
    size: int
    sha256: str
    registered_at: str
