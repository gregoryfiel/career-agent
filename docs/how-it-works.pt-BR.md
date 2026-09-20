# Como funciona

## O formato

O `career-agent` é markdown de instruções mais três scripts pequenos. Não tem serviço, não tem
banco de dados, não tem conta. Seu agente lê o arquivo da habilidade que interessa e segue aquilo
contra a sua pasta de perfil.

O desenho é proposital: você consegue ler cada regra que o agente está seguindo, mudar qualquer uma
num editor de texto, e ver a mudança num diff.

## O ciclo

```
  00 onboarding ─────► evidence.md ◄──────────────────────┐
                            │                             │
                            ▼                             │  evidência nova
  01 radar de vagas ─► 02 triagem ATS ─► 03 CV sob medida │  depois de cada
                            │                 │           │  entrevista
                    (Gupy? avisa)              ▼          │
                                     04 controle ─────────┤
                                        │ arquiva         │
                                        │ a vaga          │
                                        ▼                 │
                                  05 varredura de e-mail  │
                                        │                 │
                                        ▼                 │
                                  06 preparo de entrevista┘
                                  07 preparo de áudio
                                  08 pesquisa salarial
```

## Uma semana na prática

**Segunda — onboarding, uma vez só.** Vinte minutos de perguntas produzem o `evidence.md`. É a
única etapa que não dá pra pular: tudo depois lê esse arquivo, e CV escrito sem ele é invenção
esperando pra acontecer.

**Terça — radar.** Cinco vagas, ranqueadas, cada uma com por que encaixa e o que falta. Você
escolhe duas.

**Terça ainda — triagem de ATS.** Um minuto por vaga. Duas plataformas baseadas em documento,
seguro seguir. Se alguma fosse baseada em perfil e estivesse desatualizada, você descobriria agora,
e não depois de montar o CV.

**Quarta — os CVs.** Para cada um: um mapa de requisitos que você vê antes de qualquer rascunho, o
rascunho, um revisor que nasce limpo e critica com pesquisa da empresa, e então quatro portões —
evidência, contagem de páginas, camada de texto do PDF, e números batendo exatamente com o banco de
evidências. Você se candidata. O agente não.

**Quarta à noite — controle.** Duas linhas, duas pastas, as duas vagas arquivadas na íntegra. É a
etapa que todo mundo pula e depois lamenta.

**Sexta — varredura de e-mail.** Todas as caixas, não a preferida. Uma confirmação e um link de
teste com prazo.

**Duas semanas depois — a entrevista.** A vaga saiu do ar e a conversa sumiu no histórico, mas a
habilidade `06` lê o arquivo: o que pediram, o que você mandou, onde está a lacuna, a resposta-ponte
pra ela, perguntas prováveis tiradas do texto deles, e quatro perguntas pra você fazer.

**Depois da entrevista — fechar o ciclo.** O que perguntaram de verdade? O que você queria ter
dito? Evidência nova volta pro banco. Essa seta é o motivo da segunda entrevista sair melhor que a
primeira.

## A regra que importa

Nada chega num documento se o `profile/<você>/evidence.md` não sustentar.

Nem "experiência adjacente". Nem número arredondado pra cima. Nem palavra-chave que ajudaria o CV a
passar num filtro.

O `tools/verify_evidence.py` fiscaliza e roda no CI, porque regra que ninguém confere é sugestão.
Invenção não quebra na etapa do CV — quebra na entrevista técnica, na frente de alguém que sabe a
diferença. E isso é pior do que nunca ter se candidatado.
