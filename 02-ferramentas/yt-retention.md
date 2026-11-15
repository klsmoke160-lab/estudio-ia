# yt-retention (leitor do gráfico de retenção do YouTube)

> Data: 2026-11-15 · Tipo: guia · Status: vigente

**Resumo:** lê o arquivo "Audience retention" do YouTube Studio e diz onde as pessoas saem do vídeo: vazamento no gancho, quedas bruscas e escorregamento do meio. Serve para decidir o que mudar no próximo vídeo do Rasura.

- **Como acessar:** skill em `.agents/skills/yt-retention/` (a pasta `.claude/skills` aponta para ela) e script Python `retention.py`. Roda em qualquer Python 3, sem instalar nada.
- **Instalação:** copiada sem alteração de `Jakeschincariol/youtube-agent-skill` (MIT). Origem, commit e revisão em `.agents/skills/yt-retention/ORIGEM.md`. Foi instalada só esta skill das 11 do pacote.
- **Credenciais:** nenhuma. Não acessa a internet nem a conta do YouTube; só lê o arquivo que você baixa.
- **Comandos mais usados:**
  - `python3 .agents/skills/yt-retention/retention.py retention.csv --duration 587`
  - Como obter o arquivo: Studio, o vídeo, Análises, Engajamento, o gráfico de retenção, ícone de download, "Audience retention". Ou mande um print do gráfico, que eu leio.
- **Pegadinhas:**
  - Com poucas visualizações (o primeiro vídeo tinha 16), a curva não diz nada: um espectador que sai muda tudo. Vale a partir de algumas centenas.
  - A opção `--transcript` precisa do `deadair.py` da skill `yt-edit`, que não está instalada, e falha. Cruzar os tempos com a transcrição do Whisper à mão.
  - O limite de "gancho saudável" (perda abaixo de 25% nos primeiros 30 s) é regra do autor, não do YouTube.
  - Testada só com um arquivo inventado, para ver se roda.
- **Log:** 2026-11-15, instalada e testada com dados fictícios.
