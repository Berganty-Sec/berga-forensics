# Testes

Execute `PYTHONPATH=src python3 -m unittest discover -s tests -v`.

Os testes usam diretórios temporários e verificam persistência, SHA-256,
entradas inválidas, alteração durante leitura e o fluxo pela CLI.
