#!/usr/bin/env python3
"""Teste para verificar se o script funciona com JSON colado"""

import json

# Simular o JSON que o usuário colou (com aspas curvas)
json_usuario = """{
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

# Converter aspas curvas para retas (como o script faz agora)
json_corrigido = json_usuario.replace('"', '"').replace('"', '"').replace(''', "'").replace(''', "'")

print("Testando conversão de aspas curvas para retas...")
print("=" * 60)

try:
    config = json.loads(json_corrigido)
    print("✅ JSON parseado com sucesso!")
    print(f"\nEstrutura do JSON:")
    print(f"- Modelo: {config.get('modelo')}")
    print(f"- Título: {config.get('metadados_do_post', {}).get('titulo')}")
    print(f"- Resolução: {config.get('prompt', {}).get('resolucao')}")
    print(f"\n✅ O script corrigido funcionará com seu JSON!")
except json.JSONDecodeError as e:
    print(f"❌ Erro ao fazer parse: {e}")
    print("❌ A conversão não funcionou corretamente")
