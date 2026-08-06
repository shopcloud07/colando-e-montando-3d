#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Otimizador de imagens para paginas de venda estaticas.

COMO USAR
---------
1. Coloque este arquivo na pasta da pagina (do lado do index.html).
2. Rode:  python otimizar-imagens.py
   Na primeira vez ele so SIMULA: mostra o relatorio e nao grava nada.
3. Se gostar dos numeros, mude MODO_SIMULACAO para False e rode de novo.

SEGURANCA
---------
- Antes de gravar qualquer coisa, copia tudo para images/_originais/.
- Sempre le a partir de _originais/, nunca do resultado anterior.
  Rodar 10 vezes seguidas da o mesmo resultado (sem perda geracional).
- Nunca aumenta imagem. So reduz quando tem certeza do tamanho de exibicao.
- Se o arquivo otimizado ficar MAIOR que o original, mantem o original.
- Preserva transparencia onde ela e usada de verdade.

PARA RESTAURAR TUDO
-------------------
Apague a pasta images/ e renomeie images/_originais/ para images/.
"""

import io
import os
import re
import shutil
import sys
import urllib.parse

from PIL import Image

# ----------------------------------------------------------------------------
# CONFIGURACAO
# ----------------------------------------------------------------------------

MODO_SIMULACAO = True   # True = so mostra o relatorio, nao grava nada

QUALIDADE = 82          # 0-100. 80-85 = indistinguivel a olho nu.
                        # Abaixo de 75 comeca a aparecer artefato em degrade.

ESCALA_RETINA = 2       # Guarda o dobro do tamanho de exibicao, para telas
                        # de alta densidade nao ficarem borradas.

LARGURA_MAXIMA = 1400   # Teto absoluto. Nenhuma imagem precisa passar disso
                        # numa pagina cujo container mais largo tem ~1152px.

HTML = "index.html"
PASTA = "images"
BACKUP = os.path.join(PASTA, "_originais")

EXTENSOES = (".webp", ".png", ".jpg", ".jpeg")


# ----------------------------------------------------------------------------
# DESCOBRIR EM QUE TAMANHO CADA IMAGEM APARECE NA PAGINA
# ----------------------------------------------------------------------------

def larguras_no_html(html, arquivo):
    """
    Procura todas as tags <img> que usam este arquivo e devolve a maior
    largura de exibicao em pixels de CSS.

    Devolve None quando NAO da para ter certeza (ex.: a imagem usa 'sizes'
    com unidade vw, ou e object-cover sem largura declarada). Nesse caso o
    script nao redimensiona - so recomprime. Preferimos economizar menos a
    correr o risco de deixar a imagem borrada.
    """
    alvos = {arquivo, urllib.parse.quote(arquivo)}
    encontradas = []

    for tag in re.findall(r"<img\b[^>]*>", html):
        if not any(a in tag for a in alvos):
            continue

        # 1) Classe utilitaria do Tailwind: w-8 significa 8 * 4px = 32px.
        #    O (?:^|\s) evita casar com max-w-2xl, sm:w-40 etc.
        classe = re.search(r'class="([^"]*)"', tag)
        if classe:
            m = re.search(r"(?:^|\s)w-(\d+)(?:\s|$)", classe.group(1))
            if m:
                encontradas.append(int(m.group(1)) * 4)
                continue

        # 2) Atributo width, mas so confiavel quando NAO ha 'sizes'.
        #    Com 'sizes' o width vira apenas metadado de proporcao e nao
        #    corresponde ao tamanho real na tela.
        largura = re.search(r'\bwidth="(\d+)"', tag)
        if largura and "sizes=" not in tag:
            encontradas.append(int(largura.group(1)))
            continue

        # 3) Qualquer outro caso: incerto.
        return None

    if not encontradas:
        return None
    return max(encontradas)


def tem_transparencia_real(im):
    """RGBA nem sempre usa o canal alfa. Confere se ha pixel nao opaco."""
    if im.mode not in ("RGBA", "LA", "PA"):
        return False
    alfa = im.convert("RGBA").getchannel("A")
    return alfa.getextrema()[0] < 255


# ----------------------------------------------------------------------------
# PROCESSAMENTO
# ----------------------------------------------------------------------------

def processar(nome, html, pasta_origem):
    """Devolve (bytes_finais, largura_final, altura_final, nota)."""
    origem = os.path.join(pasta_origem, nome)
    with Image.open(origem) as im:
        im.load()
        largura_orig, altura_orig = im.size
        alfa = tem_transparencia_real(im)

        # --- decidir a largura de destino ---
        exibida = larguras_no_html(html, nome)
        if exibida:
            alvo = min(exibida * ESCALA_RETINA, LARGURA_MAXIMA)
            motivo = "exibida com %dpx" % exibida
        else:
            alvo = LARGURA_MAXIMA
            motivo = "tamanho de exibicao incerto"

        if alvo < largura_orig:
            nova_altura = round(altura_orig * alvo / largura_orig)
            im = im.resize((alvo, nova_altura), Image.LANCZOS)
            nota = "redimensionada (%s)" % motivo
        else:
            nota = "so recomprimida"  # nunca aumentamos

        # --- alfa: descartar so quando comprovadamente inutil ---
        if im.mode in ("RGBA", "LA", "PA") and not alfa:
            im = im.convert("RGB")
            nota += " + alfa inutil removido"
        elif im.mode not in ("RGB", "RGBA"):
            im = im.convert("RGBA" if alfa else "RGB")

        buf = io.BytesIO()
        im.save(buf, "WEBP", quality=QUALIDADE, method=6)
        return buf.getvalue(), im.size[0], im.size[1], nota


def main():
    if not os.path.isfile(HTML):
        sys.exit("ERRO: %s nao encontrado. Rode o script na pasta da pagina." % HTML)
    if not os.path.isdir(PASTA):
        sys.exit("ERRO: pasta %s/ nao encontrada." % PASTA)

    html = io.open(HTML, encoding="utf-8").read()

    # De onde ler os originais.
    #   - backup ja existe  -> le dele (garante que rodar de novo nao acumula perda)
    #   - nao existe + gravando -> cria o backup primeiro, depois le dele
    #   - nao existe + simulacao -> le da pasta normal, sem criar nada
    if os.path.isdir(BACKUP):
        origem = BACKUP
        print("Backup ja existe. Lendo os originais de %s/\n" % BACKUP)
    elif MODO_SIMULACAO:
        origem = PASTA
        print("[simulacao] o backup em %s/ seria criado na execucao real\n" % BACKUP)
    else:
        os.makedirs(BACKUP)
        for f in os.listdir(PASTA):
            if f.lower().endswith(EXTENSOES):
                shutil.copy2(os.path.join(PASTA, f), os.path.join(BACKUP, f))
        origem = BACKUP
        print("Backup criado em %s/\n" % BACKUP)

    arquivos = sorted(f for f in os.listdir(origem) if f.lower().endswith(EXTENSOES))

    print("modo ......... %s" % ("SIMULACAO (nada sera gravado)" if MODO_SIMULACAO else "GRAVANDO"))
    print("qualidade .... %d" % QUALIDADE)
    print("retina ....... %dx   teto: %dpx" % (ESCALA_RETINA, LARGURA_MAXIMA))
    print()
    print("%9s %9s %7s   %-13s %s" % ("ANTES", "DEPOIS", "GANHO", "DIMENSOES", "ARQUIVO / ACAO"))
    print("-" * 100)

    total_antes = total_depois = 0
    mantidos = 0

    for nome in arquivos:
        antes = os.path.getsize(os.path.join(origem, nome))
        try:
            dados, w, h, nota = processar(nome, html, origem)
        except Exception as e:
            print("%9s %9s %7s   %-13s %s  [ERRO: %s]" % (
                "%.0fKB" % (antes / 1024), "-", "-", "-", nome[:30], e))
            total_antes += antes
            total_depois += antes
            continue

        # Regra de ouro: se nao melhorou, fica como estava.
        if len(dados) >= antes:
            depois, nota, dados = antes, "MANTIDO (otimizar deixaria maior)", None
            mantidos += 1
        else:
            depois = len(dados)

        if not MODO_SIMULACAO and dados is not None:
            with open(os.path.join(PASTA, nome), "wb") as f:
                f.write(dados)

        ganho = (1 - depois / antes) * 100 if antes else 0
        print("%8.0fKB %8.0fKB %6.0f%%   %-13s %s  -> %s" % (
            antes / 1024, depois / 1024, ganho, "%dx%d" % (w, h), nome[:28], nota))

        total_antes += antes
        total_depois += depois

    print("-" * 100)
    ganho_total = (1 - total_depois / total_antes) * 100 if total_antes else 0
    print("TOTAL: %.0f KB -> %.0f KB   (economia de %.0f KB, %.0f%%)" % (
        total_antes / 1024, total_depois / 1024,
        (total_antes - total_depois) / 1024, ganho_total))
    if mantidos:
        print("%d arquivo(s) mantido(s) intacto(s): ja estavam otimos." % mantidos)

    print()
    if MODO_SIMULACAO:
        print(">> Nada foi gravado. Para aplicar de verdade, abra este arquivo,")
        print("   troque MODO_SIMULACAO para False e rode de novo.")
    else:
        print(">> Pronto. Os originais estao intactos em %s/" % BACKUP)
        print("   Para desfazer: apague os arquivos de %s/ e copie de volta os de %s/" % (
            PASTA, BACKUP))


if __name__ == "__main__":
    main()
