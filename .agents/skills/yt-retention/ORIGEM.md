# Origem de yt-retention

> Data: 2026-11-15 · Tipo: guia · Status: vigente

**Resumo:** skill copiada, sem alteração, do pacote `Jakeschincariol/youtube-agent-skill` (commit `a2feb21`, licença MIT, ver `LICENSE`). Foi instalada só esta, das 11 do pacote.

- **Para que serve:** lê o arquivo de retenção do YouTube Studio e mostra o vazamento no gancho, as quedas bruscas e o escorregamento do meio.
- **Revisado em 2026-11-15:** o código inteiro (90 linhas, só `csv`, `json`, `os`, `re` e `sys`; sem rede, sem outros programas, sem credenciais).
- **Limite:** a opção `--transcript` importa o `deadair.py` da skill `yt-edit`, que não foi instalada. Sem ele, essa opção falha. Para saber o que foi dito em cada queda, cruze os tempos com a transcrição do Whisper à mão.
- **Uso:** `python3 .agents/skills/yt-retention/retention.py retention.csv --duration 587`
