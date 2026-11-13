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

## A conferir antes de publicar

Estes pontos do roteiro vieram da memória da IA, sem documento conferido nesta sessão: regulamento prussiano de 1763; viagem de Mann em 1843; lei de Massachusetts de 1852 e Mississippi em 1918; uma em cada seis crianças trabalhando em 1900; Flexner no conselho; Fundação Rockefeller no Brasil a partir de 1916 e o acordo com a Faculdade de Medicina de São Paulo; frequência obrigatória na Constituição de 1934; biografia de John Taylor Gatto; ausência de fonte para a frase "nação de trabalhadores".

## Entregas

| Versão | Arquivo | Data | Observação |
|---|---|---|---|
| v1 | `render/perfeita-docilidade-v1.mp4` | 2026-11-13 | 14 min 2 s, 210 planos (70 de documento com marca-texto, 140 de filme de arquivo), voz provisória `pt_BR-cadu` |
| v2 | `render/perfeita-docilidade-v2.mp4` | 2026-11-13 | Estilo da referência 04: cor saturada e duotone, vermelho monocromático, 258 planos (média 3,3 s), 14 frases entre aspas, legenda amarela; voz provisória |
| v3 | `render/perfeita-docilidade-v3.mp4` | 2026-11-13 | Igual à v2, com datas e nomes em texto grande no alto, sem faixa (pedido do dono) |
