"""Plano do Short 'Parabéns, você criou o MKUltra': fontes reaproveitadas do plano da v3 (documentos originais e filmes de arquivo), tempos da narração do ElevenLabs."""
import importlib.util, pathlib
_s = importlib.util.spec_from_file_location("plano_v3", "/home/user/estudio-ia/04-projetos/2026-11-17-mkultra-v3/motor/plano.py"); PL = importlib.util.module_from_spec(_s); _s.loader.exec_module(PL)
# documentos novos, da mesma audiência do Senado (1977)
PL.doc("ecologia", 84, "The Society for the Investigation", "Human Ecology,")
PL.doc("cutout", 142, "The Bureau was serving as", "Agency participation.")
assert not [k for k in ("ecologia", "cutout") if k in PL.FALTAM], PL.FALTAM
AUDIO = "audio/narracao-final.mp3"; PALAVRAS = "audio/final.json"
CORRIGE = {"NKUltra": "MKUltra", "recebos": "recibos", "cutout": "cut-out", "cut -out": "cut-out"}
VERMELHO = {"lsd", "droga", "destruir", "janela", "escandalo", "derrubar", "secreto", "prisoes"}
VERDE = {"cut-out", "casas", "seguras", "mkultra", "contabilidade", "recibos"}
AVISO = "IMAGENS DE ARQUIVO ILUSTRATIVAS · DOCUMENTOS ORIGINAIS"
X, Dc = PL.X, PL.Dc; LW, LS, SF, GV, HE, NX, BW = PL.LW, PL.LS, PL.SF, PL.GV, PL.HE, PL.NX, PL.BW
ARQ, FICHAS, GAVETA, GOTA = PL.ARQ, PL.FICHAS, PL.GAVETA, PL.GOTA
# (início em segundos na narração, fontes em ordem, cor do filme)
BEATS = [
 (0.0,  Dc("aprovado") + LW(401) + LW(216), "petroleo"),          # você é a CIA em 1953
 (8.5,  ARQ + FICHAS, "petroleo"),                                # nenhum cientista quer o nome da CIA
 (12.0, FICHAS + GAVETA, "petroleo"),                             # você manda o dinheiro por uma fundação
 (16.0, Dc("ecologia"), "petroleo"),                              # Sociedade para a Investigação da Ecologia Humana
 (19.4, Dc("cutout"), "petroleo"),                                # isso é um cut-out
 (23.3, LS(996) + LS(1049), "petroleo"),                          # teste com voluntário não serve
 (28.0, SF(993, 1047) + X("mx41439", 5), "vermelho"),             # apartamentos em Nova York e São Francisco / LSD
 (35.0, Dc("casas"), "verde"),                                    # casas seguras
 (37.1, Dc("inst80") + Dc("univ44"), "verde"),                    # 80 instituições, 44 universidades…
 (44.0, LS(942) + GOTA, "vermelho"),                              # em 1953 um cientista toma LSD sem saber
 (49.8, X("mx22336", 5), "vermelho"),                             # 9 dias depois, cai da janela
 (53.0, Dc("ford"), "ambar"),                                     # a família de Frank Olson só descobre…
 (57.8, Dc("sub149"), "petroleo"),                                # 149 subprojetos
 (61.8, HE(587) + NX(6), "petroleo"),                             # 1973, o diretor deixa a CIA; Watergate
 (68.6, Dc("destruidos"), "vermelho"),                            # manda destruir os arquivos
 (71.1, GAVETA, "vermelho"),                                      # e acha que acabou
 (72.5, ARQ, "petroleo"),                                         # não é um espião, é a contabilidade
 (76.2, Dc("oitomil") + Dc("deposito"), "verde"),                 # 8 mil páginas em outro depósito
 (81.2, Dc("caixas"), "verde"),                                   # 1977, um pedido de acesso à informação
 (86.0, Dc("aprovado"), "vermelho"),                              # Parabéns, você criou o MKUltra
]
ETIQUETAS = [
 (0.3, 3.7, "13 DE ABRIL DE 1953", "MKULTRA É APROVADO"),
 (37.6, 43.8, "80 INSTITUIÇÕES", "44 universidades · 12 hospitais · 3 prisões"),
 (49.7, 53.0, "FRANK OLSON · 1953", None),
 (55.3, 57.6, "22 ANOS DEPOIS", "1975 · Ford pede desculpas à família"),
 (58.7, 61.7, "149 SUBPROJETOS", None),
 (62.1, 68.1, "1973", "Richard Helms deixa a CIA"),
 (76.4, 81.0, "ATÉ 8.000 PÁGINAS", "papéis financeiros, em outro depósito"),
 (81.3, 85.9, "1977", "audiência no Senado dos EUA"),
]
MUSICA = ("/home/user/estudio-ia/05-biblioteca/musica/mixkit/piano-horror-francisco-alvear.mp3", -22)
LUFS = -14.0; CARTAO = 2.4
