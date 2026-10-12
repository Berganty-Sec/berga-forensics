# Relatório da fase inicial — Berga Forensics

Data: 11/10/2026 (America/Sao_Paulo). Versão: 0.1.0.

## Resultado

A fase inicial entrega uma ferramenta local pelo terminal para criar casos,
registrar arquivos como evidências e consultar os registros. O comando público
é `bf`. A base está organizada para receber analisadores, relatórios de casos
e uma interface web futura.

Esta entrega é uma base funcional de registro, não uma suíte completa de perícia.
O presente documento é um relatório de desenvolvimento; a geração de relatórios
investigativos pelo programa ainda não foi implementada.

## Trabalho realizado

1. Definido o início pelo terminal, mantendo a futura interface web no planejamento.
2. Criado o pacote Python no formato `src`, com configuração em `pyproject.toml`,
   versão 0.1.0, requisito Python 3.11+ e ponto de entrada executável.
3. Separadas as responsabilidades em CLI, núcleo, armazenamento, analisadores e
   relatórios. Os dois últimos são apenas espaços reservados nesta versão.
4. Implementados os modelos imutáveis de caso e evidência e o serviço de criação
   de casos e registro de arquivos, separado da apresentação no terminal.
5. Implementada persistência SQLite, com criação das tabelas, chaves estrangeiras,
   consultas parametrizadas e transações nas inserções.
6. Implementados quatro comandos operacionais, ajuda, versão e seleção de banco.
7. Implementado SHA-256 por leitura em blocos de 1 MiB, evitando carregar todo o
   arquivo em memória. Antes do registro, são comparados identidade do arquivo,
   tamanho e horários de modificação para detectar mudanças durante a leitura.
8. Adicionadas validações de nome vazio, caso inexistente, arquivo ausente e
   entrada que não seja arquivo regular, com mensagens de erro no terminal.
9. Alterado o comando principal de `berga` para `bf`, conforme a escolha do usuário,
   atualizando o ponto de entrada, ajuda e exemplos.
10. Concluída a instalação editável na `.venv` após identificar que o executável
    não havia sido criado. Confirmados ajuda e versão pelo executável instalado.
11. Criados testes de fluxo, hash, persistência, entradas inválidas e alteração
    durante leitura, além da documentação de uso e arquitetura.
12. Consolidada esta fase, revisada a documentação dos códigos de saída e realizada
    uma validação adicional em processos separados com dados temporários.

## Estrutura entregue

```text
berga-forensics/
├── src/berga_forensics/
│   ├── __init__.py          # Versão do pacote
│   ├── __main__.py          # Execução com python -m
│   ├── cli/main.py          # Argumentos e saída JSON
│   ├── core/models.py       # Caso e evidência
│   ├── core/service.py      # Regras e registro com SHA-256
│   ├── storage/sqlite.py    # Banco de dados local
│   ├── analyzers/          # Reservado para análises futuras
│   └── reports/            # Reservado para relatórios futuros
├── tests/test_workflow.py
├── docs/architecture.md
├── docs/relatorio-fase-inicial.md
├── pyproject.toml
├── .gitignore
└── README.md
```

A `.venv` é o ambiente local de execução. O diretório `data/` é criado quando
usado o banco padrão. Ambiente virtual, dados locais e artefatos de build estão
ignorados pelo Git.

## Comandos disponíveis

| Comando | Resultado |
| --- | --- |
| `bf --help` | Ajuda geral |
| `bf --version` | Versão da ferramenta |
| `bf case create "Nome" --description "Descrição"` | Cria caso e retorna UUID |
| `bf case list` | Lista casos |
| `bf evidence add arquivo --case UUID --source "Origem"` | Registra arquivo e SHA-256 |
| `bf evidence list --case UUID` | Lista evidências vinculadas ao caso |
| `bf --db /caminho/banco.sqlite3 case list` | Usa banco específico |

Os comandos operacionais retornam JSON. Ajuda e versão retornam texto.
Código de saída 0 indica sucesso; 1 indica erro da operação; 2 indica erro
nos argumentos tratado pelo argparse. As opções globais devem preceder o grupo.

## Dados armazenados

| Registro | Campos |
| --- | --- |
| Caso | UUID, nome, descrição e data de criação |
| Evidência | UUID, UUID do caso, caminho absoluto, origem informada, tamanho em bytes, SHA-256 e data do registro |

As datas dos registros usam UTC com indicação de fuso. A data deste relatório
segue o contexto local do usuário. O banco padrão fica em `data/berga.sqlite3`,
relativo ao diretório de execução. Executar de outro diretório pode selecionar
outro banco; para trabalhar sempre no mesmo, use `--db` com caminho absoluto.

## Uso inicial

A partir da raiz do projeto, com a instalação local já concluída:

```bash
source .venv/bin/activate
bf --version
bf case create "Primeiro caso" --description "Investigação inicial"
bf case list
```

Copie o UUID retornado na criação e substitua `UUID_DO_CASO` no exemplo:

```bash
bf evidence add ./amostra.txt --case UUID_DO_CASO --source "Coleta local"
bf evidence list --case UUID_DO_CASO
```

Para uma nova instalação, siga as instruções do [README](../README.md).
A ativação da `.venv` vale para o terminal atual; deve ser repetida em novos
terminais. Também é possível chamar `.venv/bin/bf` diretamente.

## Validação realizada

Ambiente verificado: Python 3.13.5 em Linux. O requisito mínimo declarado é
Python 3.11, mas outras versões não foram executadas nesta validação.

Os quatro testes automatizados passaram:

- SHA-256 de conteúdo conhecido, preservação do conteúdo e recuperação do banco.
- Rejeição de entradas inválidas sem registro de evidência.
- Cancelamento do registro após alteração detectada durante o cálculo do hash.
- Fluxo da CLI e mensagem de erro para caso inexistente.

Comando para repetir a suíte:

```bash
.venv/bin/python -m unittest discover -s tests -v
```

Uma verificação adicional chamou o executável `.venv/bin/bf` em processos
separados: criou um caso, listou casos, registrou uma amostra sintética, comparou
seu hash com o valor calculado independentemente e listou a evidência persistida.
Também confirmou código 1 para caso inexistente, código 2 para argumento obrigatório
ausente e versão `bf 0.1.0`. Todos esses controles passaram.

Essa verificação usou amostra e banco em diretório temporário, sem criar casos
ou evidências de demonstração no banco de trabalho do usuário.

## Limitações atuais

- O registro guarda o caminho e o hash; não cria uma cópia preservada do arquivo.
- A leitura pode atualizar o horário de acesso conforme o sistema de arquivos.
- O SHA-256 descreve o conteúdo lido no registro. Não há comando de reverificação.
- A detecção de mudanças durante leitura é uma verificação de metadados;
  não fornece uma captura atômica ou uma garantia contra toda alteração concorrente.
- Não há cadeia de custódia completa, trilha de auditoria ou autenticação.
- Não há inspeção de conteúdo, extração de metadados, análise de logs,
  discos, memória, rede ou OSINT.
- Não há edição/remoção de registros, exportação de relatórios de casos,
  migrações versionadas de banco ou interface web.
- Não foram realizados testes de desempenho, arquivos muito grandes ou
  validação forense formal.

## Próxima etapa proposta

1. Adicionar consulta individual de evidência e reverificação de SHA-256.
2. Implementar `bf evidence inspect` com um primeiro analisador de arquivos,
   definindo os formatos suportados e resultados estruturados.
3. Persistir achados vinculados às evidências.
4. Exportar relatório de caso com registros e resultados.
5. Evoluir preservação das evidências e histórico de operações conforme o
   escopo de uso definido para a ferramenta.

A interface web permanece como evolução posterior e deverá reutilizar os serviços
do núcleo. Os itens desta seção são planejamento, não funcionalidades entregues.
