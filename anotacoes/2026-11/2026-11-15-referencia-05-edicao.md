# Análise de edição da referência 05 (11 de setembro, partes 1 e 2)

> Data: 2026-11-15 · Projeto: 03-referencias

- **Pedido:** analisar as duas partes como um vídeo só e fazer um guia técnico para reproduzir a edição.
- **Feito:**
  - juntei as partes e rodei o `measure_reference.py` do editonny;
  - criei `scripts/video/analisar_edicao.py` (medições quadro a quadro: movimento por ECC, cor, nitidez, áudio) e `scripts/video/cruzar_edicao.py` (cruza cortes, movimento, transições, fala e trilha, sempre contra uma base aleatória);
  - guia em `03-referencias/analises/2026-11-15-referencia-05-edicao-claude.md`.
- **Aprendizados:**
  - O Whisper detectou inglês por causa da entrevista inicial e "traduziu" a narração. Em vídeo brasileiro, force `language="pt"`.
  - O movimento medido mistura câmera original e zoom do editor. O zoom do editor se isola pelos planos de escala constante e diferença residual baixa.
  - Teste de sincronia sem base aleatória engana: "55% dos cortes no início de palavra" era exatamente o acaso.
- **Próximo:** aplicar no próximo vídeo do Rasura a curva de ritmo em ondas, os cartões de comentário e a lista que cresce.

## Referência 06 (lobisomem, partes 1 e 2)

- **Feito:** mesmo método da 05, mais medições de vinheta dentro da área útil, cor dominante a cada 2 s e entradas do escuro. Guia em `03-referencias/analises/2026-11-15-referencia-06-terror-lobisomem.md`.
- **Aprendizado:** em vídeo escuro com faixas pretas, a vinheta tem que ser medida dentro da área útil (a medida pelos cantos dá errado). O detector de cortes perde trocas dentro do preto, então o número de cortes é um piso.
- **Próximo:** usar a 06 como modelo para os vídeos de mistério (Névoa de 1950) e a 05 para os de investigação.
