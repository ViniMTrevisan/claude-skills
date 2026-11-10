# claude-skills

Minhas skills para Claude Code (funcionam também no Codex e em outros agents compatíveis com `SKILL.md`).

## Instalar as skills deste repo

Todas de uma vez:

```bash
git clone https://github.com/ViniMTrevisan/claude-skills.git
mkdir -p ~/.claude/skills
cp -R claude-skills/skills/* ~/.claude/skills/
```

Só uma skill (exemplo: `deep-mode`):

```bash
cp -R claude-skills/skills/deep-mode ~/.claude/skills/
```

Ou via [skills CLI](https://github.com/vercel-labs/skills):

```bash
npx skills add ViniMTrevisan/claude-skills            # escolhe quais
npx skills add ViniMTrevisan/claude-skills --skill deep-mode
```

Reinicie o Claude Code depois de instalar.

## Skills deste repo

### Raciocínio / processo

| Skill | O que faz |
|---|---|
| [deep-mode](skills/deep-mode) | Gate de profundidade antes de implementar: premissas, alternativas, edge cases, check adversarial. Compensa modelo em esforço médio. |
| [deep-debug](skills/deep-debug) | Diagnóstico de bug / teste falhando antes de propor fix. |
| [deep-design](skills/deep-design) | Gate para tarefa de UI; carrega `ui-polish` e/ou `dashboard-ui`. |
| [deep-orchestrate](skills/deep-orchestrate) | Claude orquestra, threads de outros modelos implementam (feito para o T3 Code; adapte os modelos). |
| [brainstorming](skills/brainstorming) | Clarificar escopo quando há várias interpretações válidas. |
| [writing-plans](skills/writing-plans) | Plano escrito para trabalho multi-etapa. |
| [executing-plans](skills/executing-plans) | Executar plano aprovado com checkpoints. |
| [ponytail](skills/ponytail) | YAGNI: menor solução que resolve o problema verificado. |
| [context-slicer](skills/context-slicer) | Recorta contexto mínimo e auditável em repo/conversa grande. |
| [handoff-contract](skills/handoff-contract) | Handoff verificado entre agents/sessões (com validador de segredos). |
| [code-review](skills/code-review) | Review de PR/branch/diff focado em correção. Read-only por padrão. |
| [checkup](skills/checkup) | Manutenção do setup Claude Code/Codex: contexto inchado, skills/MCPs sem uso, hooks lentos. |

### UI / design

| Skill | O que faz |
|---|---|
| [frontend-design](skills/frontend-design) | Páginas/componentes com qualidade visual. |
| [ui-polish](skills/ui-polish) | Botões, cards, modais, micro-interações, sensação premium. |
| [dashboard-ui](skills/dashboard-ui) | Admin panels, tabelas, KPIs, filtros, kanban. |

### Escrita

| Skill | O que faz |
|---|---|
| [linkedin-post](skills/linkedin-post) | Posts de LinkedIn em inglês que não parecem escritos por IA (com linter). |

### Créditos

- `brainstorming`, `writing-plans`, `executing-plans`: versões enxutas adaptadas de [obra/superpowers](https://github.com/obra/superpowers).
- `frontend-design`: adaptada da skill oficial da Anthropic ([anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official)); licença em `LICENSE.txt`.
- `ponytail`: versão reescrita inspirada em [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail) (MIT).

## Skills de terceiros que eu uso (instale da fonte)

| Skill | Instalar |
|---|---|
| [caveman](https://github.com/JuliusBrussee/caveman) — respostas comprimidas, menos tokens | `npx skills add JuliusBrussee/caveman` |
| [unslop](https://github.com/heydamir/unslop) — tira cara de "UI feita por IA" | `npx skills add heydamir/unslop` |
| [revenue-centric-design](https://github.com/heliocosta-dev/revenue-centric-design) — design de SaaS focado em conversão/retenção | `npx skills add heliocosta-dev/revenue-centric-design` |
| [ponytail original](https://github.com/DietrichGebert/ponytail) (se preferir ao meu) | `/plugin marketplace add DietrichGebert/ponytail` → `/plugin install ponytail@ponytail` |

## Plugins que eu uso (Claude Code)

Do marketplace oficial (`/plugin install <nome>@claude-plugins-official`):

- `superpowers` — workflows completos (as versões enxutas acima vêm daqui)
- `code-review`
- `context7` — docs atualizadas de libs
- `security-guidance`

## Dica: como eu ligo tudo

No `~/.claude/CLAUDE.md` eu deixo regras de quando usar cada skill, por exemplo:

```markdown
Antes de implementação, refactor ou decisão técnica, rode `deep-mode`.
Tarefa de UI roda `deep-design` no lugar do deep-mode.
Bug ou teste falhando começa em `deep-debug`.
Ordem: deep-mode (profundidade) → brainstorming/writing-plans (processo) → ponytail (o que não deve existir).
```
