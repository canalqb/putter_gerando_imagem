#!/usr/bin/env python3
"""Teste para verificar tratamento de aspas no JSON"""

import json

# JSON do usuário com aspas simples
json_string = """{
  "modelo": "imagen-3.0-generate-002",
  "prompt": {
    "descricao_visual": "Thumbnail profissional para YouTube no formato 16:9. Fundo claro e vibrante: gradiente suave de branco (#FFFFFF) para cinza clarissimo (#F5F5F5) com leve textura tecnológica de grid sutil com linhas finas na cor #E8E8E8 — transmite clareza e ambiente de código. À esquerda: pessoa realista, rosto expressivo com sorriso confiante e aberto, olhar direto para o espectador, iluminação natural e quente — transmite autoridade de quem domina o tema. À direita: título 'TUPLA em PYTHON' em tipografia bold moderna, cor escura #111111 com a palavra 'TUPLA' em destaque na cor verde #28a745, fonte sem serifa de alto contraste. Elemento visual central: símbolo de parênteses com vírgulas '(1, 2, 3)' em fonte de código estilizada, cor #ffc107, integrado ao fundo de forma clean. Ícones discretos das linguagens JavaScript, Java, C# e Rust no canto inferior central, pequenos e alinhados. Logotipo '@CanalQb' no canto inferior direito em verde #28a745, pequeno e discreto. Composição equilibrada, respira bem, sem poluição visual.",
    "principios_marketing": "atenção imediata pelo rosto humano expressivo, contraste do verde no título, símbolo de código como âncora temática, logos de linguagens como prova de amplitude do conteúdo",
    "estilo": "clean tech, hyperrealistic face, natural warm lighting, high contrast typography, bright professional YouTube thumbnail, editorial quality",
    "aspectRatio": "16:9",
    "resolucao": "1920x1080",
    "negativePrompt": "fundo escuro, fundo preto, fundo cinza escuro, texto ilegível, baixo contraste, blur excessivo, pixelado, amador, rosto distorcido, mãos visíveis, cartoon, anime, 3D render, poluição visual"
  },
  "metadados_do_post": {
    "titulo": "Tupla em Python: Guia Completo + Exemplos em Outras Linguagens 2026",
    "tema_principal": "Python tuple()",
    "palavra_chave": "tupla python",
    "categoria": "Programação / Python",
    "cor_destaque": "#28a745",
    "expressao_baseada_no_titulo": "sorriso confiante e aberto, energia de quem vai compartilhar algo valioso sobre programação"
  }
}"""

print("Teste 1: JSON original (com aspas simples)")
print("=" * 60)
try:
    config = json.loads(json_string)
    print("✅ JSON válido!")
    print(f"Título: {config['metadados_do_post']['titulo']}")
except json.JSONDecodeError as e:
    print(f"❌ Erro: {e}")
    print(f"Linha: {e.lineno}, Coluna: {e.colno}")

print("\nTeste 2: JSON com aspas simples convertidas")
print("=" * 60)
json_convertido = json_string.replace("'", '"')
try:
    config = json.loads(json_convertido)
    print("✅ JSON válido após conversão!")
    print(f"Título: {config['metadados_do_post']['titulo']}")
except json.JSONDecodeError as e:
    print(f"❌ Erro: {e}")
    print(f"Linha: {e.lineno}, Coluna: {e.colno}")

print("\nTeste 3: JSON com aspas simples escapadas")
print("=" * 60)
json_escapado = json_string.replace("'", "\\'")
try:
    config = json.loads(json_escapado)
    print("✅ JSON válido após escape!")
    print(f"Título: {config['metadados_do_post']['titulo']}")
except json.JSONDecodeError as e:
    print(f"❌ Erro: {e}")
    print(f"Linha: {e.lineno}, Coluna: {e.colno}")
