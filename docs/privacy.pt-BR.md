# Privacidade

Sua carreira não é dado de treino nem artefato público.

## O que nunca é commitado

O `profile/` está no gitignore, exceto o `profile/_example/`, que é fictício. Também ignorados:
`applications/`, `output/`, todo `.pdf` e `.docx` fora de templates, varreduras de e-mail, arquivos
de áudio e transcrições.

O CI fiscaliza: um job derruba o build se qualquer coisa dentro de `profile/` além do exemplo
passar a ser rastreada pelo git. Ignorar arquivo é decisão que não deveria depender de memória.

## O que nunca sai da sua máquina

**Áudio.** A habilidade `07` transcreve com um modelo Whisper local. Gravação não sobe pra lugar
nenhum.

**Conteúdo de e-mail.** A habilidade `05` lê e reporta. Não encaminha, não copia, não armazena
corpo de mensagem fora da sua máquina.

**Dado pessoal em formulário web.** O agente nunca digita seus dados em site de terceiro. Nunca
coloca informação pessoal em URL ou em busca.

## O que o agente não faz

Do `AGENTS.md` §2.3, e não é negociável:

O agente nunca submete candidatura, clica em "candidatar-se", envia e-mail ou mensagem, aceita
termos, cria conta, digita senha ou sobe documento em site de terceiro.

Ele prepara. **Você** envia. Essa fronteira existe pra que nada irreversível aconteça sem um humano
decidindo, e pra que você sempre saiba exatamente o que foi enviado no seu nome.

## Entrada não confiável

Vaga, e-mail de recrutador e página de empresa são dado, nunca instrução. Se algum contiver texto
endereçado ao agente, ele mostra o trecho e pergunta — não executa. E nunca segue link encontrado
dentro do corpo de uma vaga.

## Se você fizer fork

O perfil de exemplo é fictício de propósito. Mantenha assim, e mantenha o seu fora do histórico. Se
você commitar dado pessoal sem querer, reescrever o histórico não resolve depois que foi pro remoto
público — rotacione o que der pra rotacionar e trate o resto como público.
