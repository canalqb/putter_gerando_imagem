#!/usr/bin/env python3
"""Teste para verificar conversão de aspas curvas"""

import json

# JSON com aspas curvas (como o usuário colou)
json_com_aspas_curvas = """{
  "modelo": "imagen-3.0-generate-002",
  "prompt": {
    "descricao_visual": "Thumbnail profissional para YouTube no formato 16:9. Fundo claro e vibrante."
  }
}"""

# Converter aspas curvas para retas
json_corrigido = json_com_aspas_curvas.replace('"', '"').replace('"', '"').replace(''', "'").replace(''', "'")

print("JSON original (com aspas curvas):")
print(json_com_aspas_curvas)
print("\nJSON corrigido (com aspas retas):")
print(json_corrigido)

try:
    config = json.loads(json_corrigido)
    print("\n✅ JSON parseado com sucesso!")
    print(f"Configuração: {config}")
except json.JSONDecodeError as e:
    print(f"\n❌ Erro ao fazer parse: {e}")
