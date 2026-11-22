# Referência 09: capas de iceberg do Mistère

> Data: 2026-11-23 · Tipo: análise · Status: vigente

**Resumo:** print enviado pelo dono de duas capas de vídeos de iceberg do canal Mistère ("O Iceberg de Mistérios do Brasil #2", 76 mil views, 38:15; "O Iceberg de Pessoas Misteriosas", 104 mil views, 1:02:24). O Mistère é a referência principal do Rasura. Este doc descreve o padrão visual e como reproduzi-lo só com imagens reais.

Print: `03-referencias/analises/prints/2026-11-23-mistere-capas-iceberg.jpg`.

## O padrão

- **Fundo preto** com brilho vermelho em volta do iceberg.
- **Iceberg vermelho e alaranjado à esquerda**, com a parte de cima e a parte submersa visíveis, separadas pela linha da água. Parece ilustração (o Rasura não copia esse ponto: usa foto real).
- **Título em serifa itálica, grande e branco**, com sombra preta ("PESSOAS BIZARRAS", "MISTÉRIOS BRASILEIROS"), sobre ou ao lado do iceberg. Duas palavras.
- **Rostos à direita**, em preto e branco ou dessaturados, recortados e fundidos no escuro, com **tarja preta nos olhos**. De 2 a 6 rostos, em grupo.
- **Número da série** ("#2") no canto, quando é continuação.
- Paleta só de preto, vermelho, branco e cinza.

## Como o Rasura reproduz (capa do Iceberg das Conspirações)

- Script: `04-projetos/2026-11-23-iceberg-das-conspiracoes/capa/capa_mistere.py`.
- **Iceberg:** foto real da NASA (North Star Bay, Groenlândia, Operation IceBridge, 2015), recortada pelo contorno e recolorida em vermelho e laranja. A parte de baixo é o reflexo da própria foto na água, escurecido.
- **Título:** DM Serif Display Italic (`05-biblioteca/fontes/serif.ttf`), "O ICEBERG DAS / CONSPIRAÇÕES".
- **Rostos:** fotos reais de pessoas dos casos do vídeo (Sidney Gottlieb, Lyndon Johnson, Wernher von Braun), em preto e branco, com borda esfumada e tarja nos olhos. O rosto é achado pelo OpenCV (detector clássico, não é IA generativa) e a tarja ajustada pessoa a pessoa.
- **Sem imagem gerada por IA.**
