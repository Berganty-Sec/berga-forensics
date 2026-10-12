"""Ponto de entrada da CLI."""
import argparse
import json
import sqlite3
import sys
from dataclasses import asdict
from pathlib import Path

from berga_forensics import __version__
from berga_forensics.core.service import ForensicsService
from berga_forensics.storage.sqlite import SQLiteStore


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="bf", description="Berga Forensics — investigação digital.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("--db", type=Path, default=Path("data/berga.sqlite3"),
                        help="Banco local (padrão: data/berga.sqlite3)")
    groups = parser.add_subparsers(dest="group")
    cases = groups.add_parser("case", help="Gerenciar casos").add_subparsers(dest="action", required=True)
    create = cases.add_parser("create", help="Criar caso")
    create.add_argument("name")
    create.add_argument("--description", default="")
    cases.add_parser("list", help="Listar casos")
    evidence = groups.add_parser("evidence", help="Registrar evidências").add_subparsers(dest="action", required=True)
    add = evidence.add_parser("add", help="Registrar arquivo e calcular SHA-256")
    add.add_argument("path", type=Path)
    add.add_argument("--case", required=True, dest="case_id")
    add.add_argument("--source", default="", help="Origem do arquivo")
    listing = evidence.add_parser("list", help="Listar evidências do caso")
    listing.add_argument("--case", required=True, dest="case_id")
    args = parser.parse_args(argv)
    if args.group is None:
        parser.print_help()
        return 0
    store = None
    try:
        store = SQLiteStore(args.db)
        service = ForensicsService(store)
        if args.group == "case":
            result = (asdict(service.create_case(args.name, args.description))
                      if args.action == "create" else [asdict(case) for case in store.list_cases()])
        else:
            result = (asdict(service.register_evidence(args.case_id, args.path, args.source))
                      if args.action == "add" else [asdict(item) for item in store.list_evidence(args.case_id)])
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, sqlite3.Error) as error:
        print(f"Erro: {error}", file=sys.stderr)
        return 1
    finally:
        if store is not None:
            store.close()
