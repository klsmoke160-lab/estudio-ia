# Referência 05: estilo de edição (documentário sobre o 11 de setembro, partes 1 e 2)

> Data: 2026-11-15 · Tipo: análise · Status: vigente

**Resumo:** análise técnica da edição de um documentário em português de 17:39, enviado em duas partes (`claude_edicao_parte_01.mp4` e `_02.mp4`) e analisado como um vídeo só. Tudo foi medido quadro a quadro e cruzado com a transcrição palavra por palavra: cortes, movimento, transições, cor, som e sincronia com a voz. O guia diz como reproduzir a linguagem da edição em outro vídeo. O conteúdo do vídeo (teorias sobre o 11 de setembro) não foi avaliado nem deve ser copiado.

## Como foi medido

- **Cortes, texto na tela, rostos, cor e volume:** com o `measure_reference.py` do editonny. O resultado completo está em `03-referencias/medicoes/05_edicao_claude/style-guide.md`.
- **Movimento de cada plano:** zoom, panorâmica, inclinação e tremor, medidos quadro a quadro por ECC (OpenCV) com `scripts/video/analisar_edicao.py`. O sinal foi testado com uma imagem sintética: escala acima de 1 é aproximação.
- **Transições:** classificadas pelo brilho, pela nitidez e pela diferença entre os quadros em volta de cada corte. Exemplos de cada tipo foram conferidos em tiras de 10 quadros por segundo.
- **Narração:** transcrita com Whisper, em português e palavra por palavra. Cada corte foi comparado com pausas, fins de frase e inícios de palavra, e sempre contra uma base aleatória ("o que daria por acaso").
- **Trilha:** batidas, golpes e volume momentâneo, medidos com librosa e com o ebur128 do ffmpeg.
- **Cruzamento:** `scripts/video/cruzar_edicao.py`. Os números ficam em `medicoes/05_edicao_claude/aprofundado/resumo.json`.

**Limites da medição:**
- O arquivo tem 640×360, então detalhes finos (grão, fonte exata) são estimativas.
- O movimento medido inclui o da câmera original dos filmes de arquivo. Por isso o zoom digital do editor foi isolado à parte (seção 4.1).
- A classificação de transições é automática. As categorias "borrão" e "clarão" misturam transições reais com cortes para imagens claras ou tremidas.

## 1. Ficha técnica

| Medida | Valor |
|---|---|
| Duração | 17:39 (1059 s), 30 quadros/s |
| Cortes | 457 (355 nítidos e 102 fracos) |
| Cortes por minuto | **25,9** (20,1 contando só os nítidos) |
| Duração do plano | mediana **1,63 s**, média 2,31 s; 10% abaixo de 0,47 s e 10% acima de 4,75 s |
| Plano mais longo | 20,7 s (10:09–10:29) |
| Planos com algum movimento | **88%** |
| Narração | **204 palavras por minuto** falando; a voz ocupa **83%** do vídeo; pausa mediana de 0,34 s; só 11 pausas acima de 1 s |
| Volume | **-16,1 LUFS** integrado, variação de só **3,6 LU** (muito comprimido), pico real de +1,7 dBTP (estoura) |
| Trilha | contínua, uns **10 LU abaixo da voz**: a fala fica em -16,9 LUFS momentâneo e as pausas, só com trilha, em -26,5. Termina uns 13 s antes do fim |

## 2. Estrutura e curva de ritmo

O vídeo é dividido em **9 partes** com cartão de capítulo. O ritmo vem em **ondas**: começa devagar, sobe, desacelera no meio para explicar, e acelera forte no terço final, que é o clímax.

| Trecho | Início | Duração | Cortes/min | Plano mediano | Planos com movimento |
|---|---|---|---|---|---|
| Abertura fria e título | 0:00 | 42 s | **9,9** | 2,47 s | 57% |
| Parte 1: A Construção *Entre 6 e 8* | 0:42 | 74 s | 26,7 | 1,77 s | 89% |
| Partes 2 e 3: Questionamentos… | 1:56 | 198 s | 24,9 | 1,83 s | 88% |
| Parte 4: *Quem* Ganharia Com Isso? | 5:14 | 52 s | 16,2 | 2,30 s | 82% |
| Parte 5: *Amianto* | 6:05 | 249 s | 19,0 | 2,70 s | 83% |
| Parte 6: *A Importância* Dessa Construção | 10:15 | 171 s | **35,8** | 1,07 s | 91% |
| Parte 7: O Grupo *Carlyle* | 13:06 | 100 s | 30,1 | 1,60 s | 72% |
| Parte 8: *Árabes?* | 14:45 | 123 s | **35,2** | 1,20 s | 90% |
| Parte 9: *11* | 16:48 | 50 s | 21,4 | 2,57 s | 89% |

O cartão da Parte 3 não foi localizado, e as Partes 2 e 3 foram medidas juntas. O trecho mais rápido do vídeo fica entre 10:30 e 11:10, com até **66 cortes por minuto** numa janela de 20 s.

## 3. Momentos importantes

Os tempos marcados com "~" foram tirados de folhas de contato de 10 em 10 segundos e têm margem de cerca de 5 s.

| Tempo | O que acontece | Por que importa |
|---|---|---|
| 0:00–0:10 | Abertura fria: um entrevistado estrangeiro com legenda em português, **10 s sem corte**, com aproximação lenta no rosto | Gancho por autoridade: o vídeo começa no meio de uma fala, sem vinheta |
| 0:10–0:17 | Documento (cartaz oficial) com **faixa verde de destaque** e trecho em vermelho | Prova visual logo nos primeiros segundos |
| 0:18–0:20 | **Cartão "AVISO:"**: título vermelho de máquina de escrever, com letras tremendo, e texto de isenção em branco miúdo | Protege o canal e cria clima |
| 0:20–0:36 | Volta à entrevista, com **foto inserida no canto** (imagem dentro da imagem) | Aponta a fonte enquanto a pessoa fala |
| 0:39 | **Cartão de título**: nome do canal em amarelo, imagem vertical no centro e título em duas linhas | Abre o vídeo depois do gancho, aos 39 s |
| 1:08–1:20 | **Ilustração literal**: rótulo "Manual" de máquina de escrever sobre um alarme de incêndio, e uma mão puxando a alavanca | Cada informação dita vira imagem concreta |
| ~1:26 | **Meme** inserido: um personagem de anime lendo | Humor como respiro; aqui o direito de uso é um risco |
| 1:53–2:01 | "**é…**" em branco grande (1 s), **silêncio total** de cerca de 0,3 s e depois "Parte 2: Questionamentos…". Cerca de 7,5 s de preto no total | Pausa dramática que reinicia a atenção |
| 2:05–2:09 | "**NÃO FOI / PAGUE SEUS IMPOSTOS E CALE A BOCA**" em vermelho manuscrito tremido sobre preto, com o **som mais alto do vídeo** (-7 LUFS momentâneo), e corte seco para um discurso | Cartão de comentário irônico: a voz do canal aparece como texto |
| ~3:03 | Mapa com região em vermelho e rótulo "Alaska" | Geografia explicada com destaque de cor |
| 3:48 | "**olha só**" em amarelo, máquina de escrever, sobre preto | Comentário curto que puxa a atenção |
| 3:50–4:35 | **Lista que cresce** no canto superior esquerdo ("0-6, 13, 18-46: Salomon Brothers / … / 24: IRS / 25: CIA, Departamento de Defesa"). A cada item, o **selo do órgão aparece** no canto inferior direito, com **respiros pretos de 0,6 a 1,3 s** entre os passos | Enumera dados sem tela cheia de texto, criando suspense item a item |
| ~4:10 | "**Curioso, né?**" sobre a imagem | Comentário irônico em forma de rótulo |
| 5:14 | Cartão "Parte 4: **Quem** Ganharia Com Isso?" | O ritmo cai para explicar |
| ~5:30 | "**3.2 Bilhões**" escrito sobre a imagem | Número dito vira texto na tela |
| ~9:10 | "**34.000%**" grande, em vermelho, sobre a imagem | O número de maior impacto ganha cor de alerta |
| 9:20–10:09 | Entrevista antiga de estúdio, com planos mais longos | Prova por depoimento, desacelera antes do clímax |
| 10:15 | Cartão "Parte 6: **A Importância** Dessa Construção" | Começa a parte mais rápida |
| 10:38–11:01 | **Montagem mais rápida**: torres filmadas de baixo em lente olho de peixe girando, intercaladas com **o mesmo gráfico repetido três vezes** | O gráfico repetido funciona como batida visual, uma ideia martelada |
| ~11:40 | Tarja de noticiário ("Crisis on Wall St") e gráfico de bolsa | Contexto por material de TV |
| 13:06 | Cartão "Parte 7: O Grupo **Carlyle**" | |
| ~14:10–14:30 | **Documento em tabela** (executivos), logotipo em tela branca e colagem de fotos | Rede de nomes montada como quadro de investigação |
| 14:45 | Cartão "Parte 8: **Árabes?**" | |
| ~15:30 | **Lista numerada** de máquina de escrever sobre a imagem ("… 101: 1, 2, 3") | O raciocínio vira passo a passo |
| 16:48 | Cartão "Parte 9: **11**" | |
| 17:24–17:28 | Texto de notícia sobre preto, com o **segundo golpe mais alto** (-6,5 LUFS) | Fecha com impacto |
| 17:28–17:39 | Jornal antigo e a legenda "Você pode pesquisar todas as informações desse vídeo"; a trilha já acabou | Encerramento sóbrio, com convite a checar |

## 4. Linguagem visual

### 4.1 Movimento: nada fica parado

- **88% dos planos se mexem.** Imagem parada só em entrevista e em cartão.
- **Zoom digital nas imagens paradas** (fotos, documentos, logotipos), isolado da câmera original:
  - 79 planos com zoom suave e constante, 61% aproximando e 39% afastando, alternando;
  - velocidade mediana de **+2,5% por segundo para aproximar** (metade dos casos entre 1,1% e 5,2%) e **-2,2% por segundo para afastar**;
  - esses planos duram em mediana **2 s**, então o zoom total fica em torno de 5% por plano: sutil, mas sempre presente.
- **Documentos:** além do zoom, metade deles é **rolada na vertical**, para baixo ou para cima, como quem lê a página.
- **Filmes de arquivo:** guardam o movimento original (câmera na mão, torres filmadas de baixo, olho de peixe girando). O editor escolhe trechos que já se mexem.
- **Tremor proposital:** só nos cartões de texto ("AVISO", "NÃO FOI…"). As letras pulam alguns pixels, com aspecto de máquina de escrever ou de filme antigo.

### 4.2 Transições

| Tipo | Quantidade | Uso |
|---|---|---|
| Corte seco | 260 (57%) | Padrão em todo o vídeo |
| Fusão curta (dissolvência) | 74 (16%) | Entre imagens do mesmo assunto, como fumaça para fumaça ou prédio para prédio |
| Passagem pelo preto | 33 (7%) | Só para entrar e sair de cartões (capítulo, aviso, comentário) e entre os passos da lista que cresce |
| Borrão de movimento | 83 (18%) | Mistura transições de giro rápido, na montagem de 10:38, com cortes para planos tremidos. Use com moderação |
| Clarão | 7 | Raro. Vários são cortes para documento branco, não um flash de verdade |

Não há transições prontas de programa de edição (cortina, cubo, página virando). A "transição" característica é o **preto**: fade de cerca de 0,5 s da imagem para o preto, o cartão, e fade de volta.

### 4.3 Texto na tela (o centro do estilo)

| Elemento | Como é | Quando aparece |
|---|---|---|
| Legenda de entrevista estrangeira | Uma linha clara, embaixo (centro a ~98% da altura), sem caixa | Só nas falas em outra língua |
| Rótulo de máquina de escrever | Fonte de máquina de escrever, branca ou amarela, sobre a imagem, sem caixa | Quando a narração diz um nome, lugar ou número ("Manual", "Alaska", "3.2 Bilhões", "Curioso, né?") |
| Número de impacto | Grande, em vermelho, sobre a imagem ("34.000%") | O dado mais forte do capítulo |
| Lista que cresce | Canto superior esquerdo, máquina de escrever, um item por vez, com o selo correspondente aparecendo | Enumerações (andares, órgãos, nomes) |
| Lista numerada | Título e itens 1-2-3 sobre a imagem | Passo a passo de um raciocínio |
| Cartão de capítulo | Fundo preto, texto pequeno e centralizado: "Parte N:" em branco e a palavra-chave em **vermelho** (ou amarelo). Dura cerca de 1,5 s | Começo de cada uma das 9 partes |
| Cartão de comentário | Fundo preto; **a cada vez uma fonte e cor diferente** ("é…" branco grande, "olha só" amarelo de máquina de escrever, "NÃO FOI…" vermelho manuscrito tremido). Vem com silêncio ou golpe de som | Ironia ou reação do narrador; 3 a 4 vezes no vídeo |
| Aviso | "AVISO:" vermelho tremido e texto de isenção miúdo | Uma vez, aos 18 s |
| Destaque em documento | Faixa verde translúcida sobre a linha e trecho em vermelho | Quando a narração cita o documento |
| Setas e marcações | Seta vermelha apontando um ponto da imagem, com rótulo | Para mostrar onde olhar |

O medidor registrou texto na tela em **67% do tempo** e **55 trocas de texto por minuto**.

### 4.4 Imagens

São noticiário de época (com a marca da emissora visível), entrevistas, documentos e páginas, gráficos, mapas com destaque, logotipos de empresas e órgãos sobre fundo liso, colagens de fotos, imagens dentro da imagem e **ilustração literal** do que é dito. Cada substantivo tem sua imagem: "alarme manual" vira o alarme sendo puxado, "Receita Federal" vira o prédio com o nome.

### 4.5 Cor

- **Não há tratamento de cor único.** O material de arquivo fica com a cor original:
  - brilho médio de 40%, saturação moderada;
  - 9% dos planos quase em preto e branco;
  - 10% com faixas pretas, de material 4:3;
  - vinheta fraca (cantos com 92% do brilho do centro).
- **A identidade de cor vem dos cartões:** preto chapado, branco, e destaque **vermelho** (alerta) e **amarelo** (comentário ou palavra-chave). É uma paleta de três cores sobre o preto.

## 5. Som

- **Voz no centro, quase sem respiro:** 204 palavras por minuto, 83% do tempo com fala e só 11 pausas acima de 1 s.
- **Trilha contínua e baixa**, cerca de 10 LU abaixo da voz. Não acompanha os cortes: só 23% dos cortes caem perto de uma batida, contra 26% que cairiam por acaso.
- **Efeitos sonoros discretos**, cerca de 26 por minuto segundo o medidor (estimativa, que inclui respiração e batidas). Eles **não estão presos aos cortes**: 6,6% dos cortes têm golpe forte por perto, contra 6,8% por acaso.
- **Golpes fortes reservados aos cartões de impacto:** os dois picos de volume do vídeo são o "NÃO FOI…", em 2:08 (-7 LUFS momentâneo), e o fecho em 17:28 (-6,5). Fora disso, o volume quase não varia (3,6 LU).
- **Silêncio como efeito:** antes de "Parte 2" o som cai para silêncio absoluto por cerca de 0,3 s.
- **Final:** a trilha some uns 13 s antes do fim, e o encerramento fica só com a voz.

## 6. Sincronia entre corte e narração

| Teste | Nos cortes | Por acaso | Leitura |
|---|---|---|---|
| Corte dentro de uma pausa da voz | **28,2%** | 15,0% | 1,9 vez o acaso: o editor prefere cortar no respiro |
| Corte a até 150 ms de um fim de frase | **7,2%** | 3,2% | 2,2 vezes o acaso, mas é minoria |
| Corte a até 120 ms do início de uma palavra | 55,8% | 55,2% | Igual ao acaso: não corta na sílaba |
| Corte na batida da trilha | 23,0% | 26,2% | Não segue a música |
| Corte com golpe de som por perto | 6,6% | 6,8% | Não segue os efeitos |

**Leitura:** a edição é guiada pela **ideia falada**. A imagem troca quando a narração passa a outro assunto, nome ou número, e de preferência num respiro. Não segue sílaba, batida nem efeito sonoro. Como a voz é muito rápida e contínua, isso já gera de 25 a 36 cortes por minuto nos trechos densos.

## 7. Guia técnico para reproduzir em outro vídeo

### 7.1 Ritmo

1. **Abra devagar:** de 30 a 40 s de gancho com no máximo 10 cortes por minuto. Uma fala forte (entrevista ou narração) sobre um plano longo, com aproximação lenta, e só depois o título.
2. **Desenhe a curva por capítulo, não uma média:**
   - capítulos de contexto entre 16 e 20 cortes por minuto (plano mediano de 2,3 a 2,7 s);
   - capítulos de prova entre 25 e 27 (cerca de 1,8 s);
   - clímax entre 30 e 36 (1,1 a 1,6 s);
   - fecho em cerca de 21.
3. **Um plano por informação:** cada nome, número, lugar ou objeto citado ganha sua imagem. Se a frase tem três dados, são três planos.
4. **Corte no respiro quando der:** mire a pausa entre frases, e não a sílaba nem a batida. Na prática, coloque o corte no meio da pausa, ou até 50 ms antes da primeira palavra da frase seguinte.
5. **Repetição como batida:** no clímax, intercale o mesmo plano-chave (um gráfico ou documento) duas ou três vezes entre imagens em movimento.

### 7.2 Movimento

- **Nenhuma imagem parada fica estática.**
  - Fotos e logotipos: zoom de **+2,5% por segundo** (aproximando) ou **-2,2% por segundo** (afastando), alternando cerca de 60/40, em planos de cerca de 2 s.
  - Documentos: alternar zoom com **rolagem vertical lenta**.
- **Filmes de arquivo:** escolha trechos que já tenham movimento de câmera e não acrescente zoom por cima.
- **No `montar.py` do estúdio**, o zoom atual é de 7% por plano, linear. Para este estilo, use `z=1+0.025*t` (aproximar) ou `z=1.05-0.022*t` (afastar), alternando por plano, e evite planos de imagem parada sem movimento.

### 7.3 Cartões (a assinatura)

- **Capítulo:**
  - fade da imagem para o preto em cerca de 0,5 s;
  - texto **pequeno**, de 3% a 4% da altura da tela, centralizado: "Parte N:" em branco e a **palavra-chave em vermelho** (ou amarelo quando for um tema, não um alerta);
  - fica cerca de 1,5 s e volta com fade de cerca de 0,5 s.
- **Comentário irônico:** 1 a 2 s sobre preto, com **fonte e cor diferentes do resto** (manuscrita vermelha, máquina de escrever amarela, branca grande). Antes, **0,3 s de silêncio**. Junto, **um golpe grave** (é o pico de volume do vídeo). Use de 3 a 4 vezes em 15 min, nunca seguidos.
- **Aviso:** um só, nos primeiros 20 s, se o tema pedir.
- **Tremor das letras:** sorteie um deslocamento de ±2 a 3 px e um leve giro de ±0,5°, trocando 12 vezes por segundo, para a letra "pular" como filme antigo.

### 7.4 Texto sobre a imagem

- Fonte de **máquina de escrever** para rótulos e listas (no estúdio: `font2.ttf`; alternativas abertas: Special Elite, Courier Prime). Sem caixa de fundo, com sombra leve.
- Branco para informação, **amarelo** para comentário e **vermelho** para alerta ou número de impacto.
- **Rótulo:** entra no momento em que a palavra é dita e fica até o fim do plano.
- **Lista que cresce:** no canto superior esquerdo, um item por vez, cada item digitado letra a letra (de 25 a 35 letras por segundo). O selo correspondente surge no canto inferior direito, e há um respiro preto de 0,6 a 1 s entre os passos.
- **Destaque em documento:** faixa translúcida verde ou amarela sobre a linha citada, entrando no momento da citação.

### 7.5 Som

- **Voz:** cerca de -16 LUFS, comprimida, com variação abaixo de 4 LU.
- **Trilha:** contínua, **10 LU abaixo da voz**, sem montar os cortes na batida. Termine a trilha de 10 a 15 s antes do fim.
- **Golpes fortes:** só nos cartões de comentário e no fecho. No resto, efeitos baixos e esparsos.
- **Silêncio:** 0,3 s de silêncio absoluto antes de cartões dramáticos.
- **Pico:** -1 dBTP. A referência estoura a +1,7 dBTP, e esse erro não deve ser copiado.

### 7.6 O que não copiar

- **Memes e personagens de terceiros** (anime, desenhos): risco de direito autoral e de monetização. Para o humor, use material próprio ou de domínio público.
- **Marca de emissora na tela:** aparece muito na referência e é motivo de reclamação de direitos. Prefira arquivos de domínio público.
- **Música da referência:** nunca reutilizar.
- **O tom de "verdade escondida" sem fonte:** o Rasura usa a mesma linguagem visual, mas mostra o documento e diz o que ele prova e o que não prova.

## 8. Comparação com o vídeo do Rasura ("Perfeita docilidade", v10)

| Medida | Referência 05 | Rasura v10 |
|---|---|---|
| Cortes por minuto | 25,9 (ondas de 10 a 36) | ~22,7 (mais uniforme) |
| Cartões de capítulo | preto, texto pequeno, palavra em vermelho | animados, título grande letra a letra, traço vermelho e queima de filme |
| Cartões de comentário irônico | sim, 3 a 4 | não |
| Lista que cresce | sim | não |
| Rótulos de máquina de escrever sobre a imagem | constantes | títulos-chave no alto |
| Zoom digital nas imagens paradas | 2 a 2,5% por segundo, alternando | cerca de 7% por plano, alternando |
| Trilha | 10 LU abaixo da voz, contínua | base grave sintetizada e efeitos nos títulos |

**O que mais vale trazer para o próximo vídeo do Rasura:**
1. Curva de ritmo em ondas, com um clímax a mais de 30 cortes por minuto.
2. Cartões de comentário com silêncio antes e golpe junto.
3. A lista que cresce item a item, com selo.
4. Ilustração literal de cada nome e número dito.
5. Repetir o documento-chave como batida no clímax.
