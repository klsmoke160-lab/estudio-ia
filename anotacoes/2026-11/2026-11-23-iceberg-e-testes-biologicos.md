# Iceberg das Conspirações e os testes biológicos em cidades americanas

> Data: 2026-11-23 · Tipo: anotação · Status: sessão encerrada com o vídeo novo parado na narração

**Resumo:** nesta sessão saiu o documentário do Iceberg das Conspirações (v1, capa no estilo Mistère, título e descrição) e começou o vídeo seguinte, sobre os testes de guerra biológica que o Exército e a Marinha dos EUA fizeram sobre cidades americanas entre 1949 e 1968. O roteiro, os documentos, o plano de imagens, a capa e o pacote de publicação estão prontos; a narração parou por falta de crédito no ElevenLabs.

## O que ficou pronto

- **Iceberg das Conspirações** (`04-projetos/2026-11-23-iceberg-das-conspiracoes/`): vídeo v1 de 10:44, capa `render/capa-mistere.jpg`, título e descrição.
- **Testes biológicos** (`04-projetos/2026-11-23-testes-biologicos/`): roteiro de 1.614 palavras em 8 capítulos, 18 páginas de documento com marca-texto, plano de imagens com as 147 frases cobertas, capa `render/capa.jpg` e `publicacao-youtube.md`.

## O que aprendi

- **O dono não quer imagem desenhada nem com cara de IA.** O iceberg ilustrado foi rejeitado; o que funcionou foi filmagem real de iceberg (Mixkit) com o texto do nível por cima. Vale para tudo daqui em diante.
- **Antes de escrever, verificar.** Neste vídeo, a lista de cidades, o parecer de 1952 e a conclusão do estudo do metrô saíram direto dos PDFs; o processo da família Nevin só aparece na imprensa, então a frase no roteiro ficou genérica de propósito ("processou o governo e perdeu"), sem citar número de processo.
- **Um roteiro pode ir longe demais no detalhe operacional.** O primeiro rascunho descrevia o dispositivo, a quantidade e o método usados no metrô em 1966. Isso não é história, é receita, e saiu do roteiro. A história se sustenta no que o governo sabia, decidiu e admitiu.
- **Cabeçalho de capítulo no roteiro usa `#`, não `[...]`.** O `tratar_narracao.py` só reconhece linhas que começam com `#`.
- **Caixas de marca-texto em PDF escaneado:** o OCR do tesseract erra palavras com hífen de quebra de linha ("ex- posing") e troca letras em texto datilografado ("HighAvay"). Escolher como âncora um trecho curto e sem hífen, e conferir a página renderizada antes de seguir.
- **Disco:** a sessão travou em 100% de disco. O que liberou espaço: apagar `render/doc/segs` de vídeos já entregues, `uv cache prune` (444 MB) e os brutos grandes de projetos fechados.

## Material novo

- `/home/user/mk/bio/docs/`: audiência do Senado de 1977 (306 páginas, com camada de texto) e o estudo do metrô de 1968.
- `/home/user/mk/bio/raw/`: filmes de arquivo público — guerra biológica (1951), bactérias no laboratório (1953), instalações e laboratórios (anos 1950), Nova York (1941 e 1947), trem elevado (1950) e cinejornal de São Francisco (1950).

## Parado

A narração do vídeo novo precisa de 9.627 caracteres e só restam 1.288 no plano gratuito do ElevenLabs (reinicia em meados de dezembro). Opções para o dono: assinar um plano pago (resolve também a licença comercial, que o plano gratuito não dá), trocar para outra conta com crédito, ou gravar a própria voz e mandar o MP3.
