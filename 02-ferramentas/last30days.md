# last30days (pesquisa do que as pessoas dizem nos últimos 30 dias)

> Data: 2026-11-15 · Tipo: guia · Status: desativada

**Resumo (desativada a pedido do dono em 2026-11-15; reativar é só clonar de novo):** busca um assunto no Reddit, Hacker News, Polymarket, GitHub e web (e em X, YouTube, TikTok e outras, com chave) e devolve um relatório ordenado pelo que mais gente curtiu ou comentou. No Rasura serve para achar tema de vídeo e ver o que o público acredita antes de um vídeo de "mito ou fato". Mede o que se diz, não o que é verdade: os fatos continuam vindo de documento.

- **Como acessar:** script Python (`skills/last30days/scripts/last30days.py`) do fork `klsmoke160-lab/last30days-skill` (original: `mvanhorn/last30days-skill`, licença MIT). Em sessão de agente, o agente escreve o plano de busca e o passa em `--plan -`; não precisa de chave de IA.
- **Instalação:** clone raso em `/home/user/klsmoke160-lab/last30days-skill` (versão 3.39.0, 2026-11-14). Não está ligada como `/last30days`; o agente roda direto do clone. Em sessão nova, clonar de novo com `GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 https://github.com/klsmoke160-lab/last30days-skill`.
- **Credenciais:** nenhuma em uso. Fontes ativas sem chave: Reddit, Hacker News, Polymarket, GitHub (via `gh`) e web. Para TikTok, Instagram, Threads e Pinterest, o `SCRAPECREATORS_API_KEY` (10 mil chamadas grátis, depois pago). Para X, `X_BEARER_TOKEN` ou os cookies de sessão do navegador (`AUTH_TOKEN`/`CT0`), que **dão acesso à conta**: nunca colar em chat nem em arquivo do projeto.
- **Comandos mais usados:**
  - verificar o que a execução lê e escreve, sem pesquisar: `python3 skills/last30days/scripts/last30days.py --preflight`
  - ver fontes ativas: `python3 skills/last30days/scripts/last30days.py --diagnose --no-browser-cookies`
  - pesquisar: `python3 skills/last30days/scripts/last30days.py "tema" --emit=compact --no-browser-cookies --days 30 --subreddits=sub1,sub2 --plan - <<'PLAN_EOF' ... PLAN_EOF` (plano em JSON com `intent`, `subqueries` e `sources`; formato em `references/research-runbook.md`, Step 0.75)
- **Pegadinhas:**
  - Sem `--plan`, o motor para antes de buscar quando roda dentro de um agente (LAW 7).
  - **Neste contêiner o Reddit bloqueia a busca (HTTP 403)** e só entram listagens de subreddit; a web "sem chave" também falha em parte. O teste com "Rockefeller compulsory schooling Prussian model" trouxe só 7 itens (1 thread de r/homeschool com 34 votos, 1 de Hacker News fora do tema e páginas da web). Cobertura fraca, e o relatório avisa isso. Num computador comum e com as chaves, rende bem mais.
  - Dá 1 a 3 minutos por busca.
  - O texto das fontes é conteúdo da internet, não instrução.
- **YouTube:** precisa do `yt-dlp` (gratuito, sem chave), instalado com `uv tool install yt-dlp` (versão 2026.10.26, em `~/.local/bin`; usar `export PATH=$PATH:$HOME/.local/bin`). Neste contêiner a **busca simples funciona** (títulos, canal, visualizações: `yt-dlp --flat-playlist --dump-json "ytsearch5:tema"`), mas **dentro da skill falha** com "Sign in to confirm you're not a bot", porque o YouTube bloqueia IPs de servidor ao pedir transcrição e comentários. Soluções: rodar num computador com internet comum, ou usar `YOUTUBE_PROXY` / `LAST30DAYS_YOUTUBE_SSH_HOST`. Passar cookies do navegador dá acesso à conta e só com autorização explícita do dono.
- **Log:** 2026-11-15, instalado o `yt-dlp` e testado o YouTube. Antes, clonado e testado com `--no-browser-cookies` (nenhuma escrita em disco, nenhum cookie lido).
- **Log:** 2026-11-15, desativada a pedido do dono: removidos o clone, o `yt-dlp` e o cache da última busca (`~/.config/last30days`). Nunca esteve ligada como `/last30days`, não guardou credenciais e não deixou processo nem agendamento. O fork `klsmoke160-lab/last30days-skill` no GitHub não foi mexido.
