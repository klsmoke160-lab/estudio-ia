# Referência 07: o Prédio 7 do World Trade Center (três partes)

> Data: 2026-11-17 · Tipo: análise · Status: vigente

**Resumo:** vídeo brasileiro de 8 min 50 s sobre a queda do Prédio 7 do World Trade Center, enviado pelo dono em três partes e analisado como um vídeo só. É investigação em tom de conversa e ironia, com corte rápido (21 por minuto), muita imagem de arquivo amador e de TV, texto em máquina de escrever sobre as imagens e inserções de humor. Este documento mede a edição, separa o que vale copiar do que não vale (direitos e precisão) e descreve como reproduzir cada recurso no motor do estúdio.

Arquivo: `03-referencias/_entrada/referencia_07.mp4` (640×360, 30 fps). Medições: `03-referencias/medicoes/07_referencia/` (cortes do editonny, quadros e áudio do `analisar_edicao.py`, cruzamento do `cruzar_edicao.py`, transcrição palavra por palavra).

## O que o vídeo diz (só para situar)

Ele começa com uma entrevista em inglês, legendada, sobre o cartaz de "procurado" de Bin Laden no site do FBI. Depois explica a versão oficial da queda do Prédio 7, ironiza ("tudo o que eu vou falar é ficção") e passa a falar dos ocupantes do prédio, do seguro e do dono das torres. **As afirmações dele não foram conferidas e não entram no nosso método como fato.** Interessa só a forma.

## Números da edição

| Medida | Referência 07 | Nosso MKUltra v3 | Referência 06 (terror) |
|---|---|---|---|
| Cortes por minuto | **21,1** | 12,8 | 9–14 |
| Plano mediano | **2,2 s** (10% abaixo de 0,45 s; 10% acima de 6,3 s) | cerca de 4 s | 4–9 s |
| Tipos de passagem | corte seco 64%, fusão 14%, passagem pelo preto 12%, borrão/chicote 10%, clarão 1 | corte seco e nascer do escuro | — |
| Movimento | zoom de aproximação em 25% dos planos, mediana **9%/s** (10% acima de 18%/s); afastamento a 13%/s; subida vertical em 15% | zoom de 4,5% por plano | 1–2%/s |
| Fala | **209 palavras por minuto falando**, pausa mediana 0,36 s, voz em 80% do vídeo | cerca de 130 | — |
| Corte na pausa da fala | **39%**, contra 19% do acaso: o dobro | — | — |
| Corte na batida da música | 13%, contra 23% do acaso: **não corta na música** | — | — |
| Volume | -16,1 LUFS, LRA 4 | -14,1, LRA 2,5 | — |
| Cor | brilho médio 108/255, saturação 49; 11% dos planos quase em preto e branco; 9% com faixas pretas laterais (arquivo 4:3) | escuro, tingido por capítulo | escuro |
| Telas pretas | 15, de 0,4 a 7,5 s | 4 (cartões) | — |

**Leitura:** o ritmo vem da **fala**, não da música. Ele corta quando o narrador respira, e o zoom é rápido e visível, quase um "empurrão" em cada plano. É o oposto do nosso MKUltra (lento, escuro, imagem que nasce do preto).

## Linha do tempo (tempos reais)

| Tempo | O que acontece | Recurso |
|---|---|---|
| 0:00–0:40 | Entrevista em inglês com legenda em português; insertos do cartaz do FBI com zoom | Abertura lenta (6 cortes/min), prova em documento logo no início |
| 0:40 | Preto com "Parte 1: A Construção" em máquina de escrever, branco, e "Entre 6 e 8" em vermelho | Cartão de capítulo com duas cores |
| 0:45–0:55 | Torres de baixo para cima, contra o céu | Contra-plongée para dar escala |
| 0:55 | Jogador de futebol abrindo os braços (meme), sobre imagem de destroços | Inserção de humor de 1 s |
| 1:00 | "(essas aqui)" escrito sobre as torres | Anotação na tela apontando o que a voz diz |
| 1:05–1:15 | Alarme de incêndio de banco de imagens | Ilustração literal da palavra dita |
| 1:20–2:00 | Imagens amadoras do 11/9 com a data da câmera na tela | Arquivo real e caótico, cortes rápidos |
| 2:05 | Preto com "NÃO FOI / PAGUE SEUS IMPOSTOS E CALE A BOCA" em vermelho | Cartão de ironia |
| 2:25 | Ícone de papel com a palavra "Papel" sobre o fogo | Ícone que salta para cada substantivo |
| 3:20 | Telejornal da BBC | Prova em vídeo de TV (direitos de emissora) |
| 3:50–4:30 | Lista de andares crescendo no canto superior esquerdo, em máquina de escrever, com logotipos (IRS, CIA, Departamento de Defesa) | **Lista que cresce**, com selo de cada órgão |
| 4:05 | Foto da Receita Federal do Brasil para explicar o IRS | **Analogia local** para o público brasileiro |
| 4:55 | Prédio da Hartford | Plano do lugar citado |
| 5:20, 7:40, 8:05 | Entrevistas do dono das torres (TV americana) | Rosto do personagem no momento em que é citado |
| 6:30–7:05 | "Amianto", "400 toneladas", "1,5 bilhões", "2001" em letra grande sobre as torres; foto de amianto; operários; bandeira do Brasil | **Palavra-chave grande sobre a imagem**, com analogia local |

## O que vale copiar

1. **Corte na respiração da voz.** É o que faz o vídeo parecer rápido sem ficar confuso. No motor, isso é quebrar cada frase em planos que terminam nas pausas da narração (a linha do tempo já tem o instante de cada palavra).
2. **Palavra-chave grande sobre a imagem** ("400 toneladas", "1,5 bilhões"). Temos o `KEY`. Vale usar em letra maior, no centro, só para números.
3. **Lista que cresce com selo do órgão.** Temos a `LISTA`. Falta o selo ao lado de cada item, que funcionaria bem na rede do MKUltra (universidades, hospitais, prisões).
4. **Analogia brasileira.** Explicar um órgão americano com o equivalente brasileiro (IRS e Receita Federal). Vale para CIA, FBI, Senado e Congresso. Use foto própria ou de domínio público.
5. **Zoom mais rápido nos planos de prova**, de 8% a 10% por segundo, só em documento e rosto. O resto fica com o zoom lento.
6. **Cartão de capítulo com duas cores** (título em branco e detalhe em vermelho). É parecido com o nosso cartão de capítulo.

## O que não copiar

- **Trechos de telejornal (BBC, Fox Business) e entrevistas de TV.** Têm dono e levam reivindicação de direitos ou desmonetização. Use documento, arquivo do governo ou citação narrada.
- **Meme com rosto de pessoa famosa** (o jogador de futebol). É direito de imagem, e o tom quebra o clima de documentário.
- **Ironia como escudo** ("é tudo ficção"). O Rasura separa o que está no documento do que não está. Esse truque vai contra isso.
- **Afirmações sem fonte** (seguro, BBC, satélite). Não entram em roteiro nosso sem conferência.
- **Resolução baixa** (360p) e misturas de formato sem tratamento.

## Como reproduzir no motor (`scripts/video/doc_motor.py`)

| Recurso | Como fazer |
|---|---|
| Ritmo de 18 a 22 cortes por minuto | No plano: `ESTILO["dur_plano"]=2.4`. A regra de cada frase lista 2 a 3 planos curtos |
| Corte na pausa | Usar o instante das palavras (`f["t"]`) para dividir a frase nas vírgulas e pausas, e não em partes iguais (melhoria a fazer no motor) |
| Palavra-chave grande | `KEY` com fonte Anton em 120 px, no centro, por 1,5 s, só para números |
| Lista com selos | `LISTA` mais um ícone PNG de domínio público ao lado de cada item (selos oficiais do governo dos EUA são de domínio público, mas o uso não pode sugerir apoio do órgão) |
| Cartão de ironia | Melhor não usar no Rasura. Se for usar, um `CARD` com frase curta em vermelho |
| Zoom rápido em prova | `zoom` por tipo de plano: 0,10 em `doc` e `foto`, 0,045 em `clip` |

## Para o Rasura

Esta referência mostra o tom de **canal de conversa**. As referências 05 e 06 mostram o tom de **documentário de cinema**. O dono pediu que o Mystère fosse a referência principal. Se este vídeo for o do Mystère, o estilo do canal precisa ficar mais rápido e mais falado do que está hoje. Se não for, ele serve como fonte de recursos pontuais: lista com selos, analogia brasileira e palavra-chave grande.
