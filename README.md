# HyperCut

Área de trabalho pronta para produzir vídeos com [HyperFrames](https://github.com/heygen-com/hyperframes), que transforma HTML em MP4, usando o agente de IA que você preferir.

Você pede o vídeo e o agente segue um fluxo com padrões de roteiro, movimento, legenda e som, além de conferir a mixagem no arquivo final.

## O que vem aqui

- **Criação de projetos:** `bin/novo-video` monta cada vídeo com a mesma estrutura.
- **Padrões de produção:** `PRODUCAO.md` define narrativa, movimento, legibilidade e níveis de áudio.
- **Análise de referências:** a skill `assistir-video` lê vídeos por link ou arquivo, tudo na sua máquina.
- **Legendas:** a skill `legendas-da-voz` gera legenda palavra por palavra a partir da voz final.
- **Áudio:** `sons/sons` traz um kit CC0, busca e geração de efeitos. A skill `medir-mixagem` mede LUFS e pico.
- **Tratamento:** a skill `tratar-bruto` limpa voz, estabiliza imagem e confere arquivos contra a spec das redes.
- **GPU:** transcrição em NVIDIA quando disponível, com queda para CPU.

## Agentes compatíveis

As regras ficam em `AGENTS.md`, e as skills seguem o formato aberto `SKILL.md`. Nada depende de uma empresa ou de um modelo.

| Agente | Situação |
| --- | --- |
| Claude Code | Em uso |
| OpenCode | Testado |
| Codex, Cursor, Antigravity, Gemini CLI, GitHub Copilot, Windsurf | Configurados pela documentação, sem teste |

O modelo precisa rodar comandos no terminal. Para a revisão visual, precisa também ler imagem.

## Começar

```bash
git clone --recurse-submodules https://github.com/WesleyDev184/HyperCut.git
cd HyperCut
```

Siga o [INSTALACAO.md](INSTALACAO.md): ambiente primeiro, depois o passo do seu agente. A instalação foi feita para Linux x86_64 e ocupa cerca de 30 GB.

Depois, abra o agente nesta pasta e peça:

```text
Crie um vídeo vertical de 20 segundos apresentando meu produto.
```

## Seus vídeos

Tudo fica em `projetos/`, que não entra no git. Faça seu próprio backup.

## Licença

[MIT](LICENSE). Itens de terceiros, incluindo skills opcionais sem licença publicada, estão em [TERCEIROS.md](TERCEIROS.md).
