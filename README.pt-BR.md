<div align="center">

# career-agent

**A busca de emprego que mora no seu repositório — e não inventa nada.**

[![License: MIT](https://img.shields.io/badge/License-MIT-000000.svg?style=flat-square)](LICENSE)
[![Agent-agnostic](https://img.shields.io/badge/agente-agn%C3%B3stico-6f42c1?style=flat-square)](AGENTS.pt-BR.md)
[![Evidence gate](https://img.shields.io/badge/anti--inven%C3%A7%C3%A3o-validado%20no%20CI-0a7d33?style=flat-square)](tools/verify_evidence.py)
[![English](https://img.shields.io/badge/read%20in-english-0057b7?style=flat-square)](README.md)

*Nove habilidades que acham a vaga, checam o ATS antes de você gastar um CV, montam o currículo
contra um banco de evidências travado, e devolvem a vaga exata no dia da entrevista.*

[O que muda aqui](#o-que-muda-aqui) · [Instalação](#instalação) · [O ciclo](#o-ciclo) ·
[As habilidades](#as-nove-habilidades) · [Privacidade](#privacidade)

</div>

---

## Por que isso existe

Começou como a busca de emprego de uma pessoa, conduzida inteiramente por um agente de código.
Quinze candidaturas, cinco plataformas de ATS diferentes, uma triagem assíncrona por áudio, um
recrutador no WhatsApp.

No caminho, os mesmos problemas se repetiram — e nenhum dos agentes de busca de vaga que já existem
resolvia:

- Um CV inteiro foi montado para uma vaga, e só **depois** descobrimos que a candidatura rodava na
  **Gupy**, cujos campos de texto livre rejeitam qualquer automação. Trabalho perdido.
- Duas candidaturas estavam **confirmadas numa segunda caixa de e-mail** que ninguém checava, porque
  o LinkedIn manda para um endereço e todo o resto dos ATS manda para outro.
- Uma recomendação de mirar vagas de arquiteto estava **errada em cinco anos de senioridade**, e só
  uma conversa real com recrutador trouxe isso à tona.
- Chegou a entrevista e a vaga tinha **sumido no histórico da conversa** — sem jeito de lembrar o que
  tinha sido prometido no papel.
- Uma **entrevista por áudio** voltou com feedback certo, mas vago. O problema real só ficou visível
  depois de transcrever as gravações e contar quantas vezes o candidato disse *"a gente"* em vez de
  *"eu"*. Foram oitenta e uma.

Cada um desses virou uma habilidade. É isso que este repositório é.

## O que muda aqui

A maioria dos agentes de busca de vaga otimiza para volume. Este otimiza para **não te expor**.

**Banco de evidências travado.** O `profile/<você>/evidence.md` é a fonte única da verdade. Uma
tecnologia só chega no seu CV se estiver lá, com o cargo e o projeto onde você realmente usou. O
`tools/verify_evidence.py` roda no CI e derruba o build se algo escapar. Nada de habilidade
"adjacente", número inflado ou enfiar palavra-chave. Invenção não quebra na etapa do CV — quebra na
entrevista técnica, o que é pior do que nunca ter se candidatado.

**Triagem de ATS antes do CV.** A habilidade `02` identifica o sistema de candidatura pelo link da
vaga *antes* de escrever uma linha de currículo, e avisa quando a plataforma é uma que você decidiu
não encarar. Checagem barata, erro caro.

**A vaga volta para a entrevista.** A habilidade `04` arquiva a descrição completa no momento do
envio. A `06` lê isso de volta semanas depois e monta o dossiê: o que pediram, o que você mandou,
onde os dois se encontram, onde está a lacuna, perguntas prováveis de RH, perguntas prováveis de
técnico, e a resposta-ponte honesta para tudo que você não pode reivindicar.

**Preparação para entrevista por áudio.** Triagem assíncrona por áudio já é padrão em alguns
mercados. A habilidade `07` transcreve suas gravações de treino localmente com Whisper, mede ritmo,
conta vícios de linguagem e uso de primeira pessoa, e reconstrói cada resposta no formato
Contexto → Ação → Resultado, com cronômetro.

**Conta de salário que bate com a realidade.** A habilidade `08` busca dado por empresa e por cargo
em vez de média nacional e faz a conversão de regime (CLT ↔ PJ), a faixa tributária do Simples e a
exposição cambial quando o salário é cotado em moeda estrangeira.

**Roda em qualquer agente.** As instruções vivem no [`AGENTS.md`](AGENTS.md), o formato aberto que
Claude Code, Codex, Cursor, Gemini CLI, Copilot e Windsurf leem. O `CLAUDE.md` é um ponteiro de uma
linha. Sem amarra de fornecedor.

## Instalação

```bash
gh repo clone gregoryfiel/career-agent   # ou: git clone https://github.com/gregoryfiel/career-agent
cd career-agent

# Opcional — só a habilidade 07 (áudio) e o checador de páginas precisam disso
pip install -r tools/requirements.txt
sudo apt-get install -y ffmpeg libreoffice poppler-utils
```

Depois abra a pasta no agente da sua preferência e diga:

```
Roda a habilidade 00-onboarding pra mim.
```

A entrevista de onboarding leva uns vinte minutos e produz o seu banco de evidências. Todo o resto
depende dele.

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

A seta que mais importa é a que volta para o banco de evidências. Toda entrevista traz à tona
alguma coisa que você tinha esquecido que fez.

## As nove habilidades

| # | Habilidade | O que faz |
|---|---|---|
| `00` | **onboarding** | Monta o banco de evidências a partir do seu CV, LinkedIn ou conversa guiada. Marca lacunas em vez de preencher. |
| `01` | **job-radar** | Acha vagas abertas em portais e no LinkedIn, pontua aderência ao seu perfil, filtra pela sua faixa de senioridade. |
| `02` | **ats-triage** | ⭐ Resolve o link da candidatura até o ATS **antes** do trabalho de CV. Sinaliza plataformas da sua lista de recusa. |
| `03` | **tailored-cv** | Um agente rascunha, outro nasce limpo e critica com pesquisa da empresa, aí vem a verificação: evidência, páginas, camada de texto do PDF. |
| `04` | **application-tracker** | Uma linha por candidatura, uma pasta por empresa — CV enviado, vaga arquivada, status, pretensão informada. |
| `05` | **inbox-sweep** | Varre todas as caixas que você usa de verdade, porque as confirmações não caem todas no mesmo lugar. |
| `06` | **interview-prep** | ⭐ Devolve a vaga arquivada. Monta preparo de RH e técnico, mapeia suas histórias, escreve as pontes honestas. |
| `07` | **audio-interview** | ⭐ Transcreve gravações de treino localmente. Mede ritmo, vícios, primeira pessoa. Reconstrói em Contexto → Ação → Resultado. |
| `08` | **salary-research** | ⭐ Dado de remuneração por empresa, conversão de regime, exposição cambial e o roteiro da negociação. |

⭐ = não encontrado em nenhum projeto parecido. Cada um nasceu de uma falha específica.

## Privacidade

Sua carreira não é dado de treino nem artefato público.

O `profile/` está no gitignore, exceto o exemplo fictício. Nada pessoal é commitado, colado em
formulário web ou enviado para serviço de terceiro. A transcrição de áudio roda localmente na sua
máquina via Whisper — a gravação não sai dali.

O agente **nunca submete nada no seu lugar**. Ele rascunha, verifica e entrega. Clicar em
"candidatar-se" é sempre seu. Detalhe completo em [`docs/privacy.pt-BR.md`](docs/privacy.pt-BR.md).

## Documentação

- [`AGENTS.pt-BR.md`](AGENTS.pt-BR.md) — instruções canônicas ([inglês, canônico](AGENTS.md))
- [`docs/how-it-works.pt-BR.md`](docs/how-it-works.pt-BR.md) — o ciclo de ponta a ponta
- [`docs/brazilian-market.pt-BR.md`](docs/brazilian-market.pt-BR.md) — Gupy, CLT × PJ, áudio, duas caixas
- [`docs/privacy.pt-BR.md`](docs/privacy.pt-BR.md) — o que nunca sai da sua máquina

## Contribuindo

As habilidades são markdown. Se o seu mercado tem outro ATS dominante, outra conta de regime de
contratação, ou um formato de triagem que este repo ainda não encontrou — abre um PR. É esse o
mecanismo de extensão inteiro.

## Licença

MIT — veja [LICENSE](LICENSE).
