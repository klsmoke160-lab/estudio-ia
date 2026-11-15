# Referência 06: edição cinematográfica de terror (vídeo sobre lobisomens, partes 1 e 2)

> Data: 2026-11-15 · Tipo: análise · Status: vigente

**Resumo:** análise técnica de um documentário de terror e mistério em português, de 12:15, enviado em duas partes (`claude_video6_parte_01.mp4` e `_02.mp4`) e analisado como um vídeo só. É o oposto da referência 05:
- ritmo lento, com explosões de corte;
- imagem escura em formato de cinema;
- cor tingida por trecho;
- imagens que nascem do escuro;
- som com muita variação, com cortes presos aos sustos.

O guia diz como reproduzir cada técnica sem cair no visual genérico de "vídeo de terror".

## Como foi medido

Os métodos e scripts são os mesmos da referência 05:
- `measure_reference.py` do editonny;
- `scripts/video/analisar_edicao.py` (movimento por ECC, cor, nitidez e áudio);
- `scripts/video/cruzar_edicao.py`;
- transcrição Whisper forçada em português;
- medições extras de vinheta dentro da área útil, cor dominante a cada 2 s e duração das entradas do escuro.

Os dados estão em `03-referencias/medicoes/06_video6/`.

**Limites da medição:**
- O arquivo tem 640×360.
- Em imagem muito escura, o detector de cortes perde trocas que acontecem dentro do preto. Por isso o número de cortes é um piso.
- O "borrão" nas transições é em boa parte imagem escura e tremida, não um efeito.

## 1. Ficha técnica

| Medida | Valor |
|---|---|
| Duração | 12:15 (735 s), **24 quadros/s** (cadência de cinema) |
| Formato | **faixas pretas em 98% do vídeo**: área útil de 640×271, proporção **2,36:1** (cinemascope) |
| Cortes | 172 (113 nítidos e 59 fracos), de **9,2 a 14 por minuto** |
| Duração do plano | mediana **2,3 s**, média 4,3 s; 10% acima de **11 s**; plano mais longo de **65 s** (8:45–9:50) |
| Brilho | médio de **19%**; **80% dos quadros são escuros** |
| Saturação | alta (68% no medidor), porque a imagem é **tingida** e não colorida naturalmente |
| Vinheta | bordas com **30% do brilho do centro**, medida dentro da área útil |
| Narração | começa só aos **0:40**; 182 palavras por minuto; a fala ocupa **54%** do vídeo; 27 pausas acima de 1 s |
| Volume | -17,5 LUFS integrado, **variação de 9,8 LU** (muito dinâmico), pico real de +0,7 dBTP |

## 2. Curva de ritmo e de som

O vídeo alterna **calmaria escura** e **susto**:

| Trecho | Ritmo | Volume momentâneo | O que faz |
|---|---|---|---|
| 0:00–0:40 abertura sem voz | lento | -17 a -28 LUFS | Atmosfera pura: close tingido de vermelho e 8 s de preto |
| 1:38–1:41 | corte no golpe | **pico de -8,5 LUFS** | Primeiro susto |
| 4:08–4:11 | câmera na mão | pico de -9,9 LUFS | Segundo susto |
| 6:45–7:10 | **0 cortes em 25 s** | -18 | Gravura antiga, com aproximação lenta |
| 8:40–9:50 | **0 cortes, 65 s** | **-29 a -31 LUFS**, o mais baixo | Suspense no escuro: a criatura surge aos poucos |
| 9:58–10:28 | **45 cortes por minuto**, o mais rápido | pico de -9,5 LUFS em 10:15 | Clímax em montagem |
| 11:58–12:15 | parado | trilha cantada | Encerramento |

## 3. Momentos importantes

| Tempo | O que acontece | Técnica |
|---|---|---|
| 0:00–0:21 | Closes de pelos, pés e um corpo no chão, **tudo tingido de vermelho** (duotone vermelho e preto), sem narração | Abertura sensorial: mostra a textura antes de explicar |
| 0:21–0:31 | **8 s de preto** e depois a imagem volta, **subindo do escuro em 9 s** | Respiração antes da história |
| 0:40 | Começa a narração em primeira pessoa ("sempre foi um tema que me fascinou…") | Tom de relato pessoal, não de apresentador |
| 0:36–1:30 | A cor troca a cada 6 a 8 s: âmbar, verde, azul, azul-petróleo, amarelo | Cada ideia tem sua cor |
| 1:12–1:28 | Trecho de filme de época (tribunal, multidão) e um lobisomem com ovelhas, em azul | Ilustra o folclore com cinema |
| **1:38–1:41** | Rosnado em close, **corte para o preto** e uma imagem surgindo dentro de um **círculo de lanterna**, com o **pico de volume do vídeo** | Susto: corte seco no golpe e revelação parcial |
| 1:43 | "Eu cresci no interior…": noite, fogueira, mato | Memória pessoal ilustrada com imagem noturna |
| **2:06–2:09** | Vídeo **vertical de celular** no centro de um quadro preto (gramado verde à noite), depois um **clarão de luz âmbar vazando (light leak)** e o preto | Material "amador" para parecer real e transição de luz |
| 2:48 e 3:04 | Ilustrações (desenho da criatura, figura encapuzada), algumas em janela menor | Mistura de linguagens: arte e registro |
| 3:12–3:28 | Rua de interior à noite sob luz âmbar e uma criatura em imagem de **câmera de trilha** | Prova "documental" de terror |
| ~4:00 | Linha ciano em zigue-zague sobre preto (gráfico ou onda) | Grafismo mínimo, na mesma cor do trecho |
| **4:08–4:11** | Imagem noturna em **azul-petróleo, câmera na mão tremendo**, com pico de volume | Segundo susto: imagem que não se vê bem |
| 4:23–4:35 | "O lobisomem do cinema…": cenas de filmes clássicos | Contraste entre o mito de cinema e o relato |
| 4:40–4:50 | **Clipes pequenos fora do centro** sobre preto | Enquadramento de "arquivo encontrado" |
| 5:44–5:52 | Desenho em **alto contraste invertido** (branco sobre preto) | Ilustração gráfica sem cor |
| 6:24 | Cena de filme com legenda original e tradução | Citação de filme |
| **6:46–7:14** | **Gravura antiga tingida de verde**, com aproximação muito lenta por **28 s** sem corte, sobre relatos da França e da Alemanha | Documento histórico tratado como cinema |
| 7:20–7:28 | Clipe vertical em janela e mancha branca em forma de crânio | Inserções gráficas curtas |
| 8:04–8:30 | Nuvens e floresta sob luz âmbar | Paisagem como pausa |
| 8:27 | "Não foi um uivo, foi uma espécie de lamento." | Frase-chave com silêncio em volta |
| **8:40–9:50** | **O plano mais longo (65 s):** quase preto, uma criatura pálida **emergindo do escuro**, closes nas pernas, de novo preto, e **olhos brilhando surgindo do preto** (9:36) | O suspense é a escuridão. Volume no mínimo do vídeo (-31 LUFS) |
| 9:52 | Floresta azul | Saída do escuro |
| **9:58–10:28** | **Clímax em montagem:** cores trocando a cada plano, câmera na mão em azul-petróleo, vidro quebrando em vermelho, luzes de polícia, câmera de trilha. **Pico de volume em 10:15** e sombra de lobisomem numa janela | O ritmo dispara até 45 cortes por minuto |
| 10:24–10:48 | Retratos antigos de pessoas com doença de pelos, em janelas e tons sépia | Hipótese médica com fotografia de época |
| 10:56 | Ilustração em silhuetas (sombras dançando) | |
| 11:36–11:58 | Imagens verdes escuras e depois preto | Desaceleração final |
| **11:58–12:15** | Cartão "**Obrigado por assistir <3**" em amarelo-esverdeado sobre cena tingida de vermelho, com **música cantada** e legenda da letra | Encerramento emocional, com a mesma cor da abertura |

## 4. Linguagem visual

### 4.1 Formato e escuridão

- **Formato cinemascope 2,36:1:** faixas pretas de cerca de 12% em cima e embaixo. É o sinal mais forte de "cinema", e vale o vídeo inteiro, não só alguns planos.
- **A escuridão é o estilo:**
  - 80% dos quadros são escuros, com brilho médio de 19%;
  - os pretos são esmagados, sem cinza leitoso;
  - a vinheta é pesada, com bordas em 30% do brilho do centro.
- **Imagem que nasce do escuro:** 18 entradas lentas a partir do preto, com **5,6 s em mediana** (de 1,3 a 14 s). A imagem não "entra", ela vai **aparecendo**.

### 4.2 Cor tingida, uma por ideia

- **Não há tratamento natural.** Cada trecho é **monocromático**: a imagem perde a cor original e ganha **um tom só** sobre o preto (duotone).
- **Frequência das cores** (amostras a cada 2 s):

| Cor | Amostras |
|---|---|
| Azul-petróleo/ciano | 86 |
| Âmbar/laranja | 69 |
| Verde | 65 |
| Preto puro | 46 |
| Azul | 44 |
| Vermelho | 29 |
| Amarelo | 22 |

- **Trocas:** a cor muda **a cada 6 a 28 s**, acompanhando o assunto. Por exemplo, vermelho na abertura e no fim, verde na gravura histórica, âmbar nas paisagens e azul-petróleo na câmera noturna.
- **Abertura e fecho na mesma cor** (vermelho): o vídeo fecha um ciclo.

### 4.3 Movimento

- **Aproximação lenta domina:** 61 planos aproximam contra 19 que afastam.
- **Zoom digital nas imagens paradas** (gravuras, fotos, ilustrações): **1,2% por segundo** em mediana (de 0,9% a 2,3%), em planos de **4 s**. É mais lento que na referência 05 e quase imperceptível, mas constante.
- **Câmera na mão** só no material "documental" (noite, câmera de trilha, celular) e nos sustos.
- **Janelas:** clipes verticais ou pequenos colocados **fora do centro** sobre o preto, como arquivos encontrados.
- **Círculo de lanterna:** revelação de uma imagem dentro de um círculo de luz.

### 4.4 Transições

| Tipo | Quantidade | Uso |
|---|---|---|
| Corte seco | 54 | Principalmente nos sustos e na montagem do clímax |
| Passagem pelo preto | 31 | Padrão entre ideias: o preto é a "pontuação" |
| Fusão | 22 | Entre paisagens e imagens do mesmo clima |
| Luz vazando (light leak) | raro | Um clarão âmbar, como em 2:08 |
| "Borrão" | 64 | Em geral é imagem escura e tremida, não um efeito |

Não há transições prontas de programa de edição.

## 5. Som

- **Dinâmico:** variação de 9,8 LU, contra 3,6 na referência 05. Há trechos de **-28 a -31 LUFS** (quase silêncio, ambiente) e **sustos a -8,5 a -10 LUFS momentâneo**. A diferença é de cerca de 20 dB.
- **Narração** a cerca de -18 LUFS momentâneo, com a trilha subindo nos respiros (pausas a -22,6 LUFS, só cerca de 4 LU abaixo da fala). A trilha **ocupa o espaço** quando a voz para.
- **Abertura de 40 s sem narração** e várias pausas longas: o som carrega a tensão.
- **Encerramento com música cantada** e a letra legendada.

## 6. Sincronia entre corte e som

| Teste | Nos cortes | Por acaso | Leitura |
|---|---|---|---|
| Corte com golpe de som forte por perto (100 ms) | **12,2%** | 6,4% | **1,9 vez o acaso: o corte vem junto com o impacto** |
| Corte na batida da trilha (60 ms) | 26,7% | 20,1% | Leve preferência pela batida (1,3 vez) |
| Corte em pausa da voz | 48,3% | 42,1% | Quase acaso, porque a narração tem muitas pausas |
| Corte no início de palavra | 34,9% | 33,5% | Acaso |
| Corte em fim de frase | 1,2% | 1,5% | Acaso |

**Leitura:** aqui quem manda no corte é o **som**, não a narração: o golpe, o rosnado, a batida. A voz conta a história por cima de blocos de imagem que respiram no tempo da trilha.

## 7. Como reproduzir em um documentário seu

### 7.1 Formato e imagem

1. **Formato cinemascope no vídeo inteiro.** Em 1920×1080, use faixas pretas de 133 px em cima e embaixo, o que deixa uma área útil de 1920×814 (2,36:1). No ffmpeg, ao fim da cadeia de cada plano: `drawbox=x=0:y=0:w=iw:h=133:color=black:t=fill,drawbox=x=0:y=ih-133:w=iw:h=133:color=black:t=fill`. Enquadre o assunto **dentro** dessa faixa e coloque a legenda logo abaixo dela, sobre o preto.
2. **Escureça de verdade.**
   - Brilho médio entre 15% e 25%, e pretos esmagados (`eq=contrast=1.35:brightness=-0.08`, ou uma curva que leve as sombras a zero).
   - Vinheta forte: `vignette=angle=PI/2.6`, ou uma máscara radial com as bordas em 30% a 40% do centro.
   - Só faça isso se a voz estiver clara: o escuro precisa da narração para guiar.
3. **Tinja por trecho, não o vídeo inteiro.**
   - **Receita:** tire a cor (`hue=s=0`) e aplique uma cor só (`colorchannelmixer` ou o filtro `colorize` do ffmpeg 5+).
   - **Exemplos de mistura** para `colorchannelmixer`:
     - vermelho: `rr=1.2:gr=0:br=0:rg=0.15:gg=0.05:bg=0:rb=0.1:gb=0:bb=0.05`
     - azul-petróleo: `rr=0.1:gr=0.8:br=0.75:rg=0:gg=0.15:bg=0.1:rb=0:gb=0:bb=0.15`
     - âmbar: `rr=1.1:gr=0.7:br=0.2:rg=0.1:gg=0.1:bg=0:rb=0:gb=0:bb=0.05`
   - Mantenha **uma cor por ideia, por 6 a 28 s**, e troque quando o assunto mudar. Defina um código, por exemplo:
     - vermelho: o corpo e a transformação;
     - verde: documento histórico;
     - azul-petróleo: relato noturno ou registro;
     - âmbar: paisagem e memória.
   - Abra e feche o vídeo na mesma cor.
4. **Faça a imagem nascer do escuro:** `fade=t=in:d=5`, entre 3 e 9 s, junto com uma aproximação lenta. Não use fade rápido de 0,5 s: aqui a regra é o tempo.
5. **Imagem parada:** aproxime de 1% a 2% por segundo, em planos de 4 a 8 s. Em gravuras e documentos, um único plano lento de 20 a 30 s funciona (como em 6:46–7:14).
6. **Material "achado":** coloque vídeos verticais de celular ou clipes pequenos **fora do centro** sobre o preto, sem preencher a tela. Isso dá autenticidade.

### 7.2 Ritmo

- **Base lenta:** de 9 a 14 cortes por minuto, com planos de 2 a 4 s e vários de 10 s ou mais.
- **Um plano extralongo de suspense** (30 a 65 s), no escuro, com a coisa surgindo aos poucos e o volume no mínimo. Coloque-o logo **antes** do clímax.
- **Clímax curto e rápido:** 30 s a cerca de 45 cortes por minuto, a cor trocando a cada plano, câmera na mão, e termine com um golpe de som.
- **Abertura sem voz:** de 20 a 40 s de imagem e som antes da primeira palavra.

### 7.3 Som e sustos

- **Dinâmica de 15 a 20 dB** entre a calmaria (cerca de -28 LUFS momentâneo) e o susto (cerca de -9). Não comprima tudo, porque o susto só funciona se houver silêncio antes.
- **Susto em três tempos:**
  1. trecho baixo, com 2 a 5 s de quase silêncio;
  2. **corte seco no golpe** (rosnado, impacto grave), com o golpe a até 100 ms do corte;
  3. **preto** de 0,3 a 1 s e revelação parcial (círculo de lanterna, imagem tremida, sombra).
- **De dois a três sustos em 12 min**, espaçados, nunca seguidos.
- **A trilha sobe nos respiros da voz:** só uns 4 LU abaixo da fala nas pausas, e mais baixa enquanto a voz fala.
- **Integrado entre -16 e -18 LUFS**, com pico de -1 dBTP. A referência estoura a +0,7, e isso não deve ser copiado.

### 7.4 Narração e texto

- **Primeira pessoa e memória:** "eu cresci no interior". A imagem acompanha a descrição ao pé da letra (braços longos, costas curvadas, olhos).
- **Texto na tela quase só em legendas:** de cenas em outra língua e da música final. Nada de títulos chamativos: o "cinema" vem da imagem.
- **Fecho com cartão simples** sobre a cor da abertura.

### 7.5 Para não ficar genérico ou artificial

- **Faixas pretas** só funcionam com imagem enquadrada para elas. Não esmague um rosto contra a borda.
- **Tingimento com um código fixo** (cada cor quer dizer algo). Cores trocadas ao acaso parecem filtro de aplicativo.
- **Escuridão com propósito:** o escuro vem antes da revelação. Escuro o tempo todo, sem nada surgir, cansa.
- **Sustos poucos e merecidos:** o golpe precisa do silêncio antes.
- **Zoom quase invisível** (1% a 2% por segundo). Zoom rápido em imagem parada denuncia montagem amadora.
- **Material autêntico:** vídeo de celular, câmera de trilha e gravuras históricas convencem mais que criatura de computador.

### 7.6 O que não copiar

- **Trechos de filmes de lobisomem e cenas de cinema:** há muitos na referência, e todos têm dono. Corre risco de reclamação e de perder a monetização.
- **Música cantada no fim:** não use música sem licença.
- **Ilustrações e artes tiradas da internet:** verifique a licença. Gravuras antigas (séculos XV a XIX) costumam ser de domínio público.

## 8. As duas referências lado a lado

| | Referência 05 (11 de setembro) | Referência 06 (lobisomem) |
|---|---|---|
| Gênero | investigação e denúncia | terror e mistério |
| Cortes por minuto | 26 (ondas de 10 a 36) | 9 a 14 (pico de 45 no clímax) |
| Plano mais longo | 21 s | 65 s |
| Imagem | arquivo colorido, sem tratamento, cheia de texto | escura, cinemascope, tingida por trecho, quase sem texto |
| Movimento em imagem parada | 2,5% por segundo, alternando | 1,2% por segundo, quase sempre aproximando |
| Corte guiado por | ideia falada (pausas) | som (golpe, batida) |
| Volume | comprimido (3,6 LU) | dinâmico (9,8 LU) |
| Narração | 204 palavras por minuto, 83% do tempo | 182 palavras por minuto, 54% do tempo |

**Para o Rasura:** a referência 05 serve para os vídeos de investigação com documentos, como o da escola. A **referência 06 serve para os de mistério**: "A Névoa de 1950" ficaria mais forte com formato cinemascope, tingimento por trecho, imagem nascendo do escuro e sustos de som.
