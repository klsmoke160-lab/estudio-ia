# Pesquisa de imagens para documentário

> Data: 2026-11-16 · Tipo: método · Status: vigente

**Resumo:** regra do dono, valendo desde 16/11/2026, para achar imagens de documentário no Rasura. Para cada trecho da narração, procure pelo menos três opções específicas em acervos especializados e confira se cada arquivo pode ser usado em vídeo monetizado. Escolha uma e explique por que ela combina com a fala.

## A regra

1. **Para cada trecho da narração, ache três opções, quando existirem.** Dê o link do arquivo ou da página do clipe, nunca só a página inicial do site.
2. **Escolha uma e diga por quê.** A justificativa liga a imagem à frase dita e diz o que ela acrescenta.
3. **Pesquise em português e em inglês.** Os nomes próprios (pessoas, prédios, operações) rendem mais que palavras genéricas.
4. **Confira o direito de uso de cada arquivo**, um por um. O que está na internet não é livre por estar lá. Escreva a licença ao lado do link.
5. **Não use:**
   - filme antigo sem relação com o fato (o "filme de arquivo aleatório");
   - imagem genérica de banco quando existe registro real do fato;
   - imagem gerada por IA;
   - imagem de vítima ou de corpo;
   - dramatização com atores apresentada como registro real.
6. **Ordem de preferência:**
   1. registro real do fato (filme, foto ou documento da época);
   2. o lugar real, mesmo filmado hoje;
   3. objeto ou ambiente que a frase cita, em filmagem de banco cinematográfica;
   4. gráfico ou animação feitos por nós.

## Onde procurar

| Para quê | Acervos | Como o estúdio acessa |
|---|---|---|
| Cena cinematográfica atual (fogo, papel, janela, lago, objeto) | Pexels Videos, Mixkit, Pixabay Videos | O Mixkit vai direto pelo `scripts/video/buscar_acervos.py`. O Pexels e o Pixabay bloqueiam acesso automático daqui: busque na web com `site:pexels.com` e confira a página do clipe |
| Filmagem histórica e registro real | Internet Archive (coleções `FedFlix`, `prelinger`, `universal_newsreels`), Wikimedia Commons, National Archives (NARA), Library of Congress | Internet Archive e Wikimedia pelo script. Muitos filmes do NARA estão copiados no Internet Archive como `gov.archives.arc.*`, `111-lc-*` (Exército) e `428-npc-*` (Marinha). A Library of Congress bloqueia acesso automático daqui |
| Documento e investigação | CIA Reading Room (`cia.gov/readingroom`), FBI Vault, Senado e Congresso dos EUA | Busca na web com `site:cia.gov/readingroom`. O FBI Vault bloqueia acesso automático daqui |
| Foto oficial de pessoa pública dos EUA | Wikimedia Commons (retratos da CIA, Marinha, Casa Branca), bibliotecas presidenciais (ex.: Ford Library) | Script, depois a página do arquivo |
| Reportagem profissional | AP Archive, British Pathé, Getty | Só com licença paga. Nunca baixar e usar sem comprar |

## Direitos: o que costuma valer

| Origem | Monetizar? | Cuidado |
|---|---|---|
| Obra do governo federal dos EUA (CIA, Exército, Marinha, Casa Branca, NARA, Senado) | Sim, domínio público | Os acervos do governo **guardam também obras de terceiros**. A coleção de filmes da CIA no NARA (grupo 263) tem programas da NBC, da March of Time, de laboratórios e de governos estrangeiros. Leia quem produziu, não só a etiqueta "CC0" da digitalização |
| Prelinger (Internet Archive) com licença "publicdomain" | Sim | Os filmes caseiros (`prelingerhomemovies`) muitas vezes vêm sem licença declarada: confira antes |
| Wikimedia "Public domain" ou "CC0" | Sim | Leia o autor. "Autor desconhecido" numa foto de família de 1953 não prova domínio público |
| Wikimedia ou Internet Archive "CC BY" / "CC BY-SA" | Sim, com crédito | Crédito na descrição do vídeo (autor, licença, link) |
| Pexels License / Pixabay Content License | Sim, sem crédito obrigatório | Pessoa identificável não pode aparecer de forma ofensiva ou como se fizesse algo que não fez. Num documentário de crime, prefira mãos, objetos e ambientes, sem rosto |
| Mixkit Stock Video Free License | Sim | Não revender o clipe solto. Mesmo cuidado com rostos |
| Universal Newsreels | Sim, domínio público nos EUA | Confira o nome: "Dulles" nos cinejornais costuma ser **John Foster Dulles** (secretário de Estado), não Allen Dulles (diretor da CIA) |
| Emissoras de TV (CBC, ABC, CBS, NBC) e cópias de TV no Internet Archive (`tvarchive`) | Não | Mesmo dentro de acervo público |

**Content ID:** distribuidoras de banco às vezes reivindicam filmes de domínio público no YouTube. Guarde o link do acervo e a licença de cada clipe no `README` do projeto; é a prova para contestar.

## Como rodar a busca

```bash
python3 scripts/video/buscar_acervos.py consultas.json resultados.json
```

O `consultas.json` lista os trechos com as buscas de cada acervo (`ia`, `wm`, `mix`). O resultado traz título, link e licença de cada achado. Depois:

1. filtre pela licença;
2. veja os quadros de cada filme candidato numa folha de 8 quadros (o ffmpeg precisa de `http_proxy=$HTTPS_PROXY` para ler direto do acervo);
3. escreva o plano visual do projeto, com o trecho, o tempo na narração, as três opções, a escolha e o motivo.

Exemplo completo: `04-projetos/2026-11-15-mkultra/pesquisa/plano-visual.md`.
