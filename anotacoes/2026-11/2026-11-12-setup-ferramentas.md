# Setup das ferramentas num contêiner Linux

> Data: 2026-11-12 · Projeto: estudio-ia

- **Pedido:** instalar e configurar o estúdio (roteiro 2).
- **Feito:** `uv sync` (modo leve), skills externas (HyperFrames, Remotion, transitions-dev, watch, humanizer), ligação `.claude/skills`, 56 efeitos sonoros gerados (ficam fora do git), `02-ferramentas/inventario.md` atualizado.
- **Decisões:** o instalador de Mac/Windows não se aplica; os passos foram feitos à mão.
- **Verificação:** `uv run setup/conferir.py` deu "Essencial pronto". O inventário reflete o contêiner, não o computador do dono.
- **Próximo:** IA de áudio (`uv sync --extra cpu`, torch falhou por bloqueio de rede), EffectCraft (só Mac/Windows), roteiro 1 (perfil) e roteiro 3 (referências), que dependem do dono.
