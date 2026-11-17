# Aprendizados

> Data: 2026-10-22 · Tipo: dados · Status: vigente

**Como usar:** uma entrada por aprendizado, a mais nova no topo: data, projeto, o que aconteceu e o que fazer da próxima vez. Quando o aprendizado vira um número fixo, ele sobe para [regras.md](regras.md) e aqui fica só o link.

<!-- Modelo:
## AAAA-MM-DD — título curto
- **Projeto:** 04-projetos/AAAA-MM-DD-tema
- **O que aconteceu:**
- **Da próxima vez:**
-->

## 2026-11-17: fundo sintético soa como zumbido

- O "fundo" do `doc_motor.py` (dois senos graves de 55 e 82,5 Hz mais ruído marrom) soa como um ronco contínuo no fone. O dono reclamou de "som de fundo ruim".
- Agora o plano aceita `ESTILO["trilha"]=[(arquivo, capítulo onde começa, ganho em dB), ...]`, com música de verdade. Cada faixa entra no seu capítulo, a passagem entre elas dura 3 s, e a música abaixa sozinha sob a voz (`sidechaincompress`).
- **Nível bom:** música nas pausas cerca de 17 dB abaixo da voz. Para uma faixa de -15 LUFS, o ganho fica perto de -15 a -19 dB.
- **Músicas:** `05-biblioteca/musica/mixkit/` (licença Mixkit, livre para vídeo monetizado).
