# Golfo de Tonkin: a batalha que não aconteceu

> Data: 2026-11-22 · Tipo: projeto · Status: tudo pronto para montar; aguardando a narração (voz Davi do ElevenLabs bloqueada pelo limite do plano gratuito)

**Resumo:** documentário longo do Rasura (cerca de 10 min, 1.362 palavras, 12 capítulos) sobre o incidente do Golfo de Tonkin, em agosto de 1964. O ataque de 2 de agosto aconteceu; o de 4 de agosto, segundo um estudo interno da própria NSA liberado em 2005, não. Mesmo assim, ele serviu de base para a resolução que abriu caminho para a Guerra do Vietnã. Tema escolhido pelo Claude a pedido do dono ("você escolhe o tema, com a voz 3").

## Critério de pronto

- 16:9, 1920×1080, formato de cinema, motor `scripts/video/doc_motor.py`, uma cor por capítulo, trilha do Mixkit, -16 LUFS.
- Pronto quando: a narração chegar (voz Davi, `ZxeM4498ujGNHYhQXtLS`, com licença comercial), for tratada por `scripts/som/tratar_narracao.py`, e o vídeo for montado e conferido.

## Como montar quando a narração chegar

```bash
cd /home/user/estudio-ia
uv run python scripts/som/tratar_narracao.py 04-projetos/2026-11-22-golfo-de-tonkin <audio.mp3> --linha 0 --curta 0.9
python3 scripts/video/doc_motor.py 04-projetos/2026-11-22-golfo-de-tonkin edl
python3 scripts/video/doc_motor.py 04-projetos/2026-11-22-golfo-de-tonkin render
python3 scripts/video/doc_motor.py 04-projetos/2026-11-22-golfo-de-tonkin juntar
python3 scripts/video/doc_motor.py 04-projetos/2026-11-22-golfo-de-tonkin som
python3 scripts/video/doc_motor.py 04-projetos/2026-11-22-golfo-de-tonkin final golfo-de-tonkin-v1.mp4
```

O plano já foi testado com uma linha do tempo simulada: 135 planos, todas as regras casam com uma frase, um plano de cada fonte foi renderizado e conferido.

## Gancho (regra em `06-metodo/ganchos.md`)

Três opções comparadas:
1. **Cena:** "Na noite de 4 de agosto de 1964, dois navios de guerra americanos passaram horas disparando contra um inimigo no escuro."
2. **Documento e contradição (escolhido):** "Naquela noite, não houve ataque nenhum." É a frase do estudo da NSA, a mesma que está marcada na capa.
3. **Consequência:** "O comandante no local pediu uma avaliação completa antes de qualquer reação. No mesmo dia, o presidente já tinha ordenado o bombardeio."

Escolhido o 2 porque a primeira frase e o primeiro quadro são a prova que a capa promete, e o vídeo inteiro investiga como ela foi escondida.

Direção da abertura:
- **0 s:** a página 3 do estudo da NSA, com o carimbo de ultrassecreto riscado no alto, já focada na linha "no attack happened that night". O quadro nasce rápido (0,4 s), com silêncio de 1,5 s antes da voz.
- **Na voz, "ataque nenhum":** o marca-texto amarelo entra sobre a linha.
- **"A frase está num estudo ultrassecreto":** corte para a página de título do estudo ("Skunks, Bogies…"); a trilha entra.
- **"E fala da noite de 4 de agosto":** o mapa do Golfo de Tonkin do filme de 1964 (coletiva de 5 de agosto), com o único texto na tela: "4 DE AGOSTO DE 1964".
- **"dois navios… no escuro":** tempestade no mar à noite e o destróier do cinejornal de 6/8/1964.
- **"o Congresso deu ao presidente o poder":** Johnson discursando (cinejornal) e a página da resolução.
- **As duas perguntas:** a capa das interceptações da NSA ("This document contains code word material").

## Arquivos

- `roteiro-completo.txt`: roteiro com os capítulos (`# NOME`), lido pelo motor.
- `texto-para-voz.txt`: o mesmo texto sem títulos, para colar no ElevenLabs (8.446 caracteres).
- `motor/gerar_docs.py`: gera as transcrições com marca-texto e acha, pelo OCR, as caixas dos trechos nas páginas escaneadas da NSA.
- `motor/plano.py`: fontes, documentos, regras por frase, palavras-chave, cartões, cores e trilha.
- `render/capa-final.jpg`: capa ("A BATALHA QUE NÃO ACONTECEU", Johnson e a página da NSA com "no attack happened that night" marcado).
- `publicacao-youtube.md`: título, descrição, fontes e tags (capítulos com tempo entram depois da narração).
- Material bruto em `/home/user/mk/tk/` (fora do git): `raw/` (filmes), `docs/` (páginas e transcrições), `cenas.json`, `sheets/` (folhas de contato).

## Fontes conferidas (22/11)

- **National Security Archive (Universidade George Washington), Electronic Briefing Book 132**, ensaio de John Prados (2004) e comunicado de 01/12/2005: <https://nsarchive2.gwu.edu/NSAEBB/NSAEBB132/>
  - a operação OPLAN 34-A atacou as ilhas Hon Me e Hon Ngu antes do combate de 2 de agosto; barcos, alvos e dinheiro americanos;
  - o combate de 2 de agosto foi de dia, com fotos e torpedos vistos; o de 4 de agosto não teve destroços, corpos nem fotos;
  - a frase de Stockdale (do livro *In Love and War*, 1984);
  - o resumo do telegrama de Herrick ("appear doubtful", "freak weather effects", "over-eager sonarmen", "complete evaluation") na cronologia de 28/08/1964;
  - McNamara, 3/8/1964 (telefonema gravado) e 6/8/1964 (sessão fechada);
  - McNamara em 1968 ("highly classified and unimpeachable source"), recusa de deixar cópias; relato de J. Norvill Jones;
  - 548 mil soldados em março de 1969; cerca de 59 mil americanos mortos;
  - a NSA liberou mais de 140 documentos em 01/12/2005, depois de um pedido de acesso de Matthew Aid; um jornalista (I. F. Stone) questionou a segunda batalha semanas depois.
- **Robert J. Hanyok, "Skunks, Bogies, Silent Hounds, and the Flying Fish: The Gulf of Tonkin Mystery, 2-4 August 1964"**, Cryptologic Quarterly (NSA, 2001), páginas originais liberadas (relea00012.pdf no mesmo endereço):
  - p. 3: "no attack happened that night"; "nearly 90 percent of all available SIGINT" ficou de fora;
  - p. 24: os sonares ouviam a turbulência das hélices dos próprios navios; Herrick, "ENTIRE ACTION LEAVES MANY DOUBTS EXCEPT FOR APPARENT ATTEMPTED AMBUSH AT BEGINNING"; menos de três horas depois, Johnson aprovou a represália; Goldwater; "not totally clear" por que tão rápido;
  - p. 49: "an active effort to make SIGINT fit the claim"; sem "smoking gun".
- **Arquivo Nacional dos EUA, Tonkin Gulf Resolution** (Public Law 88-408): texto, aprovação em 7/8/1964 com só dois senadores contra (Morse e Gruening), revogação em janeiro de 1971: <https://www.archives.gov/milestone-documents/tonkin-gulf-resolution>
- **Discurso de Johnson, 4/8/1964** (Miller Center): <https://millercenter.org/the-presidency/presidential-speeches/august-4-1964-report-gulf-tonkin-incident>
- **Interceptações da NSA** (Biblioteca LBJ, liberadas em 2003): `tonkin_intercepts.pdf`, no mesmo endereço do National Security Archive.

## A conferir

- "Na Câmara, ninguém votou contra" (416 a 0): o dado é amplamente citado, mas a página do Arquivo Nacional só fala dos dois senadores. Conferir no registro da Câmara antes de publicar, ou suavizar.
- A coletiva do filme TC (05/08/1964) não identifica quem fala; o roteiro não diz o nome.

## Imagens (todas reais, sem IA)

| Código | Filme | Origem e direitos |
|---|---|---|
| UN | Universal Newsreel, vol. 37, n. 63, 06/08/1964 | Arquivo Nacional dos EUA (Universal Newsreels, domínio público); <https://archive.org/details/yt_LQVycAoOR6w> |
| TC | "Press conferences on the Gulf of Tonkin incident", 05/08/1964 | Arquivo Nacional, RG 111 (Exército), domínio público; <https://archive.org/details/111-lc-48220> |
| WV | "Why Vietnam?", 1965 | Departamento de Defesa, domínio público (CC0 no acervo); <https://archive.org/details/gov.dod.dimoc.46000> |
| A4 | Convés de porta-aviões no Golfo de Tonkin, 1967 | Arquivo Nacional, RG 428 (Marinha), domínio público; <https://archive.org/details/428-npc-37781> |
| BP | "The Big Picture: Why Vietnam?" | Exército, domínio público (CC0 no acervo); baixado, ainda não usado |
| mx4059, mx4060, mx34154, mx10395 | Tempestade no mar, papel antigo, máquina de escrever | Mixkit, licença gratuita |

Documentos na tela: as páginas originais do estudo da NSA e das interceptações (governo dos EUA), a imagem da resolução (Arquivo Nacional) e transcrições com a fonte no rodapé para os textos que não têm página escaneada aqui.
