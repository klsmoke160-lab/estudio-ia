# Cenas do editonny no documentário "Perfeita docilidade"

> Data: 2026-11-14 · Projeto: 04-projetos/2026-11-13-rockefeller-escola

- **Pedido:** melhorar as imagens da v5 com o editonny. O dono aprovou com "a": queima de filme nas trocas de capítulo e todas as cenas propostas, sem som novo.
- **Feito:**
  - os títulos que viraram cena saem da base com `CENAS_EDITONNY=1` no `montar.py`, e só esses planos foram re-renderizados;
  - `motor/cena_editonny.py` renderiza cada janela num projeto editonny próprio;
  - `motor/cenas_v6.py` lista as 26 janelas e sobrepõe tudo na base, usando o áudio da v5.
- **Aprendizados:**
  - Cenas de tela cheia feitas para vertical (revenue-counter, comparison) não servem em 16:9: o número sai da tela e o visual neon destoa. Fiz o contador e o painel como cenas próprias (`motor/cenas_doc.py`), no formato de cena do editonny.
  - Os cartões crossed-out-quote e comment-call-to-action são cortados em x = 1080. Para corrigir, troque `data-width="1080" data-height="1920"` por 1920×1080 na cópia da cena.
  - `--transition` e `--effect` não registram a cena: o editonny só imprime a linha, e é preciso acrescentá-la em `project.json` → `scenes`.
  - A transição exige `--cuts`, e o vídeo do edit precisa de faixa de áudio (silêncio serve).
- **Verificação:** quadros de cada cena conferidos; volume e quadros pretos medidos no arquivo final.
