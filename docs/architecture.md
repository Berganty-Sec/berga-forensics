# Arquitetura inicial

O projeto começa pelo terminal. A futura interface web reutilizará a lógica
de negócio, sem depender do código da CLI.

- `cli`: interpreta argumentos, chama operações e apresenta resultados.
- `core`: define casos, evidências e regras de negócio.
- `analyzers`: extrai e interpreta dados das evidências.
- `storage`: implementa persistência dos dados.
- `reports`: transforma resultados em relatórios.

O núcleo não deve importar a CLI nem depender de um framework web.
Analisadores devem retornar resultados estruturados, sem imprimir diretamente
no terminal. A persistência inicial usa SQLite, da biblioteca padrão. O serviço depende
de um protocolo de armazenamento, permitindo outras implementações.
O contrato dos analisadores será definido na próxima etapa.

## Funcionalidades

1. Criar e listar casos (implementado).
2. Registrar e listar evidências com SHA-256 (implementado).
3. Inspecionar arquivos com um primeiro analisador.
4. Exportar resultados em relatórios.

O foco da investigação ainda precisa ser definido antes de escolher os
analisadores. Analisadores e relatórios ainda não estão implementados.
