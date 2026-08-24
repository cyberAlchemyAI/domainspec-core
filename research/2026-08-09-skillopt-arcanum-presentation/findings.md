# SkillOpt + Arcanum: findings para uma apresentação avançada de 35 minutos

## Resposta direta

SkillOpt e Arcanum não implementam a mesma coisa e não estão integrados. O paper SkillOpt reporta um método offline para propor e selecionar mudanças em um documento textual persistente — a `skill` — usando rollouts pontuados, `bounded edits`, memória de rejeições e uma comparação estrita em seleção. O corpus público inspecionado do Arcanum, por sua vez, registra e documenta responsabilidades separadas para contrato, fixture, validação, observação, reflexão, aprovação humana e decisões de lifecycle. A relação defensável é uma **semelhança estrutural limitada**, seguida de adjacência e de um complemento arquitetural ainda proposto: um optimizer poderia produzir candidatos para uma rota governada, mas esse wiring não existe no corpus inspecionado.

O que a palestra pode mostrar honestamente hoje é a mecânica reportada pelo paper, as superfícies públicas inspecionadas do Arcanum, a ausência explícita da integração e uma `SIMULAÇÃO DE CONTRATO` sintética. Ela não pode apresentar código executado, demo live/runnable, optimizer de sigils, melhoria comportamental observada, reprodução dos resultados, promoção, deployment, produção ou compreensão da audiência.

## Audiência e tese

**Audiência:** profissionais avançados que constroem agentes, automações com LLMs, developer workflows, plataformas internas de IA ou sistemas multiagente. O contrato é uma apresentação em português, com slides e código-fonte exibido, limitada a 35 minutos. Termos em inglês permanecem quando a tradução apagaria fronteiras técnicas. Fonte: `arcanum/writing/cfp-tdc-arcanum-skillopt.md:19,29-47,49-55`.

**Tese em uma frase:** SkillOpt reporta como propor e selecionar alterações no estado textual persistente de uma `skill`; Arcanum descreve responsabilidades separadas para transformar evidência em mudança governada; a ponte útil é uma composição ainda não implementada, e não identidade nem autoevolução já existente.

## SkillOpt: mecanismo, resultados e limites verificados

### Mecanismo reportado

1. Uma `skill` em linguagem natural é tratada como estado externo treinável de um `target model` congelado. Para um harness, uma tarefa e uma skill, a execução produz trajetória e recompensa escalar em `[0,1]`; treino gera candidatos, seleção escolhe e teste reporta o desempenho final. [SkillOpt, arXiv:2605.23904v2, pp. 4–5, §3.1, Eqs. (1)–(3)].
2. O estado do optimizer inclui a skill corrente, a melhor skill aceita por validação, hashes já vistos, um buffer de passos rejeitados local ao epoch e estado slow/meta opcional. O artefato exportado é `best_skill.md`. [p. 5, §3.1, parágrafo após Eq. (3); p. 22, Algorithm 1, linhas 1–3].
3. O target congelado produz batches de rollouts pontuados. A reflexão separa falhas e sucessos, produz propostas estruturadas e faz deduplicação/merge hierárquico, priorizando correções de falhas. [p. 4, Figure 2; p. 5, §§3.2–3.3; p. 22, Algorithm 1, linhas 7–12].
4. O orçamento textual `L_t` funciona apenas como analogia de learning rate. Em patch mode, as operações são `append`, `insert_after`, `replace` e `delete`; o pool é limitado a no máximo `L_t` edits. Há schedules constant, linear, cosine e autonomous. Isso não é gradient descent. [p. 5, §3.4; pp. 23–25, §§C.2.1–C.2.6; p. 27, §C.3].
5. Um candidato só é aceito quando seu selection score é **estritamente maior** que o score corrente; empate é rejeição. Se superar também o melhor histórico, torna-se `best_skill.md`. O test split permanece bloqueado até o relatório final. [p. 6, §3.5; p. 8, “Default optimizer hyperparameters”; p. 12, “Gate strictness”; p. 22, Algorithm 1, linhas 14–27 e 37].
6. Mudanças rejeitadas e quedas de score geram feedback negativo local ao epoch; comparações same-task alimentam slow/meta guidance, que também passa por validation gate. Meta-skill fica no lado do optimizer e não é deployed. [p. 6, §§3.5–3.6; pp. 26–27, §§C.2.7–C.4].
7. A otimização é offline. Em inference, usa-se a `best_skill.md` estática sem optimizer calls adicionais e sem weight update; o texto da skill ainda ocupa context tokens. [pp. 2–3, Introduction; p. 6, §3.7; pp. 13–15, §§4.3–4.4 e Table 6].

### Resultados reportados — não reproduzidos

- O paper avalia seis benchmarks principais — SearchQA, SpreadsheetBench, OfficeQA, DocVQA, LiveMathematicianBench e ALFWorld — com sete target models em direct chat e também GPT-5.5 nos harnesses Codex e Claude Code. Compara com no skill, human skill, one-shot LLM skill, Trace2Skill, TextGrad, GEPA e EvoSkill onde o protocolo permite. [pp. 7–10, Table 1 e §4; pp. 20–21, Appendix C].
- Os autores reportam SkillOpt como best ou tied-best nas 52/52 células model × benchmark × harness avaliadas. Para GPT-5.5, os ganhos absolutos médios sobre no skill são +23,5 pontos em direct chat, +24,8 em Codex e +19,1 em Claude Code. Em direct chat, 82,3 é comparado ao oracle per-cell de 76,9 entre métodos concorrentes, diferença de +5,4 pontos. [pp. 7, 10–11, Table 1; §4.1]. Esses números são limitados às células, splits, métricas, scorers e baselines compatíveis avaliados.
- As 11 linhas de transfer reportadas são positivas sobre o baseline no-skill do target: quatro cross-model (+3,0 a +9,4), quatro cross-harness (+1,6 a +59,7) e três OlympiadBench→Omni-MATH (+1,3 a +3,7), sem reotimização no target. Isso sustenta “transfer observado nos shifts testados”, não portabilidade universal. [p. 9, Table 4; pp. 12–13, §4.3].
- Ablations associam bounded edits, rejected-buffer feedback e slow/meta updates ao desempenho nas configurações testadas. A queda de SpreadsheetBench de 77,5 para 55,0 remove **meta e slow update em conjunto**; não se pode atribuir os −22,5 pontos exclusivamente a um dos dois. [p. 8, Tables 2–3; pp. 11–12, §4.2].
- Em quatro células, um optimizer target-matched recupera aproximadamente 56–74% do ganho do optimizer GPT-5.5, mas fica atrás dele. Isso enfraquece uma leitura exclusivamente de strong-teacher distillation sem eliminar confounding por capacidade do optimizer. [pp. 13–14, §4.3, Table 5].
- Em seis casos GPT-5.5/GPT-5.5, os artefatos finais têm 379–1.995 tokens e 1–4 updates aceitos, ao custo de 20,8M–213,8M training tokens e 0,6M–46,4M tokens por ponto absoluto de teste. [pp. 14–15, §4.4, Table 6].

### Limites de prova

Todos os números acima são **paper-reported e não reproduzidos**. O preprint não constitui por si só revisão independente. A seleção depende de trajetórias pontuadas e de um signal confiável; tarefas subjetivas podem exigir juízes humanos ou model-based. O custo offline pode não se pagar para tarefas one-off. O método otimiza uma skill, não uma biblioteca heterogênea. Transfer exige nova avaliação held-out. Selection gating não é garantia de segurança, correção semântica, governance ou production approval.

O repositório oficial atual foi inspecionado em `microsoft/SkillOpt@ba820b500f9da96685cf2780c7dc85ed4eb6563e`, commit de 2026-08-09, posterior aos experimentos de maio. Nenhum commit/tag experimental exato foi estabelecido; portanto, esse HEAD não pode ser apresentado como snapshot reprodutível do paper.

## Arcanum hoje: estado observado e teto de alegação

| Estado | Evidência pública inspecionada | O que isso não prova |
|---|---|---|
| **Inspecionado / registrado / documentado** | Workflow canônico de doze estágios; validation protocol e registry gates; promotion semantics; observability nos caminhos determinísticos documentados; Signal Observer categórico; Workflow Reflect como produtor de propostas; `sigil-maintenance-loop` registrado; contrato de `experiment-harness`; tipos numéricos/booleanos em `OracleEvidence.metrics` e `ScoreResult.components`; run kernel e smoke documentado de SWE-bench Lite. | Execução dessas superfícies nesta pesquisa, scalar objective canônico, integração com SkillOpt, release ampla ou produção. |
| **Planejado / candidate** | L4 continuation-feedback attribution; active-run pointer; observação first-class de invocações nativas; SmellBench, PerfCodeBench, cloud workers e dashboard; qualquer optimizer offline para sigils ou strict held-out edit gate. | Implementação ou disponibilidade operacional. |
| **Ausente no corpus inspecionado** | Wiring de `ScoreResult` para reflection/edit/acceptance/promotion; single scalar reward canônico para qualidade de sigils; aceitação automática por comparação held-out; contrato/validator geral de provenance e independência do grader; proibição de self-authorship task/grader; observabilidade determinística universal de native skill selection. | A ausência é limitada às interfaces inspecionadas; não autoriza uma afirmação universal sobre todo sistema possível. |
| **Deployed — não provado** | Nenhuma fonte permitida prova deployment externo ou operação em produção. Registry, `.agents/skills` e `.arcanum/observability` são superfícies/projections locais. | Deployment, production operation, adoption ou readiness. |

Seletores principais: `arcanum/framework/SIGIL-DEVELOPMENT-WORKFLOW.md:7-22,182-193`; `arcanum/framework/VALIDATION-EXPERIMENT-PROTOCOL.md:51-98`; `arcanum/framework/observability/ARCHITECTURE-OVERVIEW.md:9-75,123-181,215-240`; `arcanum/arcana/signal-observer/SKILL.md:53-90`; `arcanum/arcana/workflow-reflect/SKILL.md:60-130`; `arcanum/registry/SPELLS.md:7-22`; `arcanum/spells/sigil-maintenance-loop/README.md:1-35,78-110,129-152,179-193`; `arcanum/benchmark/src/schemas.ts:57-78`; `arcanum/benchmark/ARCHITECTURE.md:127-177,224-234`.

## Matriz de relação

| Relação | SkillOpt | Arcanum | Alegação segura | Limite |
|---|---|---|---|---|
| **Semelhança estrutural limitada** | Texto persistente participa da produção de comportamento reutilizável. | Um sigil descreve comportamento reutilizável sob contrato e lifecycle. | Texto persistente pode participar de comportamento reutilizável em ambos os recortes. | Propriedade compartilhada não é identidade: SkillOpt skill state não é sigil, spell, capability, registry entry ou artefato promovido. |
| **Adjacência** | Scored rollouts → reflection → bounded edits → merge → comparação estrita → rejection memory. | Fixture → validation → categorical observation → reflection proposal → approved mutation → lifecycle decision. | Os ciclos são conceitualmente adjacentes. | Nenhuma interface, estado ou fluxo compartilhado foi demonstrado. |
| **Complemento proposto** | Um optimizer poderia fornecer candidate edits ordenados por evidência held-out. | Uma rota poderia preservar provenance, human approval, validation, lifecycle routing e promotion boundary. | Optimizer-produced candidates poderiam entrar em uma rota governada. | Inferência arquitetural; não implementada, integrada, validada ou deployed. |
| **Gaps contratuais** | O paper define objective, partitions, edit operations e comparator para seu setting. | Há score-shaped infrastructure e maintenance governance, mas não o contrato que os liga. | Faltam seis famílias de contratos para uma ponte verificável. | Não chamar isso de “the missing layer”. |

As seis famílias faltantes são: (1) objetivo e provenance do scorer, incluindo anti-gaming; (2) população de tarefas e distribuição held-out com locks e contamination controls; (3) interface de candidate edit com target digest, scope, identity e rollback; (4) comparação matched baseline/candidate, tie rule e regression residue separada de approval/promotion; (5) handoffs tipados score→reflection→proposal com autoridade, failure e replay; (6) integration validation com fixture pinada, paths executados, mutation test, regressão e rollback.

## Mapa compacto de precedentes

| Trabalho | Identidade e seletor | Papel limitado na narrativa |
|---|---|---|
| GEPA | arXiv:2507.19457, Abstract e método: trajectory sampling, natural-language reflection, prompt-update testing, Pareto frontier | Precedente adjacente de prompt optimization. |
| Trace2Skill | arXiv:2605.21810v1, Abstract, §2.2.4 SelectQ, §2.3, §3.1 | Precedente de trace-to-skill, seleção e evolução. |
| EvoSkill | arXiv:2603.02766v1, Abstract, §§2.1–2.2 | Structured skill folders, held-out validation, frontier selection e feedback history. |
| SkillsBench | arXiv:2602.12670, versão corrente, Abstract, Appendix D.5–D.6, Table 6, §D.6.1 | Evidência de benchmark sobre uso/autoria de skills; não prova impossibilidade universal. |
| SkillOpt | arXiv:2605.23904v2, pp. 4–6 §§3.1–3.6, p. 22 Algorithm 1, pp. 7–11 Table 1 e §4.1 | Otimização reportada de uma skill textual com bounded edits, memória e strict selection. |
| Arcanum | `arcanum/README.md:105-146,169-177`; workflow e definitions citados abaixo | Separação corpus-local de evidence, observation, reflection, approved mutation, validation e lifecycle. |

Esse mapa impede alegações de prioridade. O valor da apresentação é a composição e o mapa de fronteiras, não “first”, “unique” ou superioridade histórica.

## Legenda terminológica

| Termo | Uso preciso nesta apresentação |
|---|---|
| prompt pontual | Entrada textual de uma execução; não é comportamento reutilizável nem artefato governado. |
| SkillOpt `skill state` | Documento textual persistente que o paper trata como estado externo treinável de um target congelado; não é sigil. |
| executor / harness | Executa um target e captura resultados; não é target sigil, fixture, grader ou promotion owner. |
| target sigil | Objeto reutilizável que seria exercitado ou revisado; nenhum target concreto está source-bound para a simulação. |
| fixture | Caso delimitado com entrada e expectativa; não é held-out distribution, benchmark ou production proof. |
| output | Resultado da execução; não é observation, score, acceptance ou validation verdict. |
| observation | Registro e roteamento de evidência; não é julgamento semântico, edit ou mutation authority. |
| reflection | Interpretação de evidência que pode propor mudança; não edita automaticamente. |
| candidate proposal | Mudança sugerida e ainda não aplicada. |
| SkillOpt acceptance | Seleção algorítmica por score estritamente maior; não é user approval, promotion, publication ou deployment. |
| user-approved mutation | Aplicação de mudança exatamente delimitada após autorização explícita. |
| validation | Julgamento delimitado; não transfere autoridade e não prova deployment/production. |
| promotion | Decisão de lifecycle ou aplicação review-bound à fonte canônica; não é publication, deployment ou production. |

**Nota de autoridade:** `sigil`, `spell` e `capability` são descritos no README e no workflow público, mas ainda não possuem definições canônicas próprias em `arcanum/definitions/DEFINITIONS.md`. Não apresentar descrições operacionais como definições já governadas.

## Espinha de slides — 35 minutos

| Tempo | Duração | Bloco | Função |
|---|---:|---|---|
| 00:00–02:30 | 2,5 min | A resposta desaparece; o método pode permanecer | Contrastar resposta pontual e comportamento reutilizável. |
| 02:30–05:30 | 3 min | Do prompt aos contratos intermediários | Nome, fronteira, contrato, fixture, evidence e owner. |
| 05:30–09:00 | 3,5 min | Vocabulário que não pode colapsar | Separar atores, artefatos e decisões. |
| 09:00–13:00 | 4 min | SkillOpt: mecanismo reportado | External textual state, rollout, edits e strict gate; paper-reported/not reproduced. |
| 13:00–17:00 | 4 min | Arcanum hoje | Lifecycle, harness, observability, maintenance e gaps. |
| 17:00–20:00 | 3 min | Relações e contratos faltantes | Matriz em quatro linhas; declarar integração ausente. |
| 20:00–28:00 | 8 min | Source trace + `SIMULAÇÃO DE CONTRATO` | Mostrar CURRENT INSPECTED, PROPOSED, EXPECTED e NOT RUN. |
| 28:00–31:00 | 3 min | Onde a máquina para | Acceptance ≠ approval ≠ validation ≠ promotion. |
| 31:00–33:00 | 2 min | Teach-back | Recontar cadeia causal e limites. |
| 33:00–35:00 | 2 min | Composição, não autoevolução | Fecho e decisões seguintes. |
| **Total** | **35 min** |  | Alocação planejada; não ensaiada. |

Teach-back: “Qual a diferença entre a skill textual e o target sigil?”, “Qual superfície registra, qual julga e qual autoriza?”, “Que evidência ainda falta depois de uma candidate proposal?”. Não alegar que as perguntas provaram audience comprehension.

## Source trace + SIMULAÇÃO DE CONTRATO

**Status geral: PROPOSTA, NÃO EXECUTADA.** O source trace exibe `OracleEvidence.metrics` e `ScoreResult.components` como tipos numéricos/booleanos inspecionados e o `sigil-maintenance-loop` como composição registrada/documentada. O fato demonstrável é que nenhuma interface inspecionada conecta `ScoreResult` a reflection, candidate proposal, acceptance ou promotion.

| Elemento | Binding da simulação | Estado |
|---|---|---|
| harness | Contrato público de `experiment-harness`; seria o executor. | CURRENT INSPECTED CONTRACT; **NOT RUN** |
| target sigil | “sigil de revisão de planos”, ainda não selecionado nem ligado a fonte. | UNBOUND PROPOSED TARGET; **NOT RUN** |
| prompt | “Analise este plano de implementação e devolva exatamente: Objetivo, Riscos, Gate de execução e Próximo dono. Se não houver critério de aceite, retorne BLOCK em Gate de execução.” | PROPOSED INPUT |
| fixture | `tdc-missing-acceptance-001`: “Plano: adicionar cache ao agente. Etapas: implementar e publicar.” | PROPOSED; **NOT RUN** |
| expected output | “Objetivo: adicionar cache ao agente\nRiscos: publicação sem critério verificável\nGate de execução: BLOCK — critério de aceite ausente\nPróximo dono: autor do plano” | EXPECTED OUTPUT; **NOT OBSERVED** |
| observation | Signal de quality gap por critério de aceite ausente. | ABSENT; nenhum signal/label/event emitido |
| candidate proposal | Antes: “Gate de execução: informe se o plano pode prosseguir.” Depois: “Gate de execução: retorne BLOCK quando não houver critério de aceite verificável e identifique explicitamente o critério ausente.” | SYNTHETIC PROPOSED EDIT; **NOT APPLIED** |
| user approval | Decisão humana sobre scope exato da mudança. | **NOT REQUESTED** |
| validation | Reexecução de fixtures positivas/negativas e checagem de regressão. | **NOT RUN** |
| promotion | Decisão posterior de lifecycle, distinta de validation. | **NOT EVALUATED** |

### Tabela accept/reject

| Campo | Resultado |
|---|---|
| baseline output | **NOT RUN** |
| candidate output | **NOT RUN** |
| objective / score | **UNBOUND** |
| held-out comparison | **NOT RUN** |
| strict accept/reject outcome | **NOT RUN** |
| user approval | **NOT REQUESTED** |
| validation verdict | **NOT RUN** |
| promotion | **NOT EVALUATED** |

**Fallback:** se não houver antes da palestra uma execução separadamente autorizada, pinada e verificada, apresentar somente esta dry-run de contrato, com a tarja `SIMULAÇÃO DE CONTRATO`. Um transcript pré-capturado só pode ser usado após receipt de execução public-safe. Nunca inventar terminal output nem converter expected labels em observações.

## Matriz claim–evidence

| ID | Claim utilizável | Fonte e seletor exatos | Status / teto |
|---|---|---|---|
| C-SO-METHOD | SkillOpt trata uma skill textual como estado externo treinável de target congelado. | arXiv:2605.23904v2, pp. 4–5, §3.1, Eqs. (1)–(3); p. 5 após Eq. (3); p. 22 Algorithm 1, linhas 1–3 | Paper-defined; não reproduzido. |
| C-SO-LOOP | O loop usa scored rollouts, reflection, bounded edits, merge e strict selection. | p. 4 Figure 2; pp. 5–6 §§3.2–3.5; p. 22 Algorithm 1, linhas 7–27 | Paper-described; não reproduzido. |
| C-SO-RESULT | O paper reporta best ou tied-best em 52/52 células avaliadas. | pp. 7–11, Table 1 e §4.1 “Main Results” / “Headline numbers” | Paper-reported; preservar denominator/baselines/splits; não reproduzido. |
| C-SO-OFFLINE | Otimização é offline; inference usa skill estática sem optimizer calls adicionais, com context-token cost. | pp. 2–3 Introduction; p. 6 §3.7; pp. 13–15 §§4.3–4.4, Table 6 | Propriedade e accounting reportados pelos autores. |
| C-ARC-LIFECYCLE | O corpus inspecionado documenta contratos de lifecycle, validation e human-owned promotion. | `arcanum/framework/SIGIL-DEVELOPMENT-WORKFLOW.md:7-22,182-193`; `arcanum/framework/VALIDATION-EXPERIMENT-PROTOCOL.md:51-68`; `arcanum/definitions/DEFINITIONS.md:396-437` | Inspeção direta de contratos; não runtime. |
| C-ARC-MAINTENANCE | Há composição registrada que observa, reflete, exige aprovação delimitada e valida. | `arcanum/arcana/workflow-reflect/SKILL.md:60-130`; `arcanum/registry/SPELLS.md:7-22`; `arcanum/spells/sigil-maintenance-loop/README.md:1-35,78-110,129-152,179-193` | Registered/documented; não executada nesta pesquisa. |
| C-ARC-SCORE-GAP | Há score-shaped types, mas nenhum wiring inspecionado para improvement de sigils. | `arcanum/arcana/signal-observer/SKILL.md:53-90`; `arcanum/benchmark/src/schemas.ts:57-78`; `arcanum/benchmark/ARCHITECTURE.md:127-177,224-234` | Inspeção direta; ausência limitada às interfaces inspecionadas. |
| C-DEMO | É possível mostrar fonte existente e integração ausente, não comportamento executado. | `arcanum/spells/sigil-maintenance-loop/README.md:80-110,130-150,191-193`; `arcanum/framework/VALIDATION-EXPERIMENT-PROTOCOL.md:51-98` | Source trace e simulation propostos; NOT RUN. |
| C-AUDIENCE | Formato avançado em português, slides + code, 35 minutos. | `arcanum/writing/cfp-tdc-arcanum-skillopt.md:19,29-47,49-55` | Contrato local observado; timing/compreensão não testados. |

## Veredictos dos reviewers e correções resolvidas

| Reviewer gate | Veredicto inicial | Correções incorporadas | Bloqueador restante |
|---|---|---|---|
| Precedent / priority | REVISE | Removeu “first”, “unique”, “missing layer”, self-evolving e superioridade histórica; incluiu GEPA, Trace2Skill, EvoSkill e SkillsBench; substituiu uma camada singular por seis famílias de contratos. | Nenhum para writer; priority continua intencionalmente não alegada. |
| Non-vacuity / witness | REVISE | Renomeou para source trace + `SIMULAÇÃO DE CONTRATO`; separou harness, target, fixture, output, observation, proposal, approval, validation e promotion; adicionou before/after, expected output e tabela NOT RUN. | Demo live/runnable continua bloqueada. |
| Definitional soundness | REVISE | Substituiu equivalência por semelhança estrutural limitada; separou acceptance/approval/validation/promotion; adicionou nota de definição canônica ausente. | Nenhum para writer; canonical definitions permanecem abertas. |
| Recheck conjunto | PASS | Todos os defeitos gate-level acima foram resolvidos sob os claim ceilings. | Nenhum. |

## Alegações proibidas

- Arcanum implementa ou integra SkillOpt.
- Arcanum possui optimizer scalar wired para sigils.
- O source trace é code demo, live demo, runnable demo, optimizer witness ou behavior proof.
- Os resultados de SkillOpt foram reproduzidos; o HEAD atual é o snapshot experimental.
- Signal Observer/telemetry é semantic grader; `ScoreResult` é canonical scalar reward.
- Grader independence/provenance está garantida ou self-authorship é proibido.
- Reflection edita automaticamente; registry presence significa deployed.
- SkillOpt acceptance equivale a user approval, validation, promotion, publication, deployment ou production approval.
- Fixture pass, schema validity ou receipt prova improvement, deployment, produção ou segurança.
- SkillOpt prova transfer universal, ausência de overfitting ou zero prompt-token overhead.
- SkillOpt/Arcanum é first, unique, “the missing layer”, self-evolving ou historicamente superior.
- A palestra cabe em 35 minutos ou produz audience comprehension com base apenas neste plano.

## Decisões abertas

1. **Formato do witness:** escolher entre live verified run, pre-captured verified transcript ou contract simulation. Até existir fixture materializada e receipt de execução, a única opção admissível é `SIMULAÇÃO DE CONTRATO`.
2. **Números nos slides:** recomendação: headline 52/52 com denominator completo e um custo/limite; não reproduzir tabelas extensas.
3. **Benchmark architecture:** usar somente como contraste de score-shaped infrastructure; não tentar SWE-bench ao vivo sem runtime, image, fixture e argumentos pinados.
4. **Target sigil:** selecionar e source-bind um target real em ação futura autorizada ou manter explicitamente o target sintético/unbound.
5. **Reprodução e provenance:** localizar eventual snapshot experimental do SkillOpt ou manter o código atual fora de qualquer alegação de reprodução.
6. **Ensaio:** medir o bloco de oito minutos e o total; só então dizer que a duração foi observada. Audience comprehension requer evidência própria.
7. **Definições:** decidir se `sigil`, `spell` e `capability` serão futuramente promovidos a definições canônicas; este findings não autoriza essa mudança.

## Apêndice de fontes

### Primária — SkillOpt

- Yang, Y. et al. **SkillOpt: Executive Strategy for Self-Evolving Agent Skills**, arXiv:2605.23904v2, 25 maio 2026. PDF imutável: `https://arxiv.org/pdf/2605.23904v2`; SHA-256 verificado pelo explorer: `87f7f0f323b1671e9202b3ebb1596e909e507c71ecd1b360b0075a5ee1727fe3`.
- Repositório author-linked: `https://github.com/microsoft/SkillOpt/tree/ba820b500f9da96685cf2780c7dc85ed4eb6563e`; posterior ao paper e não estabelecido como snapshot experimental.

### Precedentes primários

- GEPA, arXiv:2507.19457.
- Trace2Skill, arXiv:2605.21810v1.
- EvoSkill, arXiv:2603.02766v1.
- SkillsBench, arXiv:2602.12670, versão corrente inspecionada.

### Corpus público Arcanum

- `arcanum/README.md:50-82,105-146,169-177`.
- `arcanum/definitions/DEFINITIONS.md:77-114,183-217,231-266,280-323,340-380,396-437`.
- `arcanum/framework/SIGIL-DEVELOPMENT-WORKFLOW.md:7-22,75-89,146-214`.
- `arcanum/framework/VALIDATION-EXPERIMENT-PROTOCOL.md:18-98`.
- `arcanum/framework/observability/ARCHITECTURE-OVERVIEW.md:9-75,123-181,215-240`.
- `arcanum/arcana/experiment-harness/SKILL.md:47-68,101-118`.
- `arcanum/arcana/signal-observer/SKILL.md:53-90`.
- `arcanum/arcana/workflow-reflect/SKILL.md:60-130`.
- `arcanum/registry/SPELLS.md:7-22`.
- `arcanum/spells/sigil-maintenance-loop/README.md:1-35,78-110,129-152,179-193`.
- `arcanum/benchmark/src/schemas.ts:57-78`.
- `arcanum/benchmark/ARCHITECTURE.md:127-177,224-234`.
- `arcanum/writing/cfp-tdc-arcanum-skillopt.md:19,29-47,49-55` — apenas contrato de formato/audiência; não publicar prosa privada.

## Claim ceiling final

Este documento é research substrate source-bound. Ele sustenta apenas resultados SkillOpt paper-reported e não reproduzidos; contratos, registros e ausências delimitadas inspecionados no corpus público Arcanum; e uma simulação sintética não executada. Não sustenta integração Arcanum–SkillOpt, scalar sigil optimizer, código/live/runnable demo, melhoria comportamental, independência do grader, reprodução, promoção, publication, deployment, produção, prioridade histórica ou audience comprehension.
