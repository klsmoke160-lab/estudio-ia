# Voz e narração

> Data: 2026-10-22 · Tipo: guia · Status: em teste

**Resumo:** a narração sai da sua voz gravada ou de uma voz clonada numa ferramenta de voz (ex.: ElevenLabs). O estúdio não instala nenhuma por padrão; quando você escolher uma, a IA atualiza este doc.

- **Gravar a própria voz:** celular a um palmo da boca, cômodo com cortina ou roupa, sem ventilador. Mande o arquivo para `04-projetos/<projeto>/audio/`.
- **Voz clonada:** crie a voz na ferramenta escolhida e guarde a chave no gerenciador de senhas ou na configuração da CLI dela, nunca nesta pasta.
- **Pronúncia:** escreva como se fala ("IÁ" para "IA") e confira com a transcrição (`uv run scripts/video/make_captions.py`).
- **Voz final:** seca, sem reverb nem eco; o volume é acertado na mixagem (`06-metodo/regras.md`).
- **Log:**

- 2026-11-21: ElevenLabs ligado como conector no Claude Code (sem chave em arquivo). Voz de teste: **Lucas - Deep & Profound Narrator** (`GIuLCSVfgJaUuh7hYOY8`, português do Brasil, grave, documentário), modelo `eleven_v4`. Short do MKUltra: 221 palavras em 96 s (138 palavras por minuto, 128 kbps). Aguardando aprovação do dono antes de virar a voz do canal.
- 2026-11-21: **Pronúncia de siglas na voz Lucas:** escreva "CIA" como **"Sía"** no texto que vai para o ElevenLabs (o dono aprovou depois de ouvir três opções). "Cê-I-Á" saiu errado. A legenda e as etiquetas continuam com "CIA". Teste toda sigla nova com uma frase curta antes de gerar o texto inteiro.
