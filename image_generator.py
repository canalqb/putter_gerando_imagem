#!/usr/bin/env python3
"""
Gerador de Imagens Real usando APIs Gratuitas
Funciona com Hugging Face, Pollinations AI, e outras APIs gratuitas
"""

import json
import requests
import base64
import os
from datetime import datetime
import webbrowser
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse

class ImageGenerator:
    def __init__(self, config=None):
        self.config = config
        self.generated_images = []
        
    def load_config_from_string(self, json_string):
        """Carregar configuração JSON de uma string"""
        try:
            # Converter apenas aspas curvas para aspas retas (se necessário)
            json_string = json_string.replace('"', '"').replace('"', '"').replace(''', "'").replace(''', "'")
            
            config = json.loads(json_string)
            self.config = config
            return config
        except json.JSONDecodeError as e:
            print(f"❌ Erro ao ler JSON: {e}")
            print("💡 Dica: Verifique se as aspas são retas (\") e não curvas ("")")
            print("💡 Aspas simples dentro do texto (como 'TUPLA em PYTHON') são permitidas e não causam problemas.")
            print(f"💡 Erro na linha {e.lineno}, coluna {e.colno}")
            return None
    
    def load_config_from_file(self, config_file):
        """Carregar configuração JSON de um arquivo"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.config = config
                return config
        except FileNotFoundError:
            print(f"❌ Arquivo '{config_file}' não encontrado")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ Erro ao ler JSON: {e}")
            return None
    
    def generate_with_pollinations(self, prompt, width=1920, height=1080):
        """Gerar imagem usando Pollinations AI (gratuito)"""
        try:
            print("   📡 Conectando à API Pollinations...")
            
            # Pollinations AI - API gratuita e funcional
            encoded_prompt = urllib.parse.quote(prompt)
            url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
            
            # Adicionar parâmetros de tamanho
            params = {
                'width': width,
                'height': height,
                'seed': datetime.now().timestamp(),
                'nologo': 'true',  # Remover logo
                'model': 'flux'  # Usar modelo Flux (mais rápido)
            }
            
            print("   ⏳ Baixando imagem (isso pode levar 30-60 segundos)...")
            response = requests.get(url, params=params, timeout=120, stream=True)
            
            if response.status_code == 200:
                # Salvar imagem
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"thumbnail_{timestamp}.png"
                
                print("   💾 Salvando imagem...")
                with open(filename, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                self.generated_images.append({
                    'filename': filename,
                    'url': url,
                    'method': 'Pollinations AI',
                    'prompt': prompt
                })
                
                print(f"   ✅ Imagem gerada: {filename}")
                return filename
            else:
                print(f"   ❌ Erro Pollinations: {response.status_code}")
                if response.status_code == 402:
                    print("   💡 A API pode estar temporariamente bloqueada. Tentando método alternativo...")
                    return self.generate_with_pollinations_alt(prompt, width, height)
                return None
                
        except requests.exceptions.Timeout:
            print("   ⏱️  Timeout - a API demorou muito para responder")
            return None
        except Exception as e:
            print(f"   ❌ Erro ao gerar com Pollinations: {e}")
            return None
    
    def generate_with_pollinations_alt(self, prompt, width=1920, height=1080):
        """Método alternativo para Pollinations com diferentes parâmetros"""
        try:
            print("   🔄 Tentando método alternativo...")
            
            encoded_prompt = urllib.parse.quote(prompt)
            url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
            
            # Parâmetros alternativos
            params = {
                'width': width,
                'height': height,
                'seed': int(datetime.now().timestamp()),
                'enhance': 'true'
            }
            
            response = requests.get(url, params=params, timeout=120, stream=True)
            
            if response.status_code == 200:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"thumbnail_alt_{timestamp}.png"
                
                print("   💾 Salvando imagem...")
                with open(filename, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                self.generated_images.append({
                    'filename': filename,
                    'url': url,
                    'method': 'Pollinations AI (Alt)',
                    'prompt': prompt
                })
                
                print(f"   ✅ Imagem gerada (alt): {filename}")
                return filename
            else:
                print(f"   ❌ Erro método alternativo: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"   ❌ Erro no método alternativo: {e}")
            return None
    
    def generate_with_huggingface(self, prompt):
        """Gerar imagem usando Hugging Face Inference API (gratuito)"""
        try:
            # Usando modelo estável e gratuito
            API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
            
            headers = {
                "Authorization": "Bearer hf_dummy",  # Tokens públicos funcionam para testes
                "Content-Type": "application/json",
            }
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "width": 1920,
                    "height": 1080,
                    "num_inference_steps": 20,
                    "guidance_scale": 7.5
                }
            }
            
            response = requests.post(API_URL, headers=headers, json=payload, timeout=120)
            
            if response.status_code == 200:
                # Salvar imagem
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"satsman_huggingface_{timestamp}.png"
                
                with open(filename, 'wb') as f:
                    f.write(response.content)
                
                self.generated_images.append({
                    'filename': filename,
                    'method': 'Hugging Face',
                    'prompt': prompt
                })
                
                print(f"✅ Imagem gerada com Hugging Face: {filename}")
                return filename
            else:
                print(f"❌ Erro Hugging Face: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Erro ao gerar com Hugging Face: {e}")
            return None
    
    def create_optimized_prompt(self):
        """Criar prompt otimizado para o thumbnail"""
        if not self.config:
            return None
        
        # Tentar extrair informações do JSON de forma flexível
        prompt_desc = ""
        estilo = ""
        negative_prompt = ""
        
        # Verificar diferentes estruturas possíveis do JSON
        if "prompt" in self.config:
            prompt_data = self.config["prompt"]
            if "descricao_visual" in prompt_data:
                prompt_desc = prompt_data["descricao_visual"]
            elif "description" in prompt_data:
                prompt_desc = prompt_data["description"]
            elif "text" in prompt_data:
                prompt_desc = prompt_data["text"]
            elif isinstance(prompt_data, str):
                prompt_desc = prompt_data
            
            if "estilo" in prompt_data:
                estilo = prompt_data["estilo"]
            elif "style" in prompt_data:
                estilo = prompt_data["style"]
            
            if "negativePrompt" in prompt_data:
                negative_prompt = prompt_data["negativePrompt"]
            elif "negative_prompt" in prompt_data:
                negative_prompt = prompt_data["negative_prompt"]
            elif "negative" in prompt_data:
                negative_prompt = prompt_data["negative"]
        elif "description" in self.config:
            prompt_desc = self.config["description"]
        elif "text" in self.config:
            prompt_desc = self.config["text"]
        elif isinstance(self.config, str):
            prompt_desc = self.config
        
        # Se não encontrou descrição, usar todo o JSON como prompt
        if not prompt_desc:
            prompt_desc = str(self.config)
        
        # Extrair informações adicionais se disponíveis
        width = 1920
        height = 1080
        
        if "prompt" in self.config and "resolucao" in self.config["prompt"]:
            resolucao = self.config["prompt"]["resolucao"]
            if "x" in resolucao:
                parts = resolucao.split("x")
                if len(parts) == 2:
                    try:
                        width = int(parts[0])
                        height = int(parts[1])
                    except:
                        pass
        
        # Prompt otimizado para APIs de imagem
        if estilo and negative_prompt:
            optimized_prompt = f"""
Professional YouTube thumbnail 16:9, cinematic theme. 
{prompt_desc}
Style: {estilo}
High quality, detailed, dramatic lighting, 
achievement unlock aesthetic, no watermarks, no text borders, 
professional design, ultra realistic, 8k resolution.
Negative: {negative_prompt}
""".strip()
        elif estilo:
            optimized_prompt = f"""
Professional YouTube thumbnail 16:9, cinematic theme. 
{prompt_desc}
Style: {estilo}
High quality, detailed, dramatic lighting, 
achievement unlock aesthetic, no watermarks, no text borders, 
professional design, ultra realistic, 8k resolution.
""".strip()
        else:
            optimized_prompt = f"""
Professional YouTube thumbnail 16:9, cinematic theme. 
{prompt_desc}
High quality, detailed, dramatic lighting, 
achievement unlock aesthetic, no watermarks, no text borders, 
professional design, ultra realistic, 8k resolution.
""".strip()
        
        return optimized_prompt, width, height
    
    def generate_all_methods(self, use_huggingface=False):
        """Tentar gerar imagem com métodos disponíveis"""
        if not self.config:
            print("❌ Configuração não carregada")
            return False
        
        prompt_result = self.create_optimized_prompt()
        if not prompt_result:
            print("❌ Erro ao criar prompt")
            return False
        
        if isinstance(prompt_result, tuple):
            prompt, width, height = prompt_result
        else:
            prompt = prompt_result
            width, height = 1920, 1080
        
        print("🎨 Iniciando geração de imagens...")
        print(f"📝 Prompt: {prompt[:100]}...")
        print(f"📐 Resolução: {width}x{height}")
        print("=" * 60)
        
        # Tentar Pollinations (mais confiável)
        print("1️⃣ Tentando Pollinations AI (método mais rápido)...")
        result1 = self.generate_with_pollinations(prompt, width, height)
        
        # Tentar Hugging Face apenas se solicitado
        if use_huggingface:
            print("\n2️⃣ Tentando Hugging Face...")
            result2 = self.generate_with_huggingface(prompt)
        
        # Resumo
        print("\n" + "=" * 60)
        print("📊 RESUMO DA GERAÇÃO:")
        print(f"✅ Imagens geradas: {len(self.generated_images)}")
        
        for i, img in enumerate(self.generated_images, 1):
            print(f"   {i}. {img['filename']} ({img['method']})")
        
        if self.generated_images:
            print(f"\n🎯 SUCESSO! Imagens salvas em: {os.getcwd()}")
            return True
        else:
            print("\n❌ Nenhuma imagem foi gerada. Tente novamente.")
            return False
    
    def create_web_interface(self):
        """Criar interface web para visualizar resultados"""
        html_content = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resultados - Gerador Satsman</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .container {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        h1 {{
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }}
        .image-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .image-card {{
            background: #f8f9fa;
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }}
        .image-card img {{
            width: 100%;
            border-radius: 8px;
            margin-bottom: 10px;
        }}
        .image-info {{
            font-size: 14px;
            color: #666;
        }}
        .button {{
            background: #f7931a;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            margin: 5px;
        }}
        .button:hover {{
            background: #e8840a;
        }}
        .status {{
            background: #d4edda;
            color: #155724;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎨 Resultados - Gerador Satsman</h1>
        
        <div class="status">
            ✅ Geração concluída! {len(self.generated_images)} imagem(ns) gerada(s)
        </div>
        
        <div class="image-grid>
            {self.generate_image_cards()}
        </div>
        
        <div style="text-align: center; margin-top: 30px;">
            <a href="javascript:history.back()" class="button">← Voltar</a>
            <a href="javascript:window.close()" class="button">Fechar</a>
        </div>
    </div>
</body>
</html>
        """
        
        with open('resultados.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return 'resultados.html'
    
    def generate_image_cards(self):
        """Gerar cards HTML para as imagens"""
        if not self.generated_images:
            return "<p>Nenhuma imagem foi gerada.</p>"
        
        cards = ""
        for img in self.generated_images:
            cards += f"""
            <div class="image-card">
                <img src="{img['filename']}" alt="Imagem gerada">
                <div class="image-info">
                    <strong>Arquivo:</strong> {img['filename']}<br>
                    <strong>Método:</strong> {img['method']}<br>
                    <strong>Prompt:</strong> {img['prompt'][:100]}...
                </div>
                <a href="{img['filename']}" download="{img['filename']}" class="button">
                    💾 Baixar
                </a>
            </div>
            """
        
        return cards

def validate_json_structure(config):
    """Validar estrutura básica do JSON"""
    if not isinstance(config, dict):
        print("❌ O JSON deve ser um objeto/dicionário")
        return False
    
    # Verificar se tem pelo menos alguma informação útil
    has_prompt = "prompt" in config or "description" in config or "text" in config
    if not has_prompt:
        print("⚠️  Aviso: JSON não contém campos de prompt conhecidos (prompt, description, text)")
        print("   Tentando usar o JSON completo como prompt...")
    
    return True

def get_user_json():
    """Obter JSON do usuário via input ou arquivo"""
    print("\n📝 Como você deseja fornecer o JSON?")
    print("1. Colar o JSON diretamente no terminal")
    print("2. Carregar de um arquivo")
    print("3. Usar arquivo padrão (image_config.json)")
    
    choice = input("\nEscolha uma opção (1/2/3): ").strip()
    
    if choice == "1":
        print("\n📋 Cole seu JSON abaixo (pressione Enter duas vezes para finalizar):")
        print("   (Ctrl+D ou Ctrl+Z também podem funcionar para finalizar)")
        
        lines = []
        try:
            while True:
                line = input()
                if line.strip() == "" and len(lines) > 0:
                    # Verificar se é o final (duas linhas vazias consecutivas)
                    if lines[-1].strip() == "":
                        break
                lines.append(line)
        except EOFError:
            pass
        
        json_string = "\n".join(lines)
        return json_string, "string"
    
    elif choice == "2":
        file_path = input("\n📁 Caminho do arquivo JSON: ").strip()
        if not file_path:
            print("❌ Caminho não fornecido")
            return None, None
        
        if not os.path.exists(file_path):
            print(f"❌ Arquivo não encontrado: {file_path}")
            return None, None
        
        with open(file_path, 'r', encoding='utf-8') as f:
            json_string = f.read()
        
        return json_string, "file"
    
    elif choice == "3":
        if os.path.exists("image_config.json"):
            with open("image_config.json", 'r', encoding='utf-8') as f:
                json_string = f.read()
            return json_string, "file"
        else:
            print("❌ Arquivo image_config.json não encontrado")
            return None, None
    
    else:
        print("❌ Opção inválida")
        return None, None

def main():
    """Função principal"""
    import sys
    
    # Verificar se há argumentos de linha de comando
    if len(sys.argv) > 1:
        # Modo automático com arquivo JSON
        json_file = sys.argv[1]
        if os.path.exists(json_file):
            print(f"🎨 Gerador de Imagens - Modo Automático")
            print("=" * 60)
            print(f"📁 Carregando JSON: {json_file}")
            
            generator = ImageGenerator()
            config = generator.load_config_from_file(json_file)
            
            if config and validate_json_structure(config):
                print("✅ JSON carregado com sucesso!")
                success = generator.generate_all_methods(use_huggingface=False)
                
                if success:
                    html_file = generator.create_web_interface()
                    print(f"\n🌐 Interface web criada: {html_file}")
                    try:
                        webbrowser.open(f'file://{os.path.abspath(html_file)}')
                        print("🚀 Abrindo interface web no navegador...")
                    except:
                        print("📂 Abra o arquivo 'resultados.html' manualmente no navegador")
            else:
                print("❌ Erro ao carregar JSON")
        else:
            print(f"❌ Arquivo não encontrado: {json_file}")
        return
    
    # Modo interativo
    print("🎨 Gerador de Imagens com JSON Personalizado")
    print("=" * 60)
    print("Este script permite que você insira seu próprio JSON")
    print("para gerar imagens personalizadas usando APIs gratuitas.")
    print("=" * 60)
    
    # Obter JSON do usuário
    json_string, source_type = get_user_json()
    
    if not json_string:
        print("\n❌ Não foi possível obter o JSON. Encerrando.")
        return
    
    # Criar gerador
    generator = ImageGenerator()
    
    # Carregar configuração
    print("\n🔍 Validando JSON...")
    if source_type == "string":
        config = generator.load_config_from_string(json_string)
    else:
        config = generator.load_config_from_file(json_string if source_type == "file" and os.path.exists(json_string) else "image_config.json")
    
    if not config:
        print("\n❌ Erro ao carregar configuração. Verifique o JSON.")
        return
    
    # Validar estrutura
    if not validate_json_structure(config):
        print("\n❌ Estrutura do JSON inválida.")
        return
    
    print("✅ JSON carregado com sucesso!")
    print(f"📊 Estrutura: {json.dumps(config, indent=2, ensure_ascii=False)[:200]}...")
    
    # Confirmar antes de gerar
    try:
        confirm = input("\n🚀 Deseja gerar as imagens? (s/n): ").strip().lower()
        if confirm != 's':
            print("❌ Operação cancelada pelo usuário.")
            return
    except (EOFError, KeyboardInterrupt):
        print("\n⚠️  Execução automática detectada, gerando imagens...")
    
    # Gerar imagens (apenas Pollinations por padrão, mais rápido)
    success = generator.generate_all_methods(use_huggingface=False)
    
    if success:
        # Criar interface web
        html_file = generator.create_web_interface()
        print(f"\n🌐 Interface web criada: {html_file}")
        
        # Abrir navegador
        try:
            webbrowser.open(f'file://{os.path.abspath(html_file)}')
            print("🚀 Abrindo interface web no navegador...")
        except:
            print("📂 Abra o arquivo 'resultados.html' manualmente no navegador")
    
    print("\n✅ Processo concluído!")

if __name__ == "__main__":
    main()
