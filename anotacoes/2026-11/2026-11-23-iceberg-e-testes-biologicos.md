# Iceberg das Conspirações e os testes biológicos em cidades americanas

> Data: 2026-11-23 · Tipo: anotação · Status: encerrada — os dois vídeos montados

**Resumo:** nesta sessão saiu o documentário do Iceberg das Conspirações (v1, capa no estilo Mistère, título e descrição) e começou o vídeo seguinte, sobre os testes de guerra biológica que o Exército e a Marinha dos EUA fizeram sobre cidades americanas entre 1949 e 1968. O roteiro, os documentos, o plano de imagens, a capa, a narração e o pacote de publicação ficaram prontos: vídeo de 11:08.

## O que ficou pronto

- **Iceberg das Conspirações** (`04-projetos/2026-11-23-iceberg-das-conspiracoes/`): vídeo v1 de 10:44, capa `render/capa-mistere.jpg`, título e descrição.
- **Testes biológicos** (`04-projetos/2026-11-23-testes-biologicos/`): roteiro de 1.614 palavras em 8 capítulos, 18 páginas de documento com marca-texto, plano de imagens com as 147 frases cobertas, vídeo `render/testes-biologicos-v1.mp4` (11:08), capa `render/capa.jpg` e `publicacao-youtube.md`.

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

## A narração

O dono trocou para uma conta nova do ElevenLabs e a narração saiu na mesma sessão: voz Davi, 9.627 caracteres em duas partes (o limite por geração é 5.000), juntadas com 1,2 s de silêncio. Vídeo final: 11:08.

Duas coisas aprendidas aqui:

- **Montar com narração muda antes de gastar crédito.** O `motor/timeline_ensaio.py` gera uma timeline com tempos estimados (150 palavras por minuto) e um WAV silencioso. Dá para fechar a imagem inteira, achar os erros de enquadramento e de cor, e só então gerar a voz. Neste vídeo isso evitou duas gerações jogadas fora.
- **O Whisper erra e parece erro de voz.** O alinhador acusou "27, 27 anos" repetido; ao ouvir o áudio original era "1977, vinte e sete anos depois". Antes de regravar qualquer trecho, conferir o áudio de origem, não só a transcrição.

Continua valendo: conta gratuita não dá licença comercial. Antes de monetizar, regerar as narrações dos três vídeos num plano pago.
