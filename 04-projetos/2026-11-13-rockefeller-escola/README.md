# Perfeita docilidade: Rockefeller, a Prússia e a escola obrigatória

> Data: 2026-11-13 · Tipo: projeto · Status: em produção

**Resumo:** documentário de cerca de 14 minutos sobre a teoria de que a escola obrigatória foi desenhada por Rockefeller. O vídeo mostra os documentos originais com o trecho citado em destaque e separa o que eles sustentam do que é mito.

## Critério de pronto

- Formato e duração: 16:9, 1920×1080, 24 fps, cerca de 14 min.
- Onde publica: YouTube.
- Motor: `motor/montar.py` (planos de documento com marca-texto em `motor/doc.py`, filmes de arquivo tratados com ffmpeg).
- Pronto quando: o dono revisar o roteiro, gerar a narração com a voz dele e o vídeo for remontado sobre ela.

## Checklist

- [x] 1. Ideia e critério de pronto
- [x] 2. Roteiro (escrito pela IA a pedido do dono; falta a revisão dele)
- [x] 3. Narração: voz M5 do Supertonic-3 (motor do VoiceStudio, licença OpenRAIL-M), escolhida pela IA a pedido do dono (`audio/narrar_m5.py`)
- [ ] 4. Aprovação do áudio
- [x] 5. Referências e assets
- [x] 6. Identidade visual
- [x] 7. Trilha e sound design
- [x] 8. Montagem (sobre a voz provisória)
- [ ] 9. Revisão e entrega
- [ ] 10. Aprendizados registrados

## Voz

- Motor: Supertonic-3 (Supertone), instalado em `/home/user/supertonic` (fora do git). Pesos do modelo em licença OpenRAIL-M, que permite uso comercial com restrições de uso indevido.
- Voz: M5, a mais grave das 5 masculinas (tom médio ~92 Hz) e uma das que leram os anos corretamente nos testes.
- Números são escritos por extenso antes da síntese (`audio/preparar_supertonic.py`).
- Conferência: 97,5% das palavras transcritas iguais ao roteiro. Pronúncias a ouvir: "Horace Mann", "inspetor", "dóceis".

## Fontes

Documentos (Internet Archive, todos anteriores a 1929):

- F. T. Gates, *The Country School of To-Morrow*, General Education Board, Occasional Papers No. 1, 1913 (`countryschooloft00gates`). A citação "In our dream…" está na p. 6 e foi conferida no original.
- *The General Education Board: An Account of Its Activities, 1902–1914*, 1915 (`generaleducation00geneiala`): doações de 1902, 1905 e 1907 (pp. 15–16), retrato de Rockefeller, mapas e fotos de escolas.
- Horace Mann, *Report of an Educational Tour in Germany…*, 1846 (`reportofeducatio00mannuoft`): elogio à Prússia e descrição da intimação aos pais.
- *Life of Horace Mann*, 1865 (`lifeofhoracemann00mann`): retrato.
- A. Flexner, *Medical Education in the United States and Canada*, 1910 (`medicaleducation00flexiala`): folha de rosto.

Filmes (Internet Archive, licença marcada como domínio público): `HERE_IS_GERMANY`, `AndSoTheyLive`, `Children1940`, `SchoolRules`, `HowQuiet1953`, `HowTexti1948`, `What_Happened_1901`, `loc-film-00694373-bargain-day-14th-street-new-york`, `new-york-subway-1905-directed-by-g.-w.-bitzer`, `nyc_ghetto_fish_market_1903`, `Tubercul1955`, `atom_and_biological_science`, `bacteria_friend_and_foe`. São ilustrativos.

Filmes acrescentados na v8 (troca de imagens), todos de domínio público. Os do Prelinger estão marcados assim, e os de 1911 e 1918 são anteriores a 1929:

- `1911ATripThroughNewYorkCity…` (Nova York, 1911);
- `SteelASy1936`;
- `OilforAl1949`;
- `my-four-years-in-germany-1918` (filme de 1918, usado só em planos sem cartela);
- `People Who Live Through Industry` (1928, Alemanha);
- `CityTheP1939`;
- `6381_HM_High_School_1930s`;
- `Brazilat1943`, `BeloHori1949` e `BrazilGe1942` (filmes do governo americano sobre o Brasil).

Fotos: Lewis Hine, National Child Labor Committee (1908 e 1912), domínio público, via Wikimedia Commons. O filme `1903ScenesInNewYorkCity` foi descartado porque tem marca d'água (FRAMEPOOL). Detalhes em `03-referencias/analises/2026-11-14-filmes-de-arquivo-v8.md`.

## A conferir antes de publicar

Conferido em 2026-11-14, com fontes, em `03-referencias/analises/2026-11-14-conferencia-de-fatos-perfeita-docilidade.md`. As 4 correções foram aplicadas na v10, cortando o áudio da narração sem regravar. Os itens eram:

1. "escolas que ensinavam latim a filhos de lavradores" (não está no folheto de Gates);
2. "nenhum governo estadual conseguia igualar" (sem fonte);
3. "quem mais resistia à lei não eram as famílias com medo de doutrinação" (forte demais, por causa da Lei Bennett, de 1889);
4. o acordo com a Faculdade de Medicina de São Paulo ("novo prédio", "professores estrangeiros", "poucos alunos" sem fonte).

Os demais pontos foram confirmados. Falta ainda: o dono ler o roteiro e conferir a Constituição de 1934 no texto do Planalto e o artigo de Gatto no arquivo do jornal.

## Entregas

| Versão | Arquivo | Data | Observação |
|---|---|---|---|
| v1 | `render/perfeita-docilidade-v1.mp4` | 2026-11-13 | 14 min 2 s, 210 planos (70 de documento com marca-texto, 140 de filme de arquivo), voz provisória `pt_BR-cadu` |
| v2 | `render/perfeita-docilidade-v2.mp4` | 2026-11-13 | Estilo da referência 04: cor saturada e duotone, vermelho monocromático, 258 planos (média 3,3 s), 14 frases entre aspas, legenda amarela; voz provisória |
| v3 | `render/perfeita-docilidade-v3.mp4` | 2026-11-13 | Igual à v2, com datas e nomes em texto grande no alto, sem faixa (pedido do dono) |
| v5 | `render/perfeita-docilidade-v5-editonny.mp4` | 2026-11-14 | Análise e verificação com o editonny: pausas de 0,8–1,5 s encurtadas para 0,5 s (14:40 → 14:06), 9 planos sem fade preto, sem fade de entrada, áudio -14,0 LUFS / pico -2,1 dBTP / 48 kHz. Verificação do editonny: volume passou; "intervalos silenciosos" (pausas da narração) e "texto na borda" (páginas dos documentos em close) são exceções intencionais |
| v6 | `render/perfeita-docilidade-v6-cenas.mp4` | 2026-11-14 | Cenas do editonny sobre a v5, sem som novo: ano 1913 em placar na abertura; contador das doações (1902, 1905, 1907) com total acumulado; frase "nação de trabalhadores" riscada como SEM FONTE; painel "Confirmado × Não comprovado" sincronizado com a narração; linhas de TV nos filmes de Nova York (1901–1905); chamada para comentar no fim; queima de filme em cada troca de capítulo. Refazer: `CENAS_EDITONNY=1 python3 motor/montar.py render <planos>` e `python3 motor/cenas_v6.py` |
| v7 | `render/perfeita-docilidade-v7-sem-capitulos.mp4` | 2026-11-14 | Igual à v6, com os cartões de capítulo refeitos como cena animada (`capitulo` em `motor/cenas_doc.py`): "CAPÍTULO N" em máquina de escrever, título letra a letra, traço vermelho, filme rodando atrás e queima de filme na entrada; o cartão termina no corte. Refazer: `CENAS_EDITONNY=1 SEM_CAPITULOS=1` no `montar.py` e no `cenas_v6.py` |
| v8 | `render/perfeita-docilidade-v8-imagens-novas.mp4` | 2026-11-14 | Mesma narração e cenas da v7, com imagens trocadas: 11 filmes novos de arquivo (Nova York em 1911, siderurgia, petróleo, Alemanha imperial, The City de 1939, escola dos anos 1930, Brasil dos anos 1940) e fotos de Lewis Hine no capítulo das fábricas. Refazer: `NOVAS_IMAGENS=1 CENAS_EDITONNY=1 SEM_CAPITULOS=1` no `montar.py render` e no `cenas_v6.py` |
| v9 | `render/perfeita-docilidade-v9-voz-nova.mp4` | 2026-11-14 | Narração nova da DarkPlanner (áudio `darkplanner_audio_c9b03501`, 9:44) no lugar da voz sintética: 9:57, com as imagens e cenas da v8 refeitas no tempo da voz. `audio/alinhar_dp.py` alinha o roteiro ao áudio (98,5% das palavras casadas), tira o chiado e mantém o ritmo natural da voz (pausa média de 0,2 s entre frases); só entram pausas de 1,9 s entre capítulos e 6 s no título. `audio/final_14lufs.py` leva o volume a -14 LUFS. A abertura não tem o painel de gráfico do editonny: o "1913" é título simples (`SEM_GRAFICO=1`). Refazer: `NOVO=1 NOVAS_IMAGENS=1 CENAS_EDITONNY=1 SEM_CAPITULOS=1 SEM_GRAFICO=1` no `montar.py render`, `mixar.py`, `final_14lufs.py` e `cenas_v6.py`. Atenção ao espaço: apague `/tmp/hyperframes-extract-cache-0` entre os lotes de cenas e confira a duração do vídeo base antes de renderizar as cenas |
| v10 | `render/perfeita-docilidade-v10-corrigido.mp4` | 2026-11-14 | Igual à v9, com as correções da conferência de fatos feitas por corte no áudio da narração, sem regravar: saíram o latim, a frase dos valores "que nenhum governo estadual conseguia igualar", "não eram as famílias com medo de doutrinação", "poucos alunos" e "e a consertar". Duração 9:46, -14 LUFS. Refazer: `bash motor/cadeia_v10.sh`, que roda o vídeo base com conferência de duração, a mixagem, o volume final e as cenas em lotes com limpeza de cache. O arquivo sai como `v9-voz-nova` e foi renomeado para v10 |
