# Mercado brasileiro — o que este repo sabe

Notas que não generalizam bem entre países, separadas pra que outros mercados adicionem as suas.

## Sistemas de candidatura (ATS)

| Plataforma | Presença | O que importa |
|---|---|---|
| **Gupy** | dominante, principalmente em empresa média e grande | **Baseada em perfil.** A plataforma envia o seu perfil Gupy armazenado, não o arquivo que você anexa. Campos de texto livre resistem a automação — numa ocasião cinco métodos foram tentados e todos falharam em silêncio. Planeje preencher na mão. |
| Greenhouse / Lever | tech, startups, multinacionais | Baseadas em documento, limpas, upload funciona |
| inHire, recrut.ai | tech brasileira | Baseadas em documento |
| Abler, Sólides | PME | Varia |
| LinkedIn Easy Apply | em todo lugar | Envia o seu perfil do LinkedIn — mantenha atualizado |

**A armadilha do perfil.** Um CV lindamente ajustado anexado a um perfil desatualizado é pior que
inútil: o recrutador lê o perfil. Caso real da busca que originou este repo — o perfil da Gupy ainda
listava um empregador que o candidato tinha deixado e não mencionava o cargo atual, enquanto todo CV
enviado dizia o contrário. A habilidade `02` sinaliza isso antes de você se candidatar.

## Duas caixas de e-mail, não uma

O LinkedIn notifica o endereço da **conta do LinkedIn**. Todo o resto dos ATS notifica o endereço
**digitado no formulário deles**. Se esses endereços são diferentes — e normalmente são — checar uma
caixa só mostra metade do quadro.

Na busca que originou este repo, duas de quatro confirmações estavam paradas, não lidas, num segundo
endereço. A habilidade `05` varre todas.

## CLT × PJ

São dois modelos diferentes, não dois nomes pra mesma coisa.

**CLT** é o regime de empregado registrado: 13º, férias mais um terço, FGTS, INSS patronal, e os
benefícios que a empresa somar.

**PJ** significa faturar pela sua própria empresa. Bruto maior, nada do que está acima, e você
carrega o imposto e a contabilidade.

Migrar CLT → PJ no mesmo número é redução de remuneração. Aproximadamente:

| Perde | Aprox. |
|---|---|
| 13º salário | +8,3% |
| Férias + ⅓ | +11,1% |
| FGTS | +8% |
| INSS patronal, plano de saúde, VR/VA, seguro de vida | varia — muitas vezes o maior pedaço |

Regra de bolso do mercado: **PJ precisa ficar uns 30% a 50% acima do bruto CLT** pra manter o pacote
igual. Aí subtraia a faixa do Simples Nacional (o nível de faturamento decide, e cruzar faixa muda
bastante a alíquota efetiva), o contador, e o pró-labore necessário pra ficar no anexo favorável.

**Exportação de serviços** tem tratamento diferente — normalmente isenta de ISS e de PIS/COFINS, o
que joga a alíquota efetiva abaixo da tabela nominal. Confirme os detalhes com contador; não
presuma. Veja a habilidade `08`.

## Salário em moeda estrangeira

Empresas de nearshore e staffing cotam em dólar. Três coisas pra colocar na frente da pessoa,
sempre: a cotação oficial do dia com a data, o cenário de baixa se o real valorizar, e o spread de
conversão — que varia uma ordem de grandeza entre plataformas.

E pergunte se o contrato tem cláusula de reajuste anual. Número fixo em moeda estrangeira sem
revisão é redução salarial em câmera lenta.

## Entrevista assíncrona por áudio

Cada vez mais comum, e desconhecida da maioria dos candidatos. Um bot manda a pergunta pelo
WhatsApp, um cronômetro corre, você grava um áudio de resposta, e um humano avalia depois. O
**DigAI** é a plataforma por trás da triagem de várias empresas grandes.

O que pega as pessoas de surpresa: o cronômetro inclui o tempo de leitura, a plataforma pode
rejeitar resposta enviada depois do prazo, e estrutura conta mais que profundidade porque quem
avalia está comparando dezenas de gravações. A habilidade `07` prepara pra isso especificamente.

## Título de senioridade não traduz

Consultoria pede rotineiramente dez anos pra título de "arquiteto", enquanto o mesmo escopo numa
empresa de produto é sênior individual. Errar a faixa queima ciclos inteiros de candidatura em vagas
que nunca iam converter.

Feedback de recrutador vale mais que texto de anúncio. Quando um recrutador calibra a faixa numa
conversa, registre em `profile/<pessoa>/profile.md` e trate como autoritativo.
