# Relatório de investigação básica — simulação

Data da demonstração: 11/10/2026 (America/Sao_Paulo). Ferramenta: Berga Forensics 0.1.0.

## Escopo e resultado

Foi criado um caso demonstrativo e registradas duas evidências sintéticas usando
os comandos reais de `bf`. Os registros foram persistidos em SQLite e recuperados
pela CLI. Os hashes registrados foram conferidos independentemente com SHA-256
e coincidiram com o conteúdo dos arquivos ao final da simulação.

Nenhum sistema real foi investigado. Os horários, usuário e endereço IP do log
são dados fictícios. Este relatório foi escrito a partir dos registros e da leitura
do exemplo; a ferramenta ainda não gera relatórios nem analisa logs automaticamente.

## Caso

- Nome: Simulação básica — sequência de acessos.
- Identificador: `461a32e6-562e-442e-870f-8bad7d4bbfb7`.
- Descrição: Registro demonstrativo de log sintético; sem investigação de sistema real.
- Criado em: 2026-10-11T23:23:40.052523+00:00 (UTC).
- Diretório da simulação: `data/simulacoes/investigacao-basica-c5cec7c7`.
- Banco separado: `data/simulacoes/investigacao-basica-c5cec7c7/investigacao.sqlite3`.

## Procedimento executado

1. Criados um log de acessos fictício e uma nota explicando sua origem.
2. Executado `bf --version`, com retorno `bf 0.1.0`.
3. Criado o caso com `bf --db BANCO case create NOME --description DESCRICAO`.
4. Registrados os dois arquivos com `bf --db BANCO evidence add ARQUIVO --case UUID --source ORIGEM`.
5. Consultados os casos e as evidências por `case list` e `evidence list`.
6. Conferidos os dois hashes com cálculo independente sobre os arquivos atuais.
7. Salvos os registros em `registros.json` no diretório da simulação.

Todos os comandos operacionais concluíram com código de saída 0.

## Evidências registradas

Origem declarada dos dois arquivos: arquivo sintético criado para demonstração.
Os registros contêm caminhos absolutos para os arquivos de origem.

| Arquivo | Tamanho (bytes) | Identificador |
| --- | --- | --- |
| `acessos-ficticios.log` | 248 | `a5f09558-3d5c-4e63-bf35-b1ad48521bd3` |
| `nota-coleta.txt` | 230 | `6b72779b-eebb-45af-bdd6-09a6eb023921` |

### SHA-256

**acessos-ficticios.log**

```text
560dda098f6dcb2030e3e1686e06131defeaa6e34e8d4846b428f11b00687250
```

Registrada em: 2026-10-11T23:23:40.318894+00:00 (UTC).

**nota-coleta.txt**

```text
e0cc26fe4d00bafa7b34ff3393b32926d3e099210d570b2995fca22c28561fa3
```

Registrada em: 2026-10-11T23:23:40.584049+00:00 (UTC).

## Observações sobre o log fictício

Leitura manual do conteúdo criado para a demonstração:

| Horário fictício (UTC−03:00) | Usuário | IP | Evento | Resultado |
| --- | --- | --- | --- | --- |
| 11/10/2026 09:00 | demo | 192.0.2.10 | Login | Falha |
| 11/10/2026 09:01 | demo | 192.0.2.10 | Login | Falha |
| 11/10/2026 09:02 | demo | 192.0.2.10 | Login | Sucesso |

O exemplo contém duas falhas seguidas de um sucesso para o mesmo usuário e IP.
Essa sequência, sozinha, não permite concluir que houve invasão ou comprometimento.
Em um caso real, seria necessário confirmar a origem e confiabilidade do log e
correlacionar outros eventos. Nesta simulação, a sequência foi definida de propósito.

## Conclusão e limites

O exercício demonstrou o fluxo disponível: criação de caso, registro de arquivos,
cálculo de hashes, persistência e consulta pelo terminal. Foram registrados um caso
e duas evidências; ambas passaram na conferência independente de SHA-256.

A ferramenta não produziu uma conclusão investigativa automática. Não foram
executadas análises de conteúdo, aquisição forense ou coleta de sistema real.
O registro não cria cópias preservadas e não constitui cadeia de custódia completa.
Os hashes conferidos descrevem os arquivos no momento desta demonstração.

## Como consultar a demonstração

Na raiz do projeto:

```bash
source .venv/bin/activate
bf --db data/simulacoes/investigacao-basica-c5cec7c7/investigacao.sqlite3 case list
bf --db data/simulacoes/investigacao-basica-c5cec7c7/investigacao.sqlite3 evidence list --case 461a32e6-562e-442e-870f-8bad7d4bbfb7
```

Os arquivos locais em `data/` são ignorados pelo Git. O relatório fica em `docs/`.
