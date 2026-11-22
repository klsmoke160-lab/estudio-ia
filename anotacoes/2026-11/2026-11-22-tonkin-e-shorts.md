# Sessão: Shorts "você criou", vozes do ElevenLabs e documentário do Golfo de Tonkin

> Data: 2026-11-22 · Tipo: anotação · Status: vigente

**Resumo:** criei o modelo de Short "Parabéns, você criou…" a partir da referência 08, montei o Short do MKUltra (v4 com a voz Davi), testei vozes no ElevenLabs e deixei pronto, faltando só a narração, um documentário novo sobre o Golfo de Tonkin.

## O que foi feito

- Referência 08 analisada; modelo em `06-metodo/modelo-short-voce-cria.md`; motor `scripts/video/short_voce.py` (zoom dos filmes em Python, porque o `scale` com `eval=frame` do ffmpeg travava com memória corrompida); capa vertical `scripts/video/capa_short.py`.
- Short do MKUltra: v4 com a voz Davi (`render/mkultra-voce-criou-v4.mp4`).
- Golfo de Tonkin: pesquisa no National Security Archive (estudo da NSA de Hanyok, OCR das páginas), 6 filmes de domínio público, documentos com marca-texto, plano testado, capa e pacote de publicação.

## Aprendizados

- **ElevenLabs:** a conta está no plano gratuito (10 mil caracteres por mês, sem licença comercial). Um documentário de 10 min tem cerca de 8.500 caracteres. Antes de gerar, conferir saldo e plano com `account_get_usage`.
- **Siglas:** com as vozes Lucas e Davi, "CIA" se escreve "Sía". Testar sigla nova com uma frase curta.
- **Voz renomeada na biblioteca:** a "Gabriel" passou a se chamar como uma pessoa famosa. Conferir o nome atual antes de usar.
- **"Queima de arquivo"** em português é silenciar testemunha, não destruir papéis.
- **Escolher frase de cartão (CARDS)** com até 18 caracteres: mais que isso sai cortado na tela.
- **`%` em texto do drawtext** quebra a expansão: escrever "por cento".
