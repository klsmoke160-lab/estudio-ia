# Pesquisa de imagens em acervos para o MKUltra

> Data: 2026-11-16 · Projeto: 04-projetos/2026-11-15-mkultra

- **Pedido:**
  - estilo Mystère como referência principal (o vídeo não chegou; o dono precisa mandar o arquivo ou o link);
  - regra permanente: pesquisar imagens em acervos especializados, com três opções por trecho, links específicos e conferência de direitos para monetizar.
- **Feito:**
  - regra registrada em `06-metodo/pesquisa-de-imagens.md`;
  - buscador `scripts/video/buscar_acervos.py` (Internet Archive, Wikimedia e Mixkit, com licença);
  - folhas de quadros dos filmes candidatos;
  - plano visual do MKUltra em `04-projetos/2026-11-15-mkultra/pesquisa/plano-visual.md`.
- **Achados:**
  - a coleção de filmes da CIA no NARA (grupo 263, copiada no Internet Archive como `gov.archives.arc.*`) tem testes reais de LSD de 1955 e a posse de Helms;
  - a Marinha e o Exército têm os prisioneiros da Coreia de 1953 (`428-npc-*`, `111-lc-*`), um deles escaneado em 1920×1080.
- **Aprendizados:**
  - O ffmpeg não passa pelo proxy sozinho: use `http_proxy=$HTTPS_PROXY` para tirar quadros direto do acervo.
  - Pexels, Pixabay, Library of Congress, FBI Vault e a API do NARA bloqueiam acesso automático daqui. A busca na web com o domínio resolve o Pexels e o Pixabay.
  - O Wikimedia exige User-Agent e limita pedidos em sequência (429): espaçar os pedidos.
  - A etiqueta CC0 da digitalização do NARA não cobre obra de terceiros guardada pelo governo. Ex.: "Mission Mind Control" é da ABC, "Science of Spying" é da NBC.
  - "Dulles" nos cinejornais Universal é John Foster, não Allen.
- **Próximo:** o dono aprova o plano e manda o vídeo do Mystère. Depois: conferir o produtor dos filmes de LSD, baixar o material e montar a v2.

## Continuação: v2 montada

- **Feito:**
  - baixados 10 filmes do acervo e 25 clipes de banco;
  - o plano da v2 foi para `motor/plano.py` (o da v1 ficou em `plano_v1.py`);
  - render conferido em `render/mkultra-v2.mp4`: -14,1 LUFS, 13:09, trechos pretos só nos cartões.
- **Motor (`doc_motor.py`):**
  - respeita o formato de cada fonte (`AR` e `PRE` no plano: 4:3, 16:9 e cinemascope com faixas embutidas);
  - deixa margem no recorte;
  - o aviso de abertura agora é configurável (`AVISO`).
- **Aprendizados:**
  - Clipe 16:9 com zoom de afastamento chegava ao último quadro 2 px menor que a tela, e o recorte travava o ffmpeg ("corrupted double-linked list"). A correção foi a margem de 0,4% no tamanho.
  - Clipe de banco em fundo preto (gota no copo) vira tela preta depois do tingimento escuro. Confira o brilho médio antes de usar e prefira fundo claro (gota com ondas, tinta na água).
  - O Mixkit baixa em 720p com o Referer do site. O Pexels baixa pela página `/download/video/<id>/` e às vezes manda 4K, que deve ser reduzido para 1080p.
  - O Wikimedia (upload) devolveu 429 por mais de 30 minutos. Não contornar: deixe um clipe reserva no plano (`P_`).
