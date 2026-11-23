# A lista que o Exército entregou ao Senado

> Data: 2026-11-23 · Tipo: projeto · Status: roteiro e documentos prontos; narração parada por falta de crédito de voz

**Resumo:** documentário longo do Rasura (cerca de 11 min, 1.614 palavras, 8 capítulos) sobre os testes de guerra biológica que o Exército e a Marinha dos Estados Unidos fizeram sobre cidades americanas entre 1949 e 1968, contados por dois documentos públicos: a audiência do Senado de março de 1977 e o estudo de vulnerabilidade do metrô de Nova York, de janeiro de 1968. O vídeo é honesto sobre o que não está provado (a morte de Edward Nevin) e firme no que está (a lista de cidades, o parecer de 1952 que autorizou continuar "mesmo sobre áreas povoadas", e a conclusão do próprio estudo do metrô).

## Critério de pronto

- 16:9, 1920×1080, motor `scripts/video/doc_motor.py`, formato de cinema, -16 LUFS.
- Pronto quando a narração chegar (voz Davi), for tratada por `scripts/som/tratar_narracao.py` e o vídeo for montado e conferido do começo ao fim.

## Gancho (regra em `06-metodo/ganchos.md`)

O dono pediu o vídeo, não o roteiro, então os três foram comparados por dentro:

1. **A lista (escolhido):** "Em 1977, o Exército dos Estados Unidos entregou ao Senado uma lista. Não era uma lista de inimigos. Era uma lista de cidades americanas onde o próprio Exército tinha soltado bactérias no ar, sem avisar ninguém que morava lá."
2. **O paciente:** começar pela morte de Edward Nevin em 1950 e só depois revelar o teste.
3. **A frase do parecer:** abrir com "mesmo sobre áreas povoadas" marcada em amarelo na página.

O 1 ganhou por três motivos: entrega a escala (não é um caso, é uma lista), é verificável na tela já no primeiro quadro, e evita prometer uma relação de causa que o vídeo não pode provar. O 2 tinha o risco de o espectador se sentir enganado no capítulo 2, quando o vídeo admite que a ligação nunca foi provada. O 3 virou o clímax do capítulo 3.

### Direção visual do gancho

- **Primeiro quadro:** a página 126 da audiência (a tabela com "New York, NY — 7-10 Jun 1966"), o marca-texto amarelo entrando sobre a linha. Sem rosto, sem narrador, sem logo.
- **Narração:** seca, sem música nos primeiros 4 segundos. A trilha entra só em "Washington. São Francisco. Key West."
- **Corte:** os nomes das cidades caem um a um, um corte por cidade, direto no documento.
- **Texto na tela:** só o nome da cidade e o ano, no canto, na fonte de máquina de escrever.
- **Som:** um clique de projetor a cada cidade.

## Retenção (skill `yt-retention`)

Não havia CSV de retenção para ler (o dono não tem export ainda), então os três princípios foram aplicados na escrita:

- **Vazamento no gancho (primeiros 30 s):** o fato mais forte está na primeira frase, não depois de uma introdução. Nada de "neste vídeo", nada de saudação, nada de "assista até o final".
- **Penhascos:** cada troca de capítulo é anunciada uma frase antes ("E em junho de 1966, a lista chegou ao lugar mais cheio dos Estados Unidos"), para ninguém ser jogado num assunto novo sem aviso.
- **Deslizamento:** o meio do vídeo (capítulos 4 e 5) foi cortado, não alongado. A lista de cidades é lida em ritmo rápido e os detalhes técnicos do método de teste ficaram de fora de propósito: não acrescentam nada à história e não é informação que um canal deva detalhar.

## O que está provado e o que não está

| Afirmação do vídeo | Fonte |
|---|---|
| Lista de testes em domínio público, 1949–1968 | Audiência 1977, Anexo E, Apêndice IV, Tabelas 1 e 3 (pp. 125–133) |
| Aeroporto Nacional de Washington e terminal Greyhound, maio de 1965 | Audiência 1977, p. 126 |
| Nova York, 7 a 10 de junho de 1966 | Audiência 1977, p. 126; estudo do metrô, 1968 |
| Parecer de 1952: continuar "mesmo sobre áreas povoadas" | Audiência 1977, Anexo F, p. 144 |
| Regra interna de não soltar perto de hospitais e sanatórios | Audiência 1977, p. 15 (depoimento do Cel. Carruth) |
| Onze casos num hospital de São Francisco, um morto | Artigo de Wheat e outros, *Archives of Internal Medicine*, 1951, citado na audiência, p. 14 |
| A ligação entre o teste e as infecções **nunca foi provada** | Audiência 1977, Anexo F, pp. 142–146; carta do CDC (Dr. Sencer, fev/1977) |
| Um milhão de trabalhadores no metrô, 75% no pico | Estudo do metrô, 1968, p. 2 |
| O material persistiu nas estações por uma hora ou mais | Estudo do metrô, 1968, abstract e conclusões |
| Nixon encerrou o programa ofensivo em novembro de 1969 | Audiência 1977, p. 10 |
| A família Nevin processou o governo e perdeu | Imprensa; **não** confirmado em documento primário — a frase no roteiro é genérica de propósito |

## Documentos

Os dois PDFs estão em `/home/user/mk/bio/docs/` e as páginas com marca-texto são geradas por `motor/gerar_docs.py` para `/home/user/mk/bio/docs2/`.

## Como montar quando a narração chegar

O texto para a voz está em `texto-para-voz.txt` (9.627 caracteres). O ElevenLabs aceita até 5.000 por geração: usar `voz-parte1.txt` e `voz-parte2.txt` e juntar com 1,2 s de silêncio.

```bash
cd /home/user/estudio-ia
uv run python scripts/som/tratar_narracao.py 04-projetos/2026-11-23-testes-biologicos <audio.mp3> --linha 0 --curta 0.9
python3 scripts/video/doc_motor.py 04-projetos/2026-11-23-testes-biologicos edl
python3 scripts/video/doc_motor.py 04-projetos/2026-11-23-testes-biologicos render
python3 scripts/video/doc_motor.py 04-projetos/2026-11-23-testes-biologicos juntar
python3 scripts/video/doc_motor.py 04-projetos/2026-11-23-testes-biologicos som
python3 scripts/video/doc_motor.py 04-projetos/2026-11-23-testes-biologicos final testes-biologicos-v1.mp4
```

## Montagem de ensaio (23/11)

O vídeo já foi montado inteiro com uma narração muda de tempos estimados
(`motor/timeline_ensaio.py`, 150 palavras por minuto): `render/testes-biologicos-ensaio.mp4`,
12:15, 193 planos, 15,8 cortes por minuto. A imagem é a definitiva; só falta a voz.

Corrigido depois de ver a primeira montagem:
- brilho de -0.10 para 0.05 (os filmes deste vídeo são mais escuros que os dos anteriores);
- foco nas quatro páginas do estudo do metrô, que entravam inteiras e ilegíveis;
- a página 126 marcava dez linhas de uma vez: agora o Aeroporto Nacional e Nova York
  têm cada um o seu documento, com uma linha destacada por vez;
- dois planos do capítulo do mapa (todo em vermelho) ficavam sem imagem nenhuma.

### Quando o áudio chegar

```bash
cd /home/user/estudio-ia
uv run python scripts/som/tratar_narracao.py 04-projetos/2026-11-23-testes-biologicos <audio.mp3> --linha 0 --curta 0.9
python3 scripts/video/doc_motor.py 04-projetos/2026-11-23-testes-biologicos edl
python3 scripts/video/doc_motor.py 04-projetos/2026-11-23-testes-biologicos render
python3 scripts/video/doc_motor.py 04-projetos/2026-11-23-testes-biologicos juntar
python3 scripts/video/doc_motor.py 04-projetos/2026-11-23-testes-biologicos som
python3 scripts/video/doc_motor.py 04-projetos/2026-11-23-testes-biologicos final testes-biologicos-v1.mp4
```

O `tratar_narracao.py` sobrescreve `audio/timeline_novo.json` e
`narracao/narracao_tratada.wav`, então o ensaio é descartado sozinho.
