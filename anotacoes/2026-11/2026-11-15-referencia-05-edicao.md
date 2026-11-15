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
