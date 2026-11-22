# O Iceberg das Conspirações: até onde vai a verdade?

> Data: 2026-11-23 · Tipo: projeto · Status: v1 montada e conferida; narração de conta gratuita do ElevenLabs (sem licença comercial)

**Resumo:** documentário longo do Rasura (cerca de 11 a 12 min, 1.495 palavras, 9 capítulos) que organiza teorias da conspiração num iceberg medido por uma régua só, o que está nos documentos. No topo, o que governos confessaram (Northwoods, Tuskegee, MKUltra); depois, o que foi provado por papéis arrancados (COINTELPRO, Tonkin, Paperclip); no meio, segredos reais que viraram lenda (Área 51 e U-2, Roswell e Mogul, Stargate); embaixo, o que não tem prova (pouso falso na Lua) e, no fundo, a Terra plana. Conclusão: a parte assustadora está no topo.

## Critério de pronto

- 16:9, 1920×1080, motor `scripts/video/doc_motor.py`, formato de cinema, uma cor por nível, -16 LUFS.
- Pronto quando a narração chegar (voz Davi, de preferência com licença comercial), for tratada por `scripts/som/tratar_narracao.py` e o vídeo for montado e conferido.

## Gancho (regra em `06-metodo/ganchos.md`)

Comparados por dentro (o dono pediu o vídeo, não o roteiro):
1. **Documento (escolhido):** "Em 13 de março de 1962, o general mais graduado dos Estados Unidos assinou um plano para explodir um navio americano e culpar Cuba. Isso não é teoria da conspiração." Primeiro quadro: a linha do memorando da Northwoods marcada em amarelo.
2. **Contradição:** "As conspirações que se provaram verdadeiras não foram descobertas por quem acredita em tudo."
3. **Pergunta-iceberg:** "Quanto mais fundo uma teoria da conspiração, menos documentos ela tem."

O 1 ganhou porque é concreto, verificável na tela e já mostra a régua do vídeo (documento). O 2 e o 3 viraram a conclusão.

## Como montar quando a narração chegar

O texto para a voz está em `texto-para-voz.txt` (8.900 caracteres; "CIA" escrito "Sía", "U-2" como "U dois", "FBI" como "efe-bê-í"). O ElevenLabs aceita até 5.000 caracteres por geração: gerar em duas partes, cortando na troca de capítulo, e juntar com 1,2 s de silêncio.

```bash
cd /home/user/estudio-ia
uv run python scripts/som/tratar_narracao.py 04-projetos/2026-11-23-iceberg-das-conspiracoes <audio.mp3> --linha 0 --curta 0.9
python3 scripts/video/doc_motor.py 04-projetos/2026-11-23-iceberg-das-conspiracoes edl
python3 scripts/video/doc_motor.py 04-projetos/2026-11-23-iceberg-das-conspiracoes render
python3 scripts/video/doc_motor.py 04-projetos/2026-11-23-iceberg-das-conspiracoes juntar
python3 scripts/video/doc_motor.py 04-projetos/2026-11-23-iceberg-das-conspiracoes som
python3 scripts/video/doc_motor.py 04-projetos/2026-11-23-iceberg-das-conspiracoes final iceberg-v1.mp4
```

Plano testado com linha do tempo simulada: 161 planos, todas as regras casam com uma frase, um plano de cada fonte nova renderizado e conferido.

## Fontes conferidas (23/11)

- **Northwoods, MKUltra, Paperclip, Golfo de Tonkin:** fontes nos READMEs dos projetos de 15/11, 17/11, 18/11 e 22/11 (memorando de 1962; Senado 1977; nota de Ford 1975; Arquivo Nacional; estudo da NSA de Hanyok).
- **Tuskegee:** discurso de Bill Clinton, 16/05/1997 ("40 years", "even once a cure was discovered, they were denied help, and they were lied to by their Government", "I am sorry"): <https://www.presidency.ucsb.edu/documents/remarks-apology-african-americans-the-tuskegee-experiment>
- **COINTELPRO:** Senado dos EUA, Comissão Church, livro III (1976), p. 3 e p. 82: <https://www.intelligence.senate.gov/sites/default/files/94755_III.pdf>
  - 1956 a 1971, "more than 2,000 approved COINTELPRO actions";
  - arrombamento de Media em 8/3/1971, documentos publicados;
  - gravação e bilhete a Martin Luther King, "interpreted as a threat to release the tape recording unless Dr. King committed suicide".
- **Área 51 e U-2:** National Security Archive, "Area 51, Secret Aircraft and Soviet MiGs" (2013), sobre a história do U-2 liberada pela CIA no verão de 2013: <https://nsarchive2.gwu.edu/NSAEBB/NSAEBB443/>
- **OVNIs e voos espiões:** Gerald K. Haines, "CIA's Role in the Study of UFOs, 1947-90" (CIA, 1997), p. 73: "over half of all UFO reports from the late 1950s through the 1960s were accounted for by manned reconnaissance flights": <https://archive.org/details/DTIC_ADA525986>
- **Roswell:** Força Aérea dos EUA, "The Roswell Report: Fact versus Fiction in the New Mexico Desert" (relatório de julho de 1994), prefácio: "Project MOGUL, the top-priority classified project of balloon-borne experiments, which provides the explanation for the 'Roswell Incident'": <https://archive.org/details/DTIC_ADA326148>
- **Stargate:** American Institutes for Research, avaliação para a CIA (1995): "In no case had the information provided ever been used to guide intelligence operations" e "continued use of remote viewing in intelligence gathering operations is not warranted": <https://archive.org/details/CIA-RDP96-00791R000200180006-4>; sessões sobre os reféns no Irã (títulos dos documentos da CIA, por exemplo "IRAN HOSTAGE SITUATION GRILL FLAME REMOTE VIEWING SESSION").
- **Lua:** NASA, imagens da sonda LRO (PIA12889 e PIA12920, "Apollo 17 Lunar Module Challenger descent stage").
- **Terra:** NASA, iss066e152099 (horizonte visto da ISS, 2022) e a Terra vista da órbita da Lua pela LRO.

## A conferir antes de publicar

- "Desde 2009" (a LRO foi lançada em 2009; a página da NASA não foi aberta daqui): conferir ou dizer "há mais de quinze anos".
- O U-2 derrubado em "maio de 1960" e o nome de Powers vêm dos títulos dos cinejornais da Universal (12 e 16/05/1960); a data exata (1º de maio) não está no roteiro.

## Imagens (todas reais, sem IA; o esquema do iceberg é desenhado pelo canal)

| Código | Material | Origem e direitos |
|---|---|---|
| FBI | "Focus on the FBI", c. 1959-1970 | Arquivo Nacional, domínio público (CC0 no acervo); <https://archive.org/details/gov.archives.arc.12103> |
| SC, PW | Cinejornais Universal sobre o caso do U-2, maio de 1960 | Universal Newsreels, domínio público; Internet Archive |
| mx25244, mx25245, mx8128, mx15233 | Icebergs e geleiras | Mixkit, licença gratuita |
| NASA | LRO, ISS, U-2 da NASA | NASA, domínio público |
| Reaproveitado | Filmes e documentos da MKUltra, Northwoods, Paperclip e Tonkin | ver os READMEs desses projetos |

## Entregas

| Versão | Arquivo | Data | Observação |
|---|---|---|---|
| v1 | `render/iceberg-v1.mp4` (envio: `-envio.mp4`, 720p) | 2026-11-23 | 10:44, -16 LUFS, pico -1,4 dB, voz Davi em duas partes. 161 planos. Conferido: a frase "O documento foi liberado em 1997…" está no áudio (a transcrição automática não a pegou; o tempo foi corrigido à mão na linha do tempo); o esquema do iceberg foi redesenhado para caber entre as faixas de cinema; a trilha passou a usar os nomes curtos dos capítulos. |
