# Findings — aplicabilidade de categorias infinitas, cocadeias e cohomologia

Data: 2026-07-23  
Escopo: DomainSpec, CyberAlchemy v2, Arcanum, loop de evidência, probes e resíduos, Inventory/Ontology, dispatch/observabilidade e experimentos  
Natureza: pesquisa privada; sem promoção de autoridade ou implementação

## Veredito executivo

O resultado é negativo no nível arquitetural e seletivamente positivo no nível matemático local:

1. **Nenhum candidato a \((\infty,1)\)-categoria sobrevive ao teste atual de não-vacuidade.**
2. **Nenhum candidato a complexo geral de cocadeias sobrevive ao teste atual de não-vacuidade.**
3. Portanto, recomenda-se **nenhuma mudança agora** em arquitetura, autoridade, vocabulário canônico, schema, runtime público de Arcanum ou implementação. A ausência de uma testemunha que mude um resultado operacional é a razão do bloqueio; a disponibilidade de matemática mais expressiva não basta ([research.md, Agent 1](research.md#agent-1--riehl-emily); [research.md, Agent 2](research.md#agent-2--quillen-daniel); [research.md, Agent 3](research.md#agent-3--shannon-claude)).
4. Há **exatamente dois usos matemáticos atualmente justificados**:
   - `domainspec-lean-formalization/lean-formalization/FunctorialResidueStructure.lean:76-165,253-319,449-608`: testemunha de **categoria ordinária, funtor, extensão de Kan e colimite**. Ela mostra que fibras ou contagens iguais podem ocultar MERGE versus SEPARATE enquanto um mapa sensível ao colimite distingue os casos. **Não** é uma afirmação de Čech, feixe ou cohomologia ([research.md, Agent 2](research.md#agent-2--quillen-daniel); [research.md, Agent 3](research.md#agent-3--shannon-claude)).
   - `domainspec-lean-formalization/lean-formalization/CoupledSkewTower.lean:83-199,264-315` e `domainspec-lean-formalization/lean-formalization/CoupledSkewTowerLift.lean:142-238`: testemunhas de **cociclos não abelianos dinâmicos finitos** e equivalência por transferência, incluindo exemplos não equivalentes por transferência. “Não cohomólogos” só é admissível nesse sentido explícito de equivalência de cociclos não abelianos; não designa um grupo de cohomologia nem um complexo geral de cocadeias ([research.md, Agent 3](research.md#agent-3--shannon-claude)).

Não se reivindica novidade. Toda construção considerada tem precedente matemático ou depende de um que deve ser nomeado. Encontrar um owner matemático é sempre um resultado positivo de precedência; **precedente nunca é razão para KILL**. KILL significa apenas que a aplicação local ainda carece de tipos, testemunha discriminante, condição de soundness ou vantagem sobre o modelo mínimo vigente.

## Primer para quem chega agora

### Categorias ordinárias

Uma categoria ordinária tem objetos, morfismos entre objetos, identidades e composição associativa. Entre dois objetos há um **conjunto** de morfismos. Funtores preservam identidades e composição. Transformações naturais comparam funtores. Esse nível já suporta o modelo implementado em `FunctorialResidueStructure.lean`, inclusive seu funtor, extensão de Kan e colimite; não há ali necessidade demonstrada de morfismos de dimensão superior ([research.md, Agent 1](research.md#agent-1--riehl-emily); `domainspec-lean-formalization/lean-formalization/FunctorialResidueStructure.lean:76-165,253-319,449-608`).

### Bicategorias e 2-categorias

Uma bicategoria acrescenta 2-células entre 1-morfismos. Composição e unidades valem até isomorfismos coerentes — associadores e unitors — e não necessariamente por igualdade literal. Uma 2-categoria estrita é o caso em que essas leis são igualdades estritas ([Leinster, *Basic Bicategories*](https://arxiv.org/abs/math/9810017)). Por isso, `Para_M(C)` deve ser chamado de **bicategoria por padrão**; “2-categoria estrita” só é admissível depois de uma prova de estricidade. O precedente de `Para` a partir de uma actegory é positivo ([Capucci–Gavranović, *Actegories for the Working Amthematician*](https://arxiv.org/abs/2203.16351)), mas reparametrizações como 2-células verticais, sem composição horizontal, identidades, associadores/unitors e interchange, ainda não completam sequer essa estrutura ([research.md, Agent 3](research.md#agent-3--shannon-claude)).

### Categorias infinitas

Uma \((\infty,1)\)-categoria substitui hom-sets por **mapping spaces**: pontos são 1-morfismos, caminhos são 2-morfismos invertíveis, caminhos entre caminhos são 3-morfismos e assim por diante. Composição é homotopy-coherent, não apenas uma operação estrita. Uma aplicação local só é necessária se esses dados superiores mudarem um resultado que a projeção ordinária ou bicategórica não distingue. Um grafo rico, um pipeline recursivo, um loop, várias descrições do mesmo objeto ou uma sequência de reescritas não produzem essa necessidade automaticamente ([Riehl–Verity, *Elements of ∞-Category Theory*](https://emilyriehl.github.io/files/elements.pdf); [Kerodon, definição](https://kerodon.net/tag/0039); [research.md, Agent 1](research.md#agent-1--riehl-emily)).

Na localização de Dwyer–Kan, parte-se de uma **categoria relativa real** \((C,W)\): \(C\) contém objetos e morfismos e \(W\) é uma classe declarada de equivalências fracas. A localização simplicial retém mapping spaces de zigzags e relações superiores, enquanto sua \(\pi_0\) recupera a localização ordinária. Se o mapping space localizado for discreto, ou se apenas \(\pi_0\) afetar o sistema, a localização ordinária basta ([Dwyer–Kan](https://people.math.rochester.edu/faculty/doug/otherpapers/dwyer-kan-1.pdf); [research.md, Agent 1](research.md#agent-1--riehl-emily)).

### Cocadeias, complexos e cohomologia

Uma **cocadeia** de grau \(n\) é um elemento de um portador aditivo \(C^n\). Um **complexo de cocadeias** requer mapas tipados

\[
d^n:C^n\longrightarrow C^{n+1}
\quad\text{com}\quad
d^{n+1}\circ d^n=0.
\]

Os cociclos são \(Z^n=\ker d^n\), os cobordos são \(B^n=\operatorname{im}d^{n-1}\), e a cohomologia é \(H^n=Z^n/B^n\). Uma lista de estágios, deltas, métricas ou registros não é um complexo: faltam portadores aditivos, diferenciais tipados e a lei \(d^2=0\) ([Stacks Project, complexes](https://stacks.math.columbia.edu/tag/010V); [research.md, Agent 2](research.md#agent-2--quillen-daniel)).

Em Čech, escolhem-se uma cobertura, interseções, mapas de restrição e coeficientes aditivos. \(C^p\) agrega dados sobre interseções de \(p+1\) abertos e \(d\) é a soma alternada das restrições. **\(H^0\) é o grupo das famílias locais compatíveis (0-cociclos); identificá-lo com seções globais/colagem requer as hipóteses relevantes de feixe e cobertura.** \(H^1\) é dependente da cobertura e só carrega uma leitura de transição, torsor ou obstrução global quando a construção correspondente foi tipada. Nunca se deve dizer genericamente que “\(H^1\) é falha de colagem” ([Stacks Project, Čech](https://stacks.math.columbia.edu/tag/01ED); [research.md, Agent 2](research.md#agent-2--quillen-daniel)).

## Fronteira de fontes e evidência

Este relatório sintetiza a transcrição congelada em `research/2026-07-23-infinity-category-cochain-applicability/research.md`. Os três retornos cumprem papéis distintos: teoria de categorias infinitas, teoria de cocadeias/cohomologia e cartografia repo-wide. Inventory foi usado apenas como índice de descoberta e é explicitamente um read model de cobertura parcial; não é autoridade matemática nem autoridade de promoção ([research.md, Agent 3](research.md#agent-3--shannon-claude)).

As fontes externas sustentam definições e precedentes; os caminhos locais sustentam o estado do repositório. Uma aplicação local só passa quando ambos se encontram em uma fixture tipada com controle negativo. Busca textual não prova ausência semântica, mas a inspeção estrutural encontrou objetos, setas, resíduos e resultados atuais sem qualquer fixture cuja saída dependa de homotopia superior ou de um \(H^n\) geral ([research.md, Agent 3](research.md#agent-3--shannon-claude)).

## Mapa repo-wide de aplicabilidade

O mapa não se limita à aposta de funtores:

| Superfície | Modelo mínimo atual | Classe | Decisão |
|---|---|---|---|
| DomainSpec v2 | grafo tipado finito; composição ainda não é autoridade | analogia adjacente | KILL acima de categoria ordinária; `projects/domainspec-v2/definitions/reviews/2026-07-12-category-law-formalization-route.md:13-45` |
| Resíduo funtorial | categoria ordinária, funtor, Lan e colimite | **uso real** | KEEP estrito; sem leitura Čech/feixe; `domainspec-lean-formalization/lean-formalization/FunctorialResidueStructure.lean:76-165,253-319,449-608` |
| Probes e oracle | relações, escalares, vetores, streams e harness | no-fit | KILL cochain/\(\infty\); `domainspec-lean-formalization/PROBES.md:9-33,37-77` |
| Golden chain/self-harness | DAG, ledger append-only, fixtures e verificador | no-fit | KILL: o gap é soundness do verificador, não matemática superior ([research.md, Agent 3](research.md#agent-3--shannon-claude)) |
| `Para_M(C)` | reparametrizações 2-dimensionais incompletas | candidato witness-only | precedente bicategórico/actegórico positivo; KILL conclusão/promoção ([research.md, Agent 3](research.md#agent-3--shannon-claude)) |
| Coupled skew towers | ação de grupo finita, cociclo e transferência | **uso real** | KEEP estrito; sem complexo geral; `domainspec-lean-formalization/lean-formalization/CoupledSkewTower.lean:83-199,264-315`; `domainspec-lean-formalization/lean-formalization/CoupledSkewTowerLift.lean:142-238` |
| Views/claims em Čech | validadores diretos, proveniência e solver | candidato witness-only | KILL aplicação atual ([research.md, Agent 2](research.md#agent-2--quillen-daniel)) |
| Contextualidade | ainda sem context store/presheaf executável | pesquisa prerequisite-gated | KILL implementação ([research.md, Agent 2](research.md#agent-2--quillen-daniel)) |
| Information cohomology/Assay | surprisal escalar e claim graph | pesquisa prerequisite-gated | KILL implementação ([research.md, Agent 2](research.md#agent-2--quillen-daniel)) |
| Extensão/obstrução governada | blockers, gates e métricas | analogia adjacente | KILL “classe de obstrução governada” ([research.md, Agent 2](research.md#agent-2--quillen-daniel)) |
| Rung 3 | witness atual `Subsingleton`/cardinalidade | analogia adjacente | KILL leitura \(\infty\); `domainspec-lean-formalization/lean-formalization/RungThreeLaxFibered.lean:82-126,151-241` |
| Localização de traduções | nenhuma categoria relativa \((T,W)\) operacional | candidato witness-only | KILL aplicação atual ([research.md, Agent 1](research.md#agent-1--riehl-emily)) |
| Agregação experimental | conjuntos/escalares e diagramas estritos | candidato witness-only | KILL homotopy aggregation atual ([research.md, Agent 1](research.md#agent-1--riehl-emily)) |
| Arcanum dispatch/observabilidade | DAG, waves, gates, receipts e JSONL | no-fit público | KILL categoria infinita/cochain; `arcanum/formulae/dispatch-spec/dispatch.schema.json` |
| Inventory/Ontology/CAV2 authority | grafo tipado, IDs, proveniência e ordem de promoção | no-fit | KILL categoria infinita ([research.md, Agent 3](research.md#agent-3--shannon-claude)) |

Essa classificação separa quatro estados:

- **Uso real:** há construção local tipada e resultado demonstrado — apenas o resíduo funtorial ordinário e os cociclos finitos das coupled skew towers.
- **Analogia adjacente:** o vocabulário ilumina uma forma, mas o modelo vigente já carrega toda a decisão.
- **Witness-only:** há precedente positivo e uma pergunta falsificável, porém nenhum direito a arquitetura ou implementação.
- **KILL:** a aplicação ou framing atual não satisfaz tipos, não-vacuidade ou soundness. O termo pode voltar somente com a fixture indicada.

## Avaliação separada: categorias infinitas

### Resultado

Nenhuma aplicação atual exige mapping spaces não discretos, 3-células operacionais, coerência ilimitada, localização simplicial ou limites homotópicos. DomainSpec, Saturn/loop de evidência, Arcanum, Inventory/Ontology, probes e experimentos são atualmente cobertos por grafos tipados, categorias ordinárias, DAGs, máquinas de estado, relações, vetores e ledgers ([research.md, Agent 1](research.md#agent-1--riehl-emily); [research.md, Agent 3](research.md#agent-3--shannon-claude)).

### `Para_M(C)`: limite em dimensão 2

Há precedente positivo bicategórico/actegórico para modelar mapas parametrizados e reparametrizações ([Leinster, *Basic Bicategories*](https://arxiv.org/abs/math/9810017); [Capucci–Gavranović, *Actegories for the Working Amthematician*](https://arxiv.org/abs/2203.16351)). Isso não autoriza completar ou promover a arquitetura. O máximo autorizado é uma tentativa limitada de witness: construir dois mapas parametrizados componíveis e duas reparametrizações que coincidam nos checks isolados, mas colidam sob composição horizontal; então provar que interchange/coerência muda uma saída observável.

Até essa colisão:

- chamar a estrutura de **bicategoria**;
- reservar “2-categoria estrita” para o caso em que associatividade, unidades e interchange sejam provadas estritamente;
- não inferir \(\infty\)-categoria a partir de 2-células;
- manter KILL sobre conclusão, promoção, vocabulário canônico e implementação ampla ([research.md, Agent 3](research.md#agent-3--shannon-claude)).

### Dwyer–Kan e agregação homotópica

Uma aplicação de Dwyer–Kan requer:

1. categoria relativa tipada \((T,W)\);
2. leis e evidência de que \(W\) são equivalências fracas relevantes;
3. mapping space localizado não discreto;
4. dois casos iguais em \(T[W^{-1}]\), mas operacionalmente distintos pela informação superior.

Sem o item 4, a localização ordinária vence. Analogamente, homotopy aggregation requer um diagrama real de protocolos e um observável para o qual pullback estrito e homotopy pullback divergem. Se os espaços forem discretos ou as duas agregações coincidirem, a agregação estrita vence ([Dwyer–Kan](https://people.math.rochester.edu/faculty/doug/otherpapers/dwyer-kan-1.pdf); [Kerodon, limits and colimits](https://kerodon.net/tag/02VY); [research.md, Agent 1](research.md#agent-1--riehl-emily)).

### KILL explícito

Ficam KILL agora:

- Arcanum, Inventory ou loop de evidência “como uma categoria infinita”;
- feedback, recursão ou múltiplos caminhos “como coerência superior”;
- rung 3 “como leitura infinita”;
- localização Dwyer–Kan sem \((T,W)\) e mapping space discriminante;
- agregação homotópica sem divergência operacional em relação à baseline estrita.

## Avaliação separada: cocadeias e cohomologia

### Resultado

Não existe fixture repo-wide com um pacote \((C^n,d)\), prova \(d^2=0\) e resultado DomainSpec/CAV2/Arcanum que dependa de sua classe de cohomologia. O único uso local de “cohomologous” que permanece é a equivalência não abeliana finita por transferência nas coupled skew towers; ele não é evidência de um complexo geral ([research.md, Agent 3](research.md#agent-3--shannon-claude)).

### Čech de views reais

Čech é apenas witness-only. Uma tentativa válida deve nomear views reais \(U_i\), suas interseções, restrições e um presheaf de coeficientes aditivos; construir \(C^p\), o diferencial alternado e a prova \(d^2=0\); incluir caso \(H^1=0\) e caso \(H^1\neq0\); e demonstrar uma decisão operacional que um verificador direto de ciclos/constraints não encontra.

Os guardrails são obrigatórios:

- a cohomologia de Čech é relativa à cobertura escolhida;
- \(H^0\) é o grupo das famílias locais compatíveis (0-cociclos); identificá-lo com seções globais/colagem requer as hipóteses relevantes de feixe e cobertura;
- \(H^1\) não significa genericamente “falha de colagem”;
- a leitura de \(H^1\) deve vir de transições, torsors ou de uma extensão global precisamente tipada ([Stacks Project, Čech](https://stacks.math.columbia.edu/tag/01ED); [research.md, Agent 2](research.md#agent-2--quillen-daniel)).

O witness de `FunctorialResidueStructure.lean` continua sendo a baseline mais simples para “estrutura supera contagens”. Ele não pode ser rebatizado como Čech ou sheaf ([research.md, Agent 2](research.md#agent-2--quillen-daniel)).

### Contextualidade

Contextualidade cohomológica é pesquisa prerequisite-gated: primeiro deve existir um context store, contexts de medição, restrições e um presheaf executável. Depois, o teste deve ser comparado a SAT/CSP. Um obstruction class não nulo pode certificar contextualidade, mas zero **não** libera nem certifica não-contextualidade; a obstrução é one-sided ([Abramsky–Brandenburger](https://arxiv.org/abs/1102.0264); [Abramsky–Mansfield–Barbosa](https://arxiv.org/abs/1111.3620); [research.md, Agent 2](research.md#agent-2--quillen-daniel)). Implementação agora: KILL.

### Information cohomology

Information cohomology não é “entropia com graus”. Requer o substrato real da teoria: semilattice condicional de observáveis, operação de joint measurement, probability functor estável sob conditioning, módulos probabilísticos e bar complex com seu coboundary. Sem esse substrato, surprisal de tokens, gzip, mutual information escalar ou claim graph não constituem a teoria ([Vigneaux](https://arxiv.org/abs/1709.07807); [Baudot–Bennequin](https://www.mdpi.com/1099-4300/17/5/3253); [research.md, Agent 2](research.md#agent-2--quillen-daniel)). Implementação agora: KILL.

### KILL explícito

Ficam KILL agora:

- pipeline, ledger, oracle ou golden chain “como um complexo”;
- delta entre estágios “como diferencial” sem portadores aditivos e \(d^2=0\);
- derived global sections sem site, feixe abeliano, funtor left-exact e resolução;
- “governed obstruction class” sem problema real de lifting/extensão e sistema de coeficientes;
- contextualidade antes do context store;
- information cohomology antes do substrato observável/probabilístico/bar;
- generalizar as coupled skew towers a partir de conjugação de palavras periódicas.

## Obrigações tipadas e fixtures mínimas discriminantes

### Para qualquer proposta de categoria infinita

Deve-se fornecer:

1. objetos, 1-morfismos e o modelo de mapping spaces;
2. células superiores concretas e suas leis de composição;
3. um observable local que dependa dos dados superiores;
4. fixture positiva e controle em que os mapping spaces colapsam a conjuntos discretos;
5. comparação contra categoria ordinária, bicategoria ou categoria enriquecida em espaços.

O mínimo discriminante é um par de casos com a mesma projeção ordinária/bicategórica, mas saídas distintas por coerência superior. Sem isso, KILL ([research.md, Agent 1](research.md#agent-1--riehl-emily)).

### Para qualquer proposta de complexo de cocadeias

Deve-se fornecer:

1. graduação nomeada e portadores aditivos ou preaditivos \(C^n\);
2. diferenciais tipados \(d^n:C^n\to C^{n+1}\);
3. prova de \(d^{n+1}d^n=0\);
4. kernels, images e semântica do quociente \(H^n\);
5. mapa sound de artefatos reais para cocadeias;
6. justificativa de por que cobordos são reparametrizações inócuas, e não perda real;
7. caso não nulo e caso de colapso;
8. comparação contra solver direto, cálculo de ciclo, relação, vetor ou ledger.

Para derived functors, obstruction theory, Čech e information cohomology somam-se as estruturas específicas já listadas. Sem qualquer item, o uso é no máximo metafórico ([research.md, Agent 2](research.md#agent-2--quillen-daniel)).

### Teto das coupled skew towers

Qualquer generalização deve, além de reproduzir os exemplos atuais, exibir um resultado downstream não recuperável por palavra de período/conjugação ou pela relação de transferência finita. Não é sound extrapolar de periodic conjugacy para um grupo de cohomologia geral ([research.md, Agent 3](research.md#agent-3--shannon-claude)).

## Matriz de vereditos

| Candidato | Owner positivo | Witness atual | Condição de soundness | Veredito |
|---|---|---|---|---|
| Resíduo funtorial | teoria ordinária de categorias/Kan/colimites; formalização DomainSpec | `domainspec-lean-formalization/lean-formalization/FunctorialResidueStructure.lean:253-319,539-608` ([research.md, Agent 2](research.md#agent-2--quillen-daniel)) | manter leitura ordinária; não chamar de Čech/feixe | **KEEP** |
| Coupled skew towers | cociclos não abelianos dinâmicos; formalização DomainSpec | `domainspec-lean-formalization/lean-formalization/CoupledSkewTower.lean:83-199,264-315`; `domainspec-lean-formalization/lean-formalization/CoupledSkewTowerLift.lean:142-238` ([research.md, Agent 3](research.md#agent-3--shannon-claude)) | “não cohomólogos” só na equivalência explícita de cociclos | **KEEP** |
| `Para_M(C)` | precedente bicategórico/actegórico ([Capucci–Gavranović](https://arxiv.org/abs/2203.16351)); pesquisa CAV2 | reparametrizações verticais, sem horizontal/interchange ([research.md, Agent 3](research.md#agent-3--shannon-claude)) | composed-map collision deve mudar output; bicategoria por padrão | **KILL promoção; WITNESS-ONLY** |
| Views em Čech | Čech para presheaves abelianos; [Stacks](https://stacks.math.columbia.edu/tag/01ED) | nenhum caso repo real tipado ([research.md, Agent 2](research.md#agent-2--quillen-daniel)) | views/restrições/coeficientes, \(d^2=0\), \(H^1=0/\neq0\), superar solver | **KILL atual; WITNESS-ONLY** |
| Localização \((T,W)\) | [Dwyer–Kan](https://people.math.rochester.edu/faculty/doug/otherpapers/dwyer-kan-1.pdf) | nenhuma categoria relativa operacional ([research.md, Agent 1](research.md#agent-1--riehl-emily)) | mapping space não discreto deve mudar resultado | **KILL atual; WITNESS-ONLY** |
| Agregação homotópica | higher limits/colimits; [Kerodon](https://kerodon.net/tag/02VY) | nenhum protocolo space-valued ([research.md, Agent 1](research.md#agent-1--riehl-emily)) | pullback homotópico deve superar baseline estrita | **KILL atual; WITNESS-ONLY** |
| Contextualidade | Abramsky–Brandenburger e extensões | sem context store/presheaf ([research.md, Agent 2](research.md#agent-2--quillen-daniel)) | comparar a SAT/CSP; não nulo certifica, zero não libera | **KILL implementação; RESEARCH-GATED** |
| Information cohomology | Vigneaux; Baudot–Bennequin | substrato ausente ([research.md, Agent 2](research.md#agent-2--quillen-daniel)) | observáveis, joint measurement, probability module e bar complex reais | **KILL implementação; RESEARCH-GATED** |
| Derived global sections | sheaf cohomology/derived functors | site, sheaf e resolução ausentes ([research.md, Agent 2](research.md#agent-2--quillen-daniel)) | computar \(R^n\Gamma\) sob hipóteses declaradas e superar validator | **KILL** |
| Obstrução governada | obstruction theory clássica | lifting problem e coeficientes ausentes ([research.md, Agent 2](research.md#agent-2--quillen-daniel)) | theorem-backed obstruction para extensão real | **KILL** |
| Pipeline/ledger/oracle como complexo | nenhum owner local porque os tipos não casam | sequência/registro/métricas ([research.md, Agent 2](research.md#agent-2--quillen-daniel)) | exigiria portadores aditivos, diferenciais e \(d^2=0\) | **KILL** |
| Arcanum/Inventory/loop como \(\infty\)-categoria | teoria \(\infty\) existe, mas não é aplicação local | DAG/grafo/estado/ledger ([research.md, Agent 3](research.md#agent-3--shannon-claude)) | dados superiores devem mudar decisão operacional | **KILL** |
| Rung 3 com leitura \(\infty\) | higher category theory adjacente | resultado atual é escalar/Subsingleton; `domainspec-lean-formalization/lean-formalization/RungThreeLaxFibered.lean:82-126,151-241` ([research.md, Agent 3](research.md#agent-3--shannon-claude)) | novo invariante além de cardinalidade e coerência executável | **KILL** |

## Fila limitada de witnesses

A fila é sequencial e não autoriza implementação de produto:

1. **Collision fixture de `Para_M(C)`.** Dois mapas parametrizados componíveis; reparametrizações; composição horizontal; identidade; interchange/coerência; output alterado pela colisão.
2. **Čech de views reais nomeadas.** Views, overlaps, restrições, coeficientes aditivos, \(d^2=0\), caso \(H^1=0\), caso \(H^1\neq0\) e distinção operacional além de cycle checker/SAT/CSP.
3. **Localização de categoria relativa real \((T,W)\).** Mapping space localizado não discreto e efeito operacional além da localização ordinária.
4. **Protocolo não discreto: pullback estrito versus homotópico.** Resultado observável distinto.
5. **Teste de contextualidade.** Somente depois de existir context store; comparar contra SAT/CSP; classe zero não é clearance.
6. **Information cohomology.** Por último entre as novas estruturas; somente após existir todo o substrato observável, probabilístico, modular e bar.
7. **Teto das coupled skew towers.** Executar somente se alguém propuser generalização; exigir resultado não reduzível a transferência finita/conjugação periódica.

Falhar uma fixture é um resultado válido e encerra aquele ramo. Passar uma fixture autoriza revisão do veredito, não promoção automática.

## Fronteira pública/privada

Esta pesquisa e seus seletores de DomainSpec/CAV2 são privados. Nada aqui deve ser projetado como capacidade entregue por Arcanum. O runtime público continua governado por DAGs, waves, joins/gates, receipts e observabilidade append-only, conforme `arcanum/formulae/dispatch-spec/dispatch.schema.json` e `.arcanum/observability/README.md:1-8`. Em particular:

- não adicionar vocabulário de \(\infty\)-categoria ou cohomologia a Arcanum;
- não importar prosa privada de DomainSpec, Saturn ou CAV2 para `arcanum/`;
- não tratar candidatos de pesquisa como schema, runtime ou autoridade;
- não promover definições antes de fixture, owner, soundness e gate explícitos.

## Questões residuais

1. Qual ambiguidade concreta no modelo ordinário de `Para_M(C)` não pode ser resolvida por equações ou por uma bicategoria já coerente?
2. Existem três views reais, já mantidas pelo repo, cujas restrições formem um ciclo e para as quais um solver direto seja insuficiente?
3. Qual conjunto \(W\) de traduções tem semântica de equivalência fraca verificada, em vez de mera aprovação por receipt?
4. Que protocolo produz witness spaces não discretos, e qual decisão muda entre pullback estrito e homotópico?
5. Qual context store poderia instanciar contextualidade sem confundir incompatibilidade lógica comum com obstrução cohomológica?
6. Há uma razão operacional para construir o substrato completo de information cohomology que supere surprisal, informação mútua e testes multivariados diretos?
7. Alguma generalização das coupled skew towers distingue casos que a conjugação da palavra de período e a transferência finita não distinguem?

## Disposição final

| Ação | Disposição |
|---|---|
| Manter `FunctorialResidueStructure.lean` como witness ordinário de funtor/Kan/colimite | **KEEP** |
| Manter `domainspec-lean-formalization/lean-formalization/CoupledSkewTower.lean` e `domainspec-lean-formalization/lean-formalization/CoupledSkewTowerLift.lean` como casos finitos de cociclo não abeliano/transferência | **KEEP** |
| Alterar arquitetura, autoridade, vocabulário, schema, Arcanum público ou implementação | **STOP / NO CHANGE** |
| Promover `Para_M(C)`, Čech, Dwyer–Kan, homotopy aggregation, contextualidade ou information cohomology | **KILL agora** |
| Rebatizar pipeline/ledger/oracle como complexo, ou Arcanum/Inventory/loop como \(\infty\)-categoria | **KILL** |
| Alegar novidade | **PROIBIDO; não reivindicada** |
| Tratar precedente matemático como motivo de KILL | **PROIBIDO; owner é evidência positiva** |

**Próxima ação:** executar somente o primeiro witness limitado — a collision fixture de `Para_M(C)` — se e quando o modelo ordinário produzir uma ambiguidade concreta. Caso contrário, parar.
