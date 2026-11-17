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

## 2026-11-17: não mexer no timbre da voz da DarkPlanner

- O dono ouviu a voz "dobrada" de novo, mesmo sem o eco. No teste A/B/C, o original da DarkPlanner soou limpo, e as duas versões com de-esser e equalização soaram dobradas.
- A medição não acha cópia atrasada. O efeito vem do de-esser do ffmpeg, que muda cerca de 16% da energia o tempo todo, somado à equalização sobre uma voz sintética comprimida a 64 kbps.
- Regra: o `tratar_narracao.py` agora só faz `highpass=f=60`, as pausas e o volume. Não use eco, de-esser nem equalização na voz da DarkPlanner.
- Quando o dono reclamar do som e a medição não achar nada, mande trechos curtos A/B/C (original, atual e alternativa) e pergunte qual soa errado. Foi o que achou a causa aqui.

## 2026-11-17: limitador forte "dobra" a voz no vídeo

- Mesmo sem filtros na voz, o dono ouvia "duas vozes juntas" só no vídeo completo. Nos trechos de voz pura, não.
- **Causa provável:** a mixagem passava por um limitador a -6 dBFS (`alimiter=limit=0.5`), que agia em 27% da fala, cortando até 4,5 dB. Depois vinha outro limitador para chegar a -14 LUFS.
- **Agora:** sem limitador no meio da mixagem. No final há só um limitador suave em -1 dB, e o alvo de volume vem do plano (`ESTILO["lufs"]`). Para a voz da DarkPlanner, que já sai em -16 LUFS, use -16: quase nada é limitado.
- **Testes:** voz, música e efeitos isolados (vídeos de 45 s) soavam iguais, porque a música fica cerca de 28 dB abaixo da voz quando ela fala. A trilha não era a causa.
