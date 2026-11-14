# Perfil de estilo medido nas 4 referências

> Data: 2026-11-14 · Tipo: análise · Status: vigente

**Resumo:** medições feitas com o `measure_reference.py` do editonny nas quatro referências do dono. São números de estilo (ritmo, posição de legenda, cor, volume), não cópia de conteúdo. As pastas com folhas de contato e `reference-rules.json` estão em `03-referencias/medicoes/`.

## Ritmo e som

| Referência | Cortes por minuto | Plano médio (s) | Plano mediano (s) | Plano mais longo (s) | Volume (LUFS) | Legenda (altura do centro) |
|---|---|---|---|---|---|---|
| 01 Poltergeist | 17.4 | 3.42 | 2.54 | 30.83 | -16.9 | 96% |
| 02 Hector RP | 13.1 | 4.53 | 2.67 | 36.3 | -12.8 | 98% |
| 03 Dark Academy | 15.4 | 3.85 | 2.42 | 33.0 | -18.4 | 90% |
| 04 Unabomber (JJ Dark Academy) | 21.4 | 2.78 | 2.13 | 14.0 | -18.0 | 56% |

## Cores dominantes (medidas nos pixels)

- **01 Poltergeist:** #07090B (black, 32%), #868686 (gray, 12%), #5B5D5C (gray, 12%), #B2B1AF (light gray, 11%)
- **02 Hector RP:** #040404 (black, 24%), #211F25 (black, 17%), #4F372F (red dark, 12%), #6A6161 (gray, 11%)
- **03 Dark Academy:** #060304 (black, 55%), #4B1415 (red dark, 9%), #8C8F7F (gray, 7%), #CCD7D1 (white, 7%)
- **04 Unabomber (JJ Dark Academy):** #020907 (black, 34%), #153315 (green dark, 16%), #54692B (yellow-green, 12%), #ADD6D3 (blue-green light, 11%)

## Como ler

- **A 04 é a mais rápida e a mais colorida:** 21 cortes por minuto, dominante verde-amarelo, volume mais baixo.
- **A 02 é a mais lenta:** 13 cortes por minuto, planos mais longos, voz mais alta (-12,8 LUFS).
- **As 01 e 03** ficam no meio, com 15 a 17 cortes por minuto.
- A medição de legenda e de efeitos sonoros é heurística e foi marcada como incerta pela ferramenta. A transcrição foi pulada (`--without-speech`).

## Comparação: referência 04 × vídeo do Rockefeller (v3)

| Medida | Referência 04 | Meu vídeo (v3) |
|---|---|---|
| Cortes por minuto | 21,4 | 18,2 |
| Plano médio | 2,78 s | 3,29 s |
| Plano mediano | 2,13 s | 2,92 s |
| Plano mais longo | 14,0 s | 24,4 s |
| Volume | -18,0 LUFS | -16,5 LUFS |
| Cor dominante | preto 34%, verde-escuro 16%, verde-amarelo 12% | preto 45%, amarelo-escuro 21% |
| Legenda (altura do centro) | 56% | 88% |

**Leitura:** o ritmo está a cerca de 15% abaixo da referência, e há planos longos demais (o mais longo tem 24 s, contra 14 s). A cor ficou parecida, mas mais escura e mais amarela. A legenda da referência fica no meio da tela, e a minha, embaixo.
