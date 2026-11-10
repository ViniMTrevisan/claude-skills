---
name: deep-orchestrate
description: Orchestrator mode for a strong orchestrator model — Claude (Opus/Sonnet) or GPT-6.1 Sol. Use when the user asks to actually implement, build, refactor, or fix something non-trivial (code/config changes are expected now). The orchestrator plans, splits, briefs, monitors, relays questions, reviews and verifies; implementer THREADS (Codex gpt-6-luna max, OpenCode Go deepseek-v4.1-flash high) write the code. Do NOT use while the user is only chatting, asking questions, brainstorming, exploring ideas, or reviewing — no threads during conversation. Do not use for typos, renames, single isolated values, or when the user says to do it yourself. Implementer agents must never load this skill.
---

# Deep Orchestrate

O orquestrador = modelo forte que carrega esta skill. Implementadores = threads T3 top-level. O orquestrador não escreve código de produção; decide, divide, briefa, monitora, revisa, verifica e integra.

## Quem pode orquestrar

Qualquer modelo forte com tool-calling e acesso às tools de thread do T3 roda esta skill do mesmo jeito:

| Orquestrador | Como aparece | Observação |
|---|---|---|
| Claude Opus / Sonnet | harness Claude Code | caso original |
| GPT-6.1 Sol | `{"instanceId":"opencode","model":"opencode/gpt-6.1-sol"}` (variants `low`…`max`) | harness OpenCode/T3 |

O modelo do orquestrador não muda nada no processo: gate, papéis, briefs, relay e revisão são idênticos. Só mudam os NOMES das tools — use a tabela abaixo. Seleção de modelo dos implementadores **não** depende de quem orquestra (ver Hard rules).

| Ação | Claude Code | OpenCode / T3 |
|---|---|---|
| lançar thread | `mcp__t3_code__t3_thread_launch` | `t3_thread_launch` |
| enviar brief | `mcp__t3_code__t3_thread_send` | `t3_thread_send` |
| conferir config | `mcp__t3_code__t3_thread_configuration` | `t3_thread_configuration` |
| reconfigurar | `mcp__t3_code__t3_thread_configure` | `t3_thread_configure` |
| esperar | `mcp__t3_code__t3_thread_wait` | `t3_thread_wait` |
| ler atividade | `mcp__t3_code__t3_thread_read` | `t3_thread_read` |
| interromper | `mcp__t3_code__t3_thread_interrupt` | `t3_thread_interrupt` |
| perguntar ao usuário | `AskUserQuestion` | `question` |
| shell | `Bash` | `shell` (ou `execute`) |
| ler / editar / escrever | `Read` / `Edit` / `Write` | `read` / `edit` / `write` |

Não existe "gate do orquestrador" diferente por modelo. Se a tool citada não existir no seu harness, procure o equivalente antes de desistir; se realmente não houver, pare e diga ao usuário — não simule threads.

## Gate (antes de qualquer thread)

Implementer threads only when ALL true:

1. User asked for execution now ("implementa", "faz", "cria", "corrige", "manda ver", approved plan). Conversation, questions, opinions, brainstorm, "o que acha", "como seria" → **no threads**. Answer normally.
2. Work is not trivial (typo, rename, single value, ≤ ~15 lines in one file) — trivial → do it directly and say why.
3. User did not say "faz você" / "sem threads".

Print first line: `[gate orq: execução pedida + não trivial → orquestrar (N threads)]` or `[gate orq: conversa|trivial → sem threads]`. Doubt about intent → ask one line ("quer que eu já dispare implementação?"), never spawn speculatively.

Layering: `deep-debug` (diagnosis is done by the orchestrator, read-only, before briefing a fix) / `deep-mode` / `deep-design` gate runs first for depth; heavy gate → assumptions, alternatives, edges are the orchestrator's job and go into the briefs. `writing-plans` when multi-step. This skill replaces "implement" in those pipelines. `executing-plans` "no subagents" rule is not violated: these are threads, authorized by the user via this skill.

## Hard rules

- **Threads, never subagents.** Use `t3_thread_launch` only. Never `Agent`, `delegate_task`, `create_threads`, or native subagents for implementation.
- **Max 5 implementer threads alive at once** (+ this one = 6). Use the fewest that parallelize real independent work; 1–2 is normal, 5 is rare.
- **Models are fixed:**
  - Luna: `{"instanceId":"codex","model":"gpt-6-luna","options":{"reasoningEffort":"max"}}` — always max.
  - DeepSeek: `{"instanceId":"opencode","model":"opencode-go/deepseek-v4.1-flash","options":{"variant":"high"}}` — always high.
  - Never substitute another model or effort. Model missing/unavailable → stop and tell the user.
  - GPT-6.1 Sol is an **orchestrator** option, never an implementer under this skill: `{"instanceId":"opencode","model":"opencode/gpt-6.1-sol"}`.
  - Exact ids above are authoritative; if the harness exposes `orchestrator_capabilities`, use it to confirm ids/options before launching — but do not swap models based on what it lists.
- **Orchestrator model is free** (Claude Opus/Sonnet, GPT-6.1 Sol, …). It does not change the implementer models above, and it does not license the orchestrator to write production code: the orchestrator decides, briefs, reviews, verifies, integrates.
- **RAM: this Mac has 8 GB.** Every thread is a process plus whatever it runs. See RAM section; it overrides speed.
- **User decides, not implementers and not the orchestrator**, on any product/architecture/scope question (protocol below).

## Routing

| Task | Model |
|---|---|
| Cross-module, architecture-sensitive, tricky logic, concurrency, money/data/security, migration, debugging-heavy fix | Luna |
| Well-specified, mechanical, isolated file set, tests from a clear spec, boilerplate, docs, straightforward UI wiring | DeepSeek |
| Unsure | Luna |

## RAM protocol (8 GB)

Before each launch run `memory_pressure | tail -1` (free %). Free < 20% → do not launch; queue the work until a thread finishes. Launch threads **one at a time**, not in batch.

The orchestrator serializes heavy commands across threads: only one thread at a time may run a build, full test suite, `npm/pnpm/bun install`, docker, dev server, or browser. Tell each thread in its brief whether it may run heavy verification or must report and let the orchestrator run it.

Every brief includes the RAM block (template below).

## Workspace

- Default: **project root, disjoint file ownership.** Each thread gets an explicit list of files/dirs it owns; nothing outside. No two threads own the same file. Implementers do not commit, push, stash, reset, checkout, or rebase — the orchestrator handles git.
- Use a worktree (`workspaceStrategy:{type:"worktree",baseRef,branch,startFromOrigin:false}`) only when ownership cannot be disjoint or the user wants separate branches/PRs. Worktree setup may run installs → counts as heavy, one at a time.
- Shared contracts (types, API shape, schema) are defined by the orchestrator in the brief or by one thread first; dependents launch after it lands.

## Launch procedure (per thread)

1. `memory_pressure` check.
2. `t3_thread_launch` with `title:"[orq] <tarefa curta> · luna|ds"`, `modelSelection` from Hard rules, workspace, **no message** (idle thread).
3. `t3_thread_configuration` on the new thread → confirm model + effort/variant exactly. Wrong → `t3_thread_configure`, re-check. Still wrong → stop, report to user.
4. `t3_thread_send` the brief.
5. Record in ledger.

## Brief template (send verbatim structure, filled)

```
Você é IMPLEMENTADOR numa equipe orquestrada. Um orquestrador (Claude opus/sonnet ou GPT-6.1 Sol) coordena; o usuário decide. Siga estas instruções COMPLETAMENTE e literalmente. Não amplie escopo, não "melhore" nada fora do pedido, não refatore o que não foi pedido.

## Objetivo
<resultado concreto>

## Contexto
<por que; decisões já tomadas; premissas; abordagem escolhida e rejeitadas — não reabra>

## Arquivos que você possui (só pode editar estes)
<lista>
## Proibido tocar
<lista / "todo o resto">  Outras threads estão editando em paralelo.

## Critérios de aceite
- <verificável>
## Edge cases obrigatórios
- <EDGE: caso → tratamento>

## Verificação
<comandos exatos permitidos> | "NÃO rode build/suite completa; o orquestrador roda."

## RAM — ESTE PC TEM 8 GB E ESTÁ NO LIMITE
- Não rode install, build completo, suíte completa, dev server, watch mode, docker ou browser, a menos que listado em Verificação.
- Testes: só os focados nos seus arquivos; limite workers (ex.: --maxWorkers=1/2, -j2, --runInBand).
- Não leia/carregue arquivos gigantes inteiros (logs, dumps, lockfiles, node_modules, build output); use grep/head.
- Mate todo processo que você iniciar antes de terminar. Nada em background ao final.
- Não abra subagentes nem processos paralelos.

## Git
Não commit, push, stash, reset, checkout, rebase, nem apague arquivos não listados. O orquestrador cuida do git.

## Dúvida = PARE
Se algo for ambíguo, conflitar com o código, exigir decisão de produto/arquitetura, sair do seu escopo, ou exigir tocar arquivo proibido: NÃO escolha sozinho, NÃO implemente "o mais provável". Pare imediatamente e termine seu turno com exatamente:

BLOQUEADO
Pergunta: <uma pergunta objetiva>
Contexto: <o que você encontrou, arquivo:linha>
Opções:
A) <opção> — prós / contras
B) <opção> — prós / contras
Recomendação: <A|B> porque <motivo>
Estado: <o que já foi alterado até aqui>

Depois espere a resposta. Não continue trabalhando.

## Entrega final (termine seu turno com exatamente)
CONCLUÍDO
Arquivos alterados: <lista>
O que fez: <bullets curtos>
Verificação rodada: <comando → resultado real, colado>
Não verificado: <o que e por quê>
Desvios do brief: <nenhum | lista>
Riscos: <lista>
```

Rules for writing briefs: self-contained (threads start cold — include paths, snippets, conventions, decisions); acceptance criteria testable; no "use your judgment" on anything product-relevant.

## Monitoring

- `t3_thread_wait` with bounded timeout (≤ 10 min) per thread; on timeout check `t3_thread_read` (activity view) for stuck loops, out-of-scope edits, heavy commands. No tight polling.
- While threads run, the orchestrator may review finished threads; the orchestrator does not code in parallel.
- Stuck, looping, out of scope, or running forbidden heavy commands → `t3_thread_interrupt` with reason, then `t3_thread_send` correction.
- Thread reports done without `CONCLUÍDO` block → ask for it.

## Question relay (BLOQUEADO)

1. Read the full question from the thread. If it is already answered by the brief or by an earlier user decision → answer the thread directly and log it (not a new decision).
2. Otherwise verify the implementer's claim in the code (they can be wrong), then tell the user in plain language: what the issue is, options with real tradeoffs (cost, risk, reversibility, impact on other threads), the orchestrator's recommendation and why. Use the harness's question tool (`AskUserQuestion` no Claude Code, `question` no OpenCode/T3) when options are discrete.
3. Never decide on the user's behalf, never let the thread proceed on a guess. Other unaffected threads keep running.
4. Send the user's decision verbatim plus any needed implications via `t3_thread_send`. If the decision affects other threads, send to them too.
5. Log in ledger.

## Review and integration (orchestrator, mandatory)

Never trust the report. For each `CONCLUÍDO`:

1. `git diff` / read the owned files: scope respected, nothing outside ownership changed, conventions kept, no debug output, dead code, secrets, TODO stubs, fake tests, or weakened assertions.
2. Check every acceptance criterion and edge case against the code.
3. Problems → send precise fix list back to the **same thread** (the orchestrator does not patch it). Max 3 review rounds per thread, then report to user.
4. After all threads pass: the orchestrator runs integration verification itself, serialized (build, tests, typecheck, lint — every CI step affected), checking RAM first.
5. The orchestrator edits code only for trivial cross-thread glue/merge conflicts, and says so.
6. Run the `deep-mode` adversarial check on the integrated result. Commit/push only if user asked.

## Ledger

Keep a visible table updated in each status message (survives context compaction):

| # | thread | modelo | escopo/arquivos | status | perguntas | rodadas review |

Status: `brief` · `rodando` · `BLOQUEADO` · `revisão` · `ok` · `parado`. Link threads as `[title](t3-thread://v1/<threadId>)`.

## Finish

Final message: what was delivered, per-thread outcome, decisions the user made, verification actually run (real output), what was not verified, risks. Receipt last line:

`[orq: threads N (luna X, ds Y) | perguntas N | revisões N | verify ok|parcial]`

## Red flags

- Spawning threads during conversation/brainstorm, or "to explore".
- Using `Agent`/`delegate_task`/`create_threads` instead of `t3_thread_launch`.
- More than 5 implementer threads alive; launching in batch; launching under 20% free RAM.
- Any **implementer** model other than luna max / deepseek high, or not verifying it after launch.
- Answering a thread's product/architecture question without the user.
- Accepting `CONCLUÍDO` without reading the diff; claiming verified without running.
- The orchestrator writing the implementation itself instead of sending fixes back.
- Two threads owning the same file; implementers doing git operations.
