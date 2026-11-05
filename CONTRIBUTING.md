# Como contribuir

Obrigado por querer ajudar o HyperCut. Issues e pull requests são bem-vindos, em português.

## Antes de começar

- Procure nas [issues](https://github.com/WesleyDev184/HyperCut/issues) se o assunto já existe.
- Mudança grande: abra uma issue antes do pull request e combine o caminho.
- Prepare o ambiente pelo [INSTALACAO.md](INSTALACAO.md).
- Leia o [AGENTS.md](AGENTS.md) e o [PRODUCAO.md](PRODUCAO.md). Eles são a fonte das regras daqui.

## O que entra no repositório

- Ferramentas, skills, regras e documentação compartilhadas.
- Só material com licença que permita redistribuir. Registre o que vem de terceiros no [TERCEIROS.md](TERCEIROS.md).

## O que não entra

- Vídeos: `projetos/` fica fora do git.
- Skill ou mídia sem licença clara.
- Cookies, senhas, tokens, dados pessoais e gravações de outras pessoas.
- Nome de pessoa ou marca nos arquivos publicados. Escreva "a pessoa" no lugar.

## Pull request

1. Faça um fork e crie uma branch a partir da `main`.
2. Mantenha cada pull request em um assunto só.
3. Teste a mudança de verdade: rode o comando alterado ou gere um vídeo curto com `bin/novo-video`.
4. Atualize a documentação quando o comportamento mudar.
5. Preencha o modelo do pull request.

A `main` é protegida: toda mudança entra por pull request, com squash. O título do pull request vira a mensagem
do commit, então use o formato `tipo: descrição`, como `feat: adiciona paleta clara` ou `fix: corrige caminho do whisper`.

## Regras do projeto

- Textos, comentários e mensagens em pt-BR.
- Use `bin/hf` no lugar de `npx hyperframes`.
- A versão do HyperFrames é uma só, fixada no `package.json`. Atualizar exige conferir as skills e os projetos.
- Commits e pull requests não citam agente, modelo ou ferramenta de IA como autor ou coautor.
  Usar IA para contribuir é permitido, desde que você tenha testado e entenda o que enviou.

## Segurança

Não abra issue pública para falha de segurança. Siga o [SECURITY.md](SECURITY.md).

## Licença

Ao contribuir, você concorda que sua contribuição seja distribuída sob a [licença MIT](LICENSE).
