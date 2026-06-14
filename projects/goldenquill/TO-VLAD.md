---
to: Vladimir Rondelli
from: Victor (auditoria multi-agente, sintetizada)
re: Reference monitor verificado para uso de ferramentas por agentes — o que está provado e o repo que proponho
date: 2026-06-13
status: rascunho para conversa
---

# Para o Vlad — temos um porteiro de ferramentas para agentes cuja álgebra de decisão é provada em Lean, e ele já roda como CLI

Vlad, isto saiu de uma auditoria multi-agente sobre o `lean-formalization/` desta semana, sintetizada por mim. O enquadramento importa: **não é caça-erro**. É um inventário honesto do que está *de pé* — provado em Lean 4 / Mathlib, sorry-free, build verde (`lake build`, exit 0, hoje 2026-06-13), com axiomas restritos a `propext` / `Quot.sound` / `Classical.choice`. Quero te mostrar onde a confiança realmente mora, porque o valor aqui é localizado e isso é uma virtude, não um defeito.

## A frase única

A confiança no nosso reference monitor não está mais espalhada por "o porteiro inteiro" — ela está concentrada, por construção, em **duas superfícies pequenas e nomeadas**: a cola de parsing na entrada (a *trust border*) e cada regra de matcher; toda a álgebra de decisão que liga essas duas pontas é teorema, não código que você precisa confiar.

## Os achados que sustentam o resto

**1. Um veredito `allow` é correto por teorema — não existe allow falso.**
Evidência: `decidePolicy_sound` (`AgentPermissionKernel.lean:162`) prova que `decidePolicy P r = allow → Satisfies P r`. E o ponto fino: `decidePolicy_allow_iff` (`AgentPermissionKernel.lean:137`) mostra que o monitor *executável* concorda **exatamente** com a spec relacional `Satisfies`, que é definida de forma independente. Isso é o que torna a soundness um teorema de verdade e não um `rfl` disfarçado — a spec e a implementação são objetos separados que provamos coincidir.
Por que importa: a propriedade de segurança que mais queremos ("o monitor nunca concede o que a política proíbe") é a que está CERTIFICADA, não a que está torcendo para dar certo.
O que fazer: este é o teorema-âncora do TRUST-MODEL.md; ele encabeça a coluna CERTIFICADO.

**2. Deny tem precedência não-contornável, e camadas só estreitam autoridade.**
Evidência: `deny_precedence` (`AgentPermissionKernel.lean:170`) — um `forbid` em QUALQUER camada força `deny`, não importa quantas camadas permitam. E `add_layer_restricts` (`AgentPermissionKernel.lean:180`) — adicionar uma camada só pode *narrow* a autoridade (confinamento / no-escalation).
Por que importa: é a garantia de defense-in-depth. Um administrador de tier superior não pode ser "votado a favor" por tiers inferiores.
O que fazer: estas duas são as leis que justificam o modelo de tiers (ver abaixo, na descoberta de design).

**3. Composição de políticas é interseção-de-autoridade — e é literalmente um homomorfismo de monóide.**
Evidência: `decidePolicy_append_allow` (`AgentPermissionKernelComposition.lean:51`) prova `allow(P++Q) ⟺ allow(P) ∧ allow(Q)`. O resultado novo de hoje vai além: em `AgentPermissionKernelAlgebra.lean`, `decidePolicy_append_meet` (`:90`) e `decidePolicy_flatten_meet` (`:98`) provam que `decidePolicy` é um **homomorfismo de monóide** de (camadas, `++`, `[]`) para (`Decision`, `meet`, `allow`). Compor N tiers vira o `meet` (fold) das decisões: associatividade, identidade e composição de N-tiers saem de graça. Sorry-free, axiomas `[propext, Quot.sound]`.
Por que importa: a composição não é um caso especial frágil — é uma estrutura algébrica. Mas há uma armadilha embutida e honesta: `allow` é a **identidade** do monóide, ou seja, a política vazia é o elemento neutro e a *mais permissiva*. Isso é **fail-open algébrico**. Não é um bug do teorema; é uma consequência da álgebra que o **border tem de rejeitar** (e rejeita — ver achado 5).
O que fazer: registrar essa identidade como exatamente o motivo pelo qual o border recusa política vazia. A álgebra te diz onde está o footgun.

**4. Defesa contra path-traversal é teorema, com confinamento provado.**
Evidência: `normalize_clean` (`AgentPermissionKernelArgs.lean:129`) — todo path normalizado é livre de `..`, `.` e segmento vazio. `normalize_idempotent` (`:150`) — normalizar é fixed-point, então temos representantes canônicos genuínos. As testemunhas concretas: `prefix_confusion_defended` (`:175`, `/workspace/**` não casa `/workspace-evil`) e `dotdot_escape_defended` (`:181`). E o fecho: `read_confined` (`AgentPermissionKernelConfinement.lean:82`) — se a regra Read dispara, o prefixo concedido é *genuinamente ancestral* do path normalizado; não há como escapar.
Por que importa: as três classes clássicas de evasão de path (`../`, `.`, `//`) estão discharged como matemática, não como uma lista de regex que torcemos para estar completa.
O que fazer: este bloco é a vitrine. É o argumento mais legível para alguém de fora de que "verificado" aqui significa algo.

**5. Não é um Cedar re-skin, e o executável existe e falha fechado.**
Evidência (não-Cedar): `layered_not_flattenable` (`AgentPermissionKernel.lean:202`) é **axiom-free** (`by decide`) — exibe uma requisição onde a semântica em-camadas e a Cedar-achatada discordam. Certifica que nossa semântica não é expressável achatando tudo num único set. Evidência (executável): `PermGuard.lean` é o CLI `permguard [--explain] <policy.json> <request.json>`, que roda o `decidePolicy` provado e é **FAIL-CLOSED** — parse falha → exit 2, nunca `allow`. O ÚNICO código não-verificado é o parser JSON, isolado atrás de um banner "TRUST BORDER". Verificado e2e pelo binário, 7/7 (incluindo a defesa de `..`).
Por que importa: "provado em Lean" sem binário é teatro; "binário" sem o teorema é só mais um gatekeeper. Temos os dois, e a fronteira entre eles está fisicamente marcada no código.
O que fazer: o banner TRUST BORDER vira o contrato visual do repo inteiro.

## O trust-model — a espinha (e o que eu peço que você verifique como verificador)

Esta é a parte em que mais preciso do seu olho. A disciplina é **claim ≤ proof**: distinguir o que está CERTIFICADO do que está só ASSUMIDO.

- **CERTIFICADO** (Lean, sorry-free): a álgebra de decisão (deny-precedence, composição-interseção, sem allow falso — achados 1–3); a normalização de path (`..`/`.`/`//`-free + idempotente, achado 4); o confinamento de path; a soundness relacional do matcher (`matchesGlob_iff` em `AgentPermissionKernelGlobSpec.lean`); e a separação de tipo Bash/path — `cmdMatchesPrefix` + `mkBashRule` em `AgentPermissionKernelBash.lean` são um matcher flat, *type-separado* do glob de path, porque o `*` do Bash não é o `*` segmentado.

- **ENFORÇADO NO BORDER** (checks do parser, fail-closed — *não* são teoremas, são guardas de runtime): política não-vazia (recusa allow-all — exatamente o fail-open algébrico do achado 3); e proibição de `/` dentro de um segmento.

- **ASSUMIDO** (preconditions *declaradas*, NÃO certificadas — esta lista é o perímetro honesto): resolução de `realpath`/symlink; TOCTOU; case-fold do filesystem + Unicode NFC; quoting e word-splitting de shell; `*` no meio de string; a *intenção* de quem escreve a política; e ausência de limite de tamanho/profundidade.

Vlad, o pedido concreto: **ataque a coluna ASSUMIDO**. Se um item de lá puder ser promovido a CERTIFICADO ou a ENFORÇADO-no-border, ótimo. Mas o que eu *não* quero é que algum dia alguém leia "verificado" e ache que symlink/TOCTOU/NFC estão cobertos. Eles não estão, e a honestidade sobre isso é metade do valor.

## O que eu deixo em aberto para você decidir

- **O nome do repo.** É decisão sua/nossa. Candidatos: **Limen** (latim "limiar", a fronteira em si) · **Portcullis/Cullis** (a grade medieval que cai = fail-closed literal) · **Janus** (deus dos portões, duas faces = allow/deny) · **Custos** (latim "guardião") · **Claustrum** (clausura — espelha `read_confined`) · **Keep** (o torreão = o core verificado) · **Sequent** (cálculo de sequentes, ângulo Lean) · **Verdict**. Minha recomendação atual: **Limen, Cullis ou Janus**.
- **O default do schema de tiers.** A descoberta de design (abaixo) sugere um default, mas quero seu voto antes de cravar.
- **O gate numérico do E1.** Proponho 0 divergências em N=10k; você pode achar que precisa de mais.

## Descoberta de design (registrar no repo)

As camadas são **tiers de governança** (org → project → user), **não** uma-camada-por-ferramenta. Sob interseção-de-autoridade (achado 3), se você modelar uma camada por ferramenta, qualquer camada que *abstém* sobre uma ferramenta mata o `∀`-permit e **nega tudo**. Então o schema precisa fazer "um tier cobre todas as ferramentas" o *default*, ou políticas ingênuas viram deny-all silencioso. Isso vira o experimento E4.

## Próximos passos concretos, em ordem de alavancagem

1. **TRUST-MODEL.md** — a espinha CERTIFICADO / ENFORÇADO / ASSUMIDO, exatamente nas três colunas acima. Maior alavancagem porque é o documento que impede inflação futura.
2. **Estrutura do repo**: core Lean verificado isolado em `lean/`; cola não-verificada em quarentena em `border/` (parser + realpath/NFC/case-fold); `tools/` (outros métodos); `policies/` (exemplos org/project/user); `tests/{differential,property,e2e}`.
3. **README honesto** + uma **"constituição-lite" de 5 leis**, cada uma enforçável por gate: L1 `claim ≤ proof`; L2 border fail-closed; L3 nenhuma lógica de decisão fora do core provado; L4 toda suposição declarada; L5 todo change no border passa por teste diferencial.
4. **PHASED-PLAN com gates** + os 4 experimentos, todos atados ao risco real — que está no BORDER, não nas provas:
   - **E1 (diferencial)**: cola escrita à mão vs `decidePolicy` provado como oráculo, fuzz de `(policy, request)`. Gate: 0 divergências em N=10k.
   - **E2 (propriedade)**: `border/canon` vs `normalize` provado, em paths fuzzados.
   - **E3 (adversarial/e2e)**: corpus do red-team passado pelo binário `permguard`. Gate: 100% fail-closed.
   - **E4 (footgun de tiers)**: medir com que frequência políticas ingênuas uma-camada-por-ferramenta negam-tudo → decide o default do schema (a descoberta acima).

Mantenha o dia-1 mínimo: atenuação ≤ 7 regras. Não queremos um repo que prometa mais regras do que provamos.

## Uma observação além da auditoria

O que eu acho mais bonito aqui não é nenhum teorema individual — é que o trabalho de verificação **moveu fisicamente a fronteira de confiança**. Antes, confiar no porteiro era confiar em tudo: a lógica de decisão, o parsing, o matching, a composição. Agora a álgebra inteira é teorema, e a confiança encolheu para duas superfícies que cabem num parágrafo: a cola de entrada e cada regra de matcher. Isso é, no fundo, o que formalização *deveria* entregar e quase nunca entrega — não "é tudo seguro", mas "aqui, exatamente nestes dois lugares pequenos, é onde você ainda precisa olhar". A `trust border` no `PermGuard.lean` é essa ideia feita banner. O repo inteiro deveria ser uma máquina para manter essa fronteira pequena e visível.

— V.
