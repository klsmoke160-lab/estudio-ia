# A Névoa de 1950: a cidade que virou um experimento secreto

> Data: 2026-11-12 · Tipo: projeto · Status: em produção

**Resumo:** documentário de mistério sobre a Operação Sea-Spray (São Francisco, 1950) e o caso Edward Nevin, para o canal do dono no YouTube. Roteiro do dono; esta pasta guarda a abertura (primeiros 82 s) como amostra de estilo.

## Critério de pronto

- Formato e duração: 16:9, 1920×1080, 24 fps. Amostra: 82 s (abertura). Vídeo inteiro: cerca de 15 min.
- Onde publica: YouTube.
- Motor: HTML + canvas, renderizado quadro a quadro com Playwright e ffmpeg (`motor/`).
- Pronto quando: o dono aprovar o estilo da amostra, gravar a narração e o vídeo inteiro for montado sobre ela.

## Checklist

- [x] 1. Ideia e critério de pronto
- [x] 2. Roteiro: texto final do dono (`roteiro.md`)
- [ ] 3. Narração: só existe a provisória, em voz sintética (Piper `pt_BR-faber`)
- [ ] 4. Aprovação do áudio
- [x] 5. Referências: 3 vídeos analisados (`referencias/analise.md`)
- [x] 6. Identidade visual: névoa cinza-azulada, vermelho do pigmento da Serratia, papel envelhecido
- [x] 7. Sound design da amostra (`audio/eventos.json`, `audio/mixar.py`)
- [x] 8. Montagem da amostra (`motor/index.html`)
- [ ] 9. Revisão e entrega
- [ ] 10. Aprendizados registrados

## Decisões

- **Sem imagens de terceiros.** Todas as cenas são desenhadas por código. As referências usam banco de imagens e trechos de outros canais, que não podemos copiar.
- **Nada de documento falso.** Os "papéis" são ícones estilizados com rótulo, não fac-símiles.
- **Só o que o roteiro afirma.** Nenhum número ou fato novo entra na tela.
- **Narração provisória.** A voz sintética serve para medir o tempo. A voz final é do dono.

## Fontes das imagens

Filmes do Arquivo Prelinger (archive.org), todos com licença marcada como domínio público: `Bridging1937`, `Operatio1946`, `Operatio1946_2`, `bacteria_friend_and_foe`, `atom_and_biological_science`, `Tubercul1955`, `mental_hospital`, `BoyinCou1940`, `NewspaperSto`, `Survival1951`, `Powersof1947`, `Doctorin1946`. As imagens são ilustrativas: nenhuma mostra a operação real.

## Como refazer

```bash
python3 audio/narrar.py      # narração provisória + timeline.json
python3 audio/cues.py        # marcas de tempo → motor/timeline.js
python3 audio/mixar.py       # mix.wav
node motor/render.mjs        # quadros em render/frames
```

## Entregas

| Versão | Arquivo | Data | Observação |
|---|---|---|---|
| v1 | `render/nevoa-1950-abertura-v1.mp4` | 2026-11-12 | Abertura de 82 s, só gráficos, voz provisória |
| v1 | `render/nevoa-1950-documentario-v1.mp4` | 2026-11-12 | Vídeo inteiro, 17 min 40 s, filmes de arquivo em domínio público (Prelinger), voz sintética `pt_BR-cadu` |
