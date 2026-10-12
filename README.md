# Berga Forensics

Ferramenta modular de investigação digital, inicialmente via terminal,
com estrutura preparada para uma futura interface web.

## Estado atual

CLI com criação e listagem de casos, registro e listagem de evidências,
cálculo de SHA-256 e persistência local em SQLite. Analisadores e relatórios
ainda serão implementados.

## Desenvolvimento

Requer Python 3.11 ou superior.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
bf --help
bf --version
```

Também é possível executar a base sem instalar dependências:

```bash
PYTHONPATH=src python3 -m berga_forensics --help
PYTHONPATH=src python3 -m berga_forensics --version
```

Veja [a arquitetura](docs/architecture.md) para as responsabilidades dos módulos
e os próximos passos propostos.

Dados locais de investigação podem ser mantidos em `data/`, ignorado pelo Git.

## Casos e evidências

```bash
bf case create "Investigação" --description "Descrição do caso"
bf case list
bf evidence add ./arquivo.pdf --case <id-do-caso> --source "Origem da coleta"
bf evidence list --case <id-do-caso>
```

Substitua `<id-do-caso>` pelo UUID retornado na criação. Os comandos operacionais
retornam JSON; ajuda e versão retornam texto. Datas são registradas em UTC.
Erros de operação retornam código 1 e uma mensagem em stderr; argumentos
inválidos retornam código 2.

O banco padrão é `data/berga.sqlite3`, relativo ao diretório de execução.
Para reutilizar um banco a partir de qualquer diretório, informe um caminho
absoluto com a opção global antes do comando:

```bash
bf --db /caminho/berga.sqlite3 case list
```

O registro lê o arquivo em blocos e guarda caminho absoluto, origem informada,
tamanho, SHA-256 e data do registro. Não copia o arquivo: preservar o original
continua sendo responsabilidade de quem realiza a coleta. A leitura pode
atualizar o horário de acesso conforme a configuração do sistema de arquivos.
Alterações detectadas durante a leitura cancelam o registro. O hash representa
o conteúdo lido no momento do registro; ainda não existe comando de reverificação
nem uma cadeia de custódia completa.

## Verificação

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

## Relatório da fase inicial

Veja o [relatório da fase inicial](docs/relatorio-fase-inicial.md) para o histórico
da entrega, funcionalidades, validação, limitações e próximos passos.
