---
document_family: product_research_blueprint
idea_name: Ontologize para Inteligência Comercial do 80VinteBot
status: proposta para descoberta
prepared_on: 2026-07-16
language: pt-BR
audience:
  - fundadores
  - liderança de produto
  - liderança comercial
  - liderança de engenharia
---

# Ontologize para o 80VinteBot

## Transformar conversas de vendas em conhecimento comercial utilizável

> **Status desta proposta:** material para uma conversa de descoberta. Não é contrato, integração pronta, auditoria, certificação ou promessa de resultado comercial.

**Em uma frase:** o Ontologize transforma conversas de vendas em um mapa estruturado e revisável de intenções, necessidades, objeções, lacunas de qualificação, próximos passos e resultados, sempre ligado às evidências que deram origem a cada interpretação.

## Resumo executivo

O 80VinteBot já trabalha no ponto em que grande parte da inteligência comercial nasce: a conversa com o cliente. O desafio é que, depois da conversa, muito desse conhecimento pode ficar preso em históricos, campos isolados do CRM ou na memória de quem acompanhou o atendimento.

O Ontologize propõe uma camada de inteligência comercial que organiza esse material em um mapa comum. Em vez de registrar apenas que um lead foi qualificado, o mapa pode mostrar:

- o que a pessoa queria resolver;
- quais necessidades foram confirmadas;
- quais objeções apareceram;
- quais critérios sustentaram a qualificação;
- o que ainda ficou sem resposta;
- quais promessas e próximos passos foram combinados;
- qual trecho da conversa sustenta cada interpretação;
- o que um responsável humano confirmou, contestou ou deixou inconclusivo.

O primeiro passo não seria integrar o Ontologize ao produto nem alterar a operação. Seria executar um teste pequeno, offline e supervisionado sobre uma etapa do funil. O objetivo é descobrir se esse mapa ajuda o time a tomar uma decisão real que hoje exige reler conversas, cruzar registros ou depender de conhecimento tácito.

## O problema em uma cena

Uma conversa termina e o CRM recebe o status **lead qualificado**.

Alguns dias depois, o time quer entender:

- Por que esse lead foi qualificado?
- O interesse foi dito pelo cliente ou inferido pelo atendente?
- Qual pergunta importante não foi feita?
- Existe uma objeção recorrente escondida em outras conversas?
- O próximo passo foi realmente combinado?
- O CRM preservou o que importava ou apenas resumiu o desfecho?

Quando a resposta depende de reler várias conversas manualmente, o conhecimento existe, mas ainda não está pronto para ser usado de forma consistente.

## Cada conversa deixa um mapa, não apenas um histórico

O Ontologize organiza os elementos da conversa e as relações entre eles:

```text
lead
  -> intenção
  -> necessidade
  -> objeção
  -> critério de qualificação
  -> promessa
  -> próximo passo
  -> resultado no funil
```

Cada ligação pode apontar para a mensagem que a originou. Assim, o time não recebe somente uma conclusão gerada por IA. Recebe uma interpretação que pode ser inspecionada, corrigida e aproveitada por pessoas, processos e sistemas.

Esse mapa pode criar uma linguagem comum entre vendas, atendimento, produto e tecnologia. A conversa continua sendo a fonte; o Ontologize torna seu significado mais fácil de consultar e revisar.

## Como seria usar isso

Esta é uma experiência-alvo a ser validada, não uma funcionalidade pronta.

1. O time escolhe uma etapa específica do funil e um conjunto permitido de conversas.
2. O Ontologize identifica os principais elementos comerciais e aponta a evidência de origem.
3. O mapa é comparado com o que foi registrado no CRM ou no processo atual.
4. Um responsável revisa os pontos importantes e marca o que está correto, incorreto ou inconclusivo.
5. O time recebe um retrato das lacunas, divergências, objeções e oportunidades de melhoria.
6. O responsável decide se o resultado merece ser repetido, ajustado, integrado ou encerrado.

## Para quem isso pode ser útil

| Pessoa ou time | Trabalho que o mapa pode apoiar |
| --- | --- |
| Liderança comercial | Entender por que oportunidades avançam, travam ou se perdem |
| Operação de vendas | Encontrar lacunas de qualificação e passagem de contexto |
| Produto | Identificar necessidades e objeções recorrentes com evidência |
| Customer success | Receber contexto melhor sobre promessas e expectativas |
| Engenharia e dados | Trabalhar com conceitos definidos e rastreáveis, não apenas texto livre |
| Fundadores | Avaliar onde a conversa está produzindo ou perdendo conhecimento comercial |

## A pergunta do primeiro teste

> Um mapa estruturado de uma etapa do funil ajuda um responsável do 80VinteBot a encontrar e decidir algo que hoje exige reler conversas, cruzar registros ou depender de conhecimento tácito?

Se a resposta observada for não, o piloto deve registrar isso e encerrar ou mudar de direção. O teste não precisa provar uma tese predefinida; precisa reduzir uma incerteza útil.

## Piloto proposto

### Mapa de Inteligência de Conversas de Vendas

Um piloto colaborativo e sem cobrança, pensado como caso de teste entre pessoas de confiança. A ausência de cobrança não elimina as regras de escopo, privacidade, propriedade e encerramento.

### Recorte inicial

- uma etapa do funil;
- um tipo de lead ou oferta;
- um conjunto limitado de conversas sintéticas ou anonimizadas;
- execução offline e somente leitura;
- nenhuma escrita no CRM;
- nenhuma mensagem enviada a clientes;
- nenhuma credencial de produção;
- revisão humana de toda conclusão importante.

### Método do piloto

Escolhemos uma decisão real e o material permitido; o Ontologize transforma as conversas em um mapa comparável ao processo atual; e o responsável revisa as divergências antes de decidir se encerra, ajusta ou avança para outro teste.

## O que o 80VinteBot receberia

### 1. Mapa do vocabulário comercial

Uma definição compartilhada dos conceitos usados no recorte, como intenção, necessidade, objeção, qualificação, promessa, próximo passo e resultado.

### 2. Mapa estruturado das conversas

Uma representação consultável dos conceitos e das relações encontrados, com referência às mensagens de origem sempre que o dado permitir.

### 3. Relatório de lacunas de qualificação

Perguntas ausentes, critérios não confirmados, ambiguidades e informações que podem ter sido inferidas cedo demais.

### 4. Mapa de objeções e próximos passos

Objeções observadas, respostas associadas, recorrências e compromissos registrados ou ausentes.

### 5. Comparação conversa x CRM

Um retrato do que foi preservado, simplificado, alterado ou perdido entre a conversa e o registro operacional.

### 6. Scorecard de decisão

Os resultados do teste, as limitações encontradas e uma recomendação explícita: parar, repetir, ajustar ou investigar uma integração.

## O que "decisão" significa aqui

Uma decisão não é aceitar um relatório nem concordar que o mapa parece interessante. É uma mudança operacional específica, reversível e pertencente a um responsável:

> Para leads que apresentam uma condição observável, trocar a ação atual por uma ação definida e medir se o resultado melhora sem ultrapassar os limites acordados.

### Exemplo ilustrativo de decisão X

O mapa encontra conversas em que o lead declara intenção de compra, mas mantém uma objeção de preço sem resposta e recebe apenas o follow-up genérico.

**Decisão X:** para esse grupo de leads, encaminhar a conversa a uma pessoa em até 15 minutos e exigir um próximo passo com data antes de encerrar o atendimento. O prazo de 15 minutos é apenas ilustrativo; o valor real seria definido pelo 80VinteBot e pelo cliente participante.

**Hipótese econômica:** uma resposta mais adequada à objeção reduz perda entre qualificação e reunião, o que pode aumentar propostas, vendas e receita por lead elegível.

```text
evidência nas conversas
  -> decisão X
  -> mudança no atendimento
  -> mais reuniões ou avanço no funil
  -> mais vendas
  -> maior receita por lead elegível
```

Essa cadeia é uma hipótese causal, não um resultado prometido. Cada ligação precisa ser observada; se as reuniões aumentarem, mas as vendas ou a margem não melhorarem, não podemos declarar impacto financeiro positivo.

### Como testar impacto em receita

O teste precisa separar três tipos de medida:

- **Métrica econômica principal:** receita por lead elegível e quantidade de vendas no grupo observado.
- **Indicadores intermediários:** tempo até o encaminhamento, reuniões marcadas, propostas emitidas e conversão entre etapas.
- **Guardrails:** carga humana, cancelamentos, reclamações, desconto concedido, margem e qualquer efeito indesejado.

Uma leitura simples seria:

```text
receita por lead elegível = receita atribuída aos leads elegíveis / total de leads elegíveis
```

Para atribuir uma diferença à decisão X, seria necessário um segundo experimento autorizado, com regra predefinida, período, população comparável, baseline ou grupo de controle e demais mudanças relevantes congeladas ou registradas. O piloto offline proposto nesta primeira conversa pode encontrar e especificar a decisão candidata; ele não pode provar impacto em receita.

### Regra de decisão do experimento

- **Expandir:** a métrica principal melhora e os guardrails permanecem aceitáveis.
- **Reter ou retestar:** os sinais intermediários melhoram, mas o efeito econômico continua inconclusivo.
- **Reverter:** a métrica principal piora, os guardrails são violados ou o custo supera o benefício observado.

## O que isso poderia habilitar depois

As possibilidades abaixo são hipóteses de evolução. Elas dependem da utilidade observada no piloto e de novas decisões de produto, segurança e engenharia.

- perfis de lead explicáveis, ligados aos sinais que os sustentam;
- critérios de qualificação aplicados com maior consistência;
- passagem de contexto mais completa entre atendimento, vendas e customer success;
- inteligência sobre objeções e necessidades recorrentes;
- campos de CRM acompanhados da evidência que justificou seu preenchimento;
- um ciclo supervisionado em que as correções do time melhoram o vocabulário e as regras;
- uma futura camada de inteligência nativa do 80VinteBot, caso haja valor e viabilidade técnica.

O caminho desejável é: primeiro demonstrar utilidade fora da produção; depois decidir se uma integração merece existir.

## O que já sabemos e o que ainda não sabemos

| Afirmação | Situação atual |
| --- | --- |
| O 80VinteBot oferece automação de conversas e operações comerciais | Observado em material público; o ambiente real não foi inspecionado |
| A oferta pública inclui elementos como onboarding e avaliação da experiência | Observado em material público |
| O Ontologize possui uma proposta e um desenho de produto para conhecimento estruturado e revisável | Sustentado pelos artefatos atuais do projeto |
| Existe um desenho interno de piloto para evidências de leads | Planejado, ainda não executado |
| O mapa será útil para uma decisão do 80VinteBot | Hipótese a testar |
| O Ontologize deve virar uma funcionalidade integrada ao 80VinteBot | Desconhecido; não é decisão deste piloto |
| A abordagem aumentará conversão ou receita | Desconhecido; não deve ser prometido pelo piloto |

## Como avaliar o teste

As medidas servem para aprender, não para fabricar uma história de sucesso.

- proporção de campos importantes com evidência identificável;
- interpretações confirmadas, contestadas ou deixadas inconclusivas pelo responsável;
- lacunas de qualificação encontradas;
- divergências entre conversa e CRM;
- tempo necessário para a revisão;
- objeções recorrentes consideradas acionáveis pelo time;
- próximos passos ausentes ou ambíguos;
- trabalho adicional imposto ao responsável;
- pedido espontâneo para repetir o uso em outro conjunto de conversas.

Interesse em repetir o teste é um sinal de utilidade percebida. Não prova retorno financeiro, disposição a pagar ou impacto em conversão.

## Proteções para dados, propriedade e amizade

- usar dados sintéticos ou anonimizados sempre que possível;
- receber apenas o mínimo necessário para o recorte escolhido;
- definir por escrito quem pode acessar cada material;
- não reutilizar conversas, resultados ou nomes fora do piloto sem autorização;
- não publicar o caso nem usar a marca do 80VinteBot sem aprovação explícita;
- registrar o que deve ser devolvido, retido ou apagado ao final;
- separar claramente contribuições do 80VinteBot, tecnologia do Ontologize e aprendizados compartilhados;
- permitir que qualquer lado encerre o piloto sem obrigação comercial futura.

## Riscos principais

### Um relatório interessante que não muda nenhuma decisão

**Proteção:** escolher a decisão, o responsável e o uso esperado antes de analisar qualquer conversa.

### Interpretações convincentes, mas incorretas

**Proteção:** ligar conclusões a evidências, expor incerteza e exigir revisão humana nos pontos importantes.

### Escopo crescer para uma integração prematura

**Proteção:** manter o primeiro teste offline, somente leitura e com critério explícito de encerramento.

### Exposição desnecessária de dados comerciais ou pessoais

**Proteção:** minimizar, anonimizar e controlar acesso; interromper o teste se não houver base segura para o uso.

### A proximidade pessoal substituir uma decisão de produto

**Proteção:** tratar o piloto gratuito com o mesmo rigor de escopo, evidência e fechamento de um trabalho profissional.

## O que este piloto não pretende fazer

- substituir o CRM;
- operar autonomamente sobre clientes;
- enviar mensagens ou alterar dados em produção;
- declarar que uma classificação é verdadeira sem revisão;
- auditar ou certificar o 80VinteBot;
- provar aumento de receita, conversão ou produtividade em um teste curto;
- obrigar uma parceria, integração ou contrato posterior;
- transformar um teste amistoso em divulgação pública sem consentimento.

## Perguntas para a conversa de descoberta

1. Em qual etapa do funil vocês mais precisam reler conversas para entender o que aconteceu?
2. Qual decisão comercial ou de produto poderia melhorar com esse entendimento?
3. Quem é a pessoa responsável por revisar e usar o resultado?
4. O que o CRM registra hoje e o que costuma ficar apenas na conversa?
5. Como vocês definem um lead qualificado nessa etapa?
6. Quais objeções, necessidades ou sinais gostariam de enxergar com mais consistência?
7. Existem conversas sintéticas, anonimizadas ou autorizadas adequadas para o teste?
8. Quais dados não devem sair do ambiente atual em nenhuma circunstância?
9. Que resultado faria o piloto merecer uma segunda rodada?
10. Que resultado faria vocês encerrarem a ideia?
11. Quanto trabalho de revisão é aceitável para o responsável?
12. Há alguma funcionalidade existente que já resolve esse trabalho de forma suficiente?
13. Qual regra de atendimento, qualificação ou encaminhamento vocês estariam realmente dispostos a mudar?
14. Qual métrica econômica do cliente permitiria saber se essa mudança produziu valor?

## Próxima decisão

Antes de construir ou integrar qualquer coisa, precisamos responder:

> Existe uma etapa do funil, uma decisão operacional que pode ser alterada, um responsável, um conjunto permitido de conversas e uma métrica de resultado que justifiquem um teste pequeno?

Se sim, o próximo artefato deve ser um plano de piloto com escopo, acesso, medidas, responsabilidades e critério de encerramento. Se não, a proposta deve permanecer como hipótese, sem pressionar uma aplicação artificial.

## Mensagem curta para iniciar a conversa

> Estive olhando o 80VinteBot e pensei em uma aplicação bem concreta do Ontologize. A ideia é pegar uma etapa pequena do funil e transformar algumas conversas em um mapa revisável de necessidades, objeções, critérios de qualificação, próximos passos e evidências. Assim daria para comparar o que realmente apareceu na conversa com o que chegou ao CRM e descobrir se existe conhecimento comercial sendo perdido. Faria primeiro de forma offline, com dados sintéticos ou anonimizados, sem tocar a produção e sem custo para vocês. Antes de propor o teste, queria entender se existe uma decisão real em que esse mapa ajudaria. Se o mapa revelar uma mudança operacional concreta, podemos desenhar um segundo experimento para medir conversão e receita por lead; o primeiro piloto, sozinho, não prova esse impacto. Se não existir uma decisão útil, paramos por aí.
