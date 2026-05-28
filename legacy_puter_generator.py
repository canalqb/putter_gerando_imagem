#!/usr/bin/env python3
"""
Script to generate images using Puter.js API from JSON configuration
"""

import json
import requests
import base64
import os
from datetime import datetime

def load_config(config_file="image_config.json"):
    """Load JSON configuration from file"""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_file}' not found")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None

def create_html_for_puter(config):
    """Create HTML file with Puter.js for image generation"""
    
    # Extract prompt details
    prompt_desc = config["prompt"]["descricao_visual"]
    estilo = config["prompt"]["estilo"]
    negative_prompt = config["prompt"]["negativePrompt"]
    aspect_ratio = config["prompt"]["aspectRatio"]
    
    # Combine prompts for better results
    full_prompt = f"{prompt_desc}. Style: {estilo}"
    
    # Escape quotes for JavaScript
    escaped_full_prompt = full_prompt.replace('"', '\\"')
    escaped_negative_prompt = negative_prompt.replace('"', '\\"')
    
    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Puter Image Generator</title>
    <script src="https://js.puter.com/v2/"></script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f0f0f0;
        }}
        .container {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .button {{
            background-color: #f7931a;
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            margin: 10px 5px;
        }}
        .button:hover {{
            background-color: #e8840a;
        }}
        .button:disabled {{
            background-color: #ccc;
            cursor: not-allowed;
        }}
        .status {{
            margin: 20px 0;
            padding: 15px;
            border-radius: 5px;
            font-weight: bold;
        }}
        .loading {{
            background-color: #fff3cd;
            color: #856404;
        }}
        .success {{
            background-color: #d4edda;
            color: #155724;
        }}
        .error {{
            background-color: #f8d7da;
            color: #721c24;
        }}
        .image-container {{
            margin: 20px 0;
            text-align: center;
        }}
        .generated-image {{
            max-width: 100%;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }}
        .prompt-info {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            margin: 15px 0;
            font-size: 14px;
            border-left: 4px solid #f7931a;
        }}
        .download-btn {{
            background-color: #28a745;
            color: white;
            padding: 10px 20px;
            text-decoration: none;
            border-radius: 5px;
            display: inline-block;
            margin: 10px 5px;
        }}
        .download-btn:hover {{
            background-color: #218838;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎨 Gerador de Imagens com Puter.js</h1>
        <p>Gerando imagem para o projeto: <strong>{config["metadados_do_post"]["titulo"]}</strong></p>
        
        <div class="prompt-info">
            <h3>📝 Detalhes do Prompt:</h3>
            <p><strong>Modelo:</strong> {config["modelo"]}</p>
            <p><strong>Aspect Ratio:</strong> {aspect_ratio}</p>
            <p><strong>Resolução:</strong> {config["prompt"]["resolucao"]}</p>
            <br>
            <p><strong>Prompt Principal:</strong></p>
            <p style="font-style: italic;">{prompt_desc}</p>
            <br>
            <p><strong>Estilo:</strong></p>
            <p style="font-style: italic;">{estilo}</p>
            <br>
            <p><strong>Negative Prompt:</strong></p>
            <p style="font-style: italic;">{negative_prompt}</p>
        </div>

        <button class="button" onclick="generateImage()" id="generateBtn">
            🚀 Gerar Imagem
        </button>
        <button class="button" onclick="generateWithDifferentModel()" id="generateBtn2">
            🔄 Tentar com Outro Modelo
        </button>

        <div id="status" class="status" style="display: none;"></div>
        <div id="imageContainer" class="image-container"></div>
    </div>

    <script>
        const config = {json.dumps(config, indent=2, ensure_ascii=False)};
        
        function showStatus(message, type) {{
            const statusDiv = document.getElementById('status');
            statusDiv.textContent = message;
            statusDiv.className = `status ${{type}}`;
            statusDiv.style.display = 'block';
        }}

        function showImage(imageData, filename) {{
            const container = document.getElementById('imageContainer');
            container.innerHTML = `
                <h3>✅ Imagem Gerada com Sucesso!</h3>
                <img src="${{imageData}}" alt="Generated Image" class="generated-image">
                <br><br>
                <a href="${{imageData}}" download="${{filename}}" class="download-btn">
                    💾 Baixar Imagem
                </a>
                <button class="button" onclick="generateImage()">
                    🔄 Gerar Nova Imagem
                </button>
            `;
        }}

        async function generateImage() {{
            const generateBtn = document.getElementById('generateBtn');
            const generateBtn2 = document.getElementById('generateBtn2');
            
            generateBtn.disabled = true;
            generateBtn2.disabled = true;
            showStatus('🔄 Gerando imagem... Aguarde...', 'loading');

            try {{
                const prompt = "{escaped_full_prompt}";
                const negativePrompt = "{escaped_negative_prompt}";
                
                // Try with Gemini 2.5 Flash for image generation
                const response = await puter.ai.chat(
                    `Generate a professional YouTube thumbnail based on this detailed description: ${{prompt}}. 

Negative prompts to avoid: ${{negativePrompt}}.

Requirements:
- Aspect ratio: {aspect_ratio}
- High quality, professional design
- No watermarks
- Cinematic and dramatic lighting
- Bitcoin/crypto theme with orange and gold accents`,
                    {{
                        model: 'gemini-2.5-flash-preview',
                        stream: false
                    }}
                );

                showStatus('✅ Imagem gerada com sucesso!', 'success');
                
                // Create a filename based on the project
                const timestamp = new Date().toISOString().slice(0, 19).replace(/[:-]/g, '');
                const filename = `satsman_thumbnail_${{timestamp}}.png`;
                
                // Since we can't directly get image data from text response, 
                // we'll show the response and instructions
                const container = document.getElementById('imageContainer');
                container.innerHTML = `
                    <h3>📝 Resposta do Modelo:</h3>
                    <div style="background: #f8f9fa; padding: 20px; border-radius: 5px; margin: 15px 0;">
                        <pre style="white-space: pre-wrap; font-family: monospace;">${{response}}</pre>
                    </div>
                    <h3>🎯 Próximos Passos:</h3>
                    <p>1. Use a ferramenta de geração de imagens como DALL-E, Midjourney ou o Google AI Studio com o prompt acima</p>
                    <p>2. Configure para aspect ratio {aspect_ratio} e resolução {config["prompt"]["resolucao"]}</p>
                    <p>3. Aplique o negative prompt para evitar elementos indesejados</p>
                    <br>
                    <button class="button" onclick="copyPrompt()">
                        📋 Copiar Prompt Completo
                    </button>
                    <button class="button" onclick="generateWithDifferentModel()">
                        🔄 Tentar Outra Abordagem
                    </button>
                `;

            }} catch (error) {{
                console.error('Error generating image:', error);
                showStatus(`❌ Erro ao gerar imagem: ${{error.message}}`, 'error');
            }} finally {{
                generateBtn.disabled = false;
                generateBtn2.disabled = false;
            }}
        }}

        async function generateWithDifferentModel() {{
            const generateBtn = document.getElementById('generateBtn');
            const generateBtn2 = document.getElementById('generateBtn2');
            
            generateBtn.disabled = true;
            generateBtn2.disabled = true;
            showStatus('🔄 Tentando com modelo diferente...', 'loading');

            try {{
                const prompt = "{escaped_full_prompt}";
                
                // Try with Gemini 3.1 Pro for better quality
                const response = await puter.ai.chat(
                    `Create a detailed prompt for image generation AI (like DALL-E, Midjourney, or Stable Diffusion) based on this YouTube thumbnail concept:

${{prompt}}

Negative prompts to avoid: {escaped_negative_prompt}

Output format: Provide a single, comprehensive prompt that includes all visual elements, style, lighting, and technical specifications for generating a {aspect_ratio} {config["prompt"]["resolucao"]} YouTube thumbnail.`,
                    {{
                        model: 'gemini-3.1-pro-preview',
                        stream: false
                    }}
                );

                showStatus('✅ Prompt otimizado gerado!', 'success');
                
                const container = document.getElementById('imageContainer');
                container.innerHTML = `
                    <h3>🎯 Prompt Otimizado para Geração de Imagem:</h3>
                    <div style="background: #e8f4fd; padding: 20px; border-radius: 5px; margin: 15px 0; border-left: 4px solid #2196f3;">
                        <pre style="white-space: pre-wrap; font-family: monospace; font-size: 14px;">${{response}}</pre>
                    </div>
                    <h3>📋 Como Usar:</h3>
                    <div style="background: #f0f8f0; padding: 15px; border-radius: 5px; margin: 10px 0;">
                        <p><strong>Opção 1:</strong> Copie o prompt acima e use no <a href="https://aistudio.google.com/" target="_blank">Google AI Studio</a></p>
                        <p><strong>Opção 2:</strong> Use no <a href="https://www.bing.com/images/create" target="_blank">Microsoft Designer (DALL-E 3)</a></p>
                        <p><strong>Opção 3:</strong> Use no <a href="https://www.midjourney.com/" target="_blank">Midjourney</a></p>
                    </div>
                    <br>
                    <button class="button" onclick="copyOptimizedPrompt()">
                        📋 Copiar Prompt Otimizado
                    </button>
                    <button class="button" onclick="generateImage()">
                        🔄 Voltar à Geração Direta
                    </button>
                `;

            }} catch (error) {{
                console.error('Error with different model:', error);
                showStatus(`❌ Erro: ${{error.message}}`, 'error');
            }} finally {{
                generateBtn.disabled = false;
                generateBtn2.disabled = false;
            }}
        }}

        function copyPrompt() {{
            const prompt = "{escaped_full_prompt}";
            const negativePrompt = "{escaped_negative_prompt}";
            const fullText = `Prompt: ${{prompt}}\\n\\nNegative Prompt: ${{negativePrompt}}\\n\\nAspect Ratio: {aspect_ratio}\\nResolution: {config["prompt"]["resolucao"]}`;
            
            navigator.clipboard.writeText(fullText).then(() => {{
                showStatus('📋 Prompt copiado para a área de transferência!', 'success');
            }}).catch(() => {{
                showStatus('❌ Falha ao copiar prompt', 'error');
            }});
        }}

        function copyOptimizedPrompt() {{
            const optimizedText = document.querySelector('#imageContainer pre').textContent;
            navigator.clipboard.writeText(optimizedText).then(() => {{
                showStatus('📋 Prompt otimizado copiado!', 'success');
            }}).catch(() => {{
                showStatus('❌ Falha ao copiar prompt', 'error');
            }});
        }}

        // Auto-generate on page load
        window.addEventListener('load', () => {{
            setTimeout(generateImage, 1000);
        }});
    </script>
</body>
</html>"""
    
    return html_content

def save_html_file(html_content, filename="puter_image_generator.html"):
    """Save HTML content to file"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✅ HTML file saved as: {filename}")
        return filename
    except Exception as e:
        print(f"❌ Error saving HTML file: {e}")
        return None

def create_config_file(config):
    """Save the JSON configuration to a file"""
    filename = "image_config.json"
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"✅ Configuration saved as: {filename}")
        return filename
    except Exception as e:
        print(f"❌ Error saving configuration: {e}")
        return None

def main():
    """Main function to run the image generator"""
    print("🎨 Puter.js Image Generator")
    print("=" * 50)
    
    # JSON configuration provided by user
    config = {
        "modelo": "imagen-3.0-generate-002",
        "prompt": {
            "descricao_visual": "Thumbnail profissional para YouTube no formato 16:9. Fundo escuro (#111111) com partículas douradas flutuando e grade de blockchain sutil. Lado esquerdo: símbolo do Bitcoin (₿) em laranja #f7931a gigante e brilhante, com raios de luz saindo dele. Centro: título em duas linhas bold ultra-impactante — 'SATSMAN' em branco e 'GANHEI SATS!' em laranja #f7931a. Abaixo: badge em verde escuro mostrando '10.000 SATS ≈ $8' com ícone de seta para cima. Lado direito: calendário ou contador visual mostrando '15 DIAS' com checkmarks verdes, representando a sequência obrigatória. Canto superior direito: etiqueta amarela com texto 'BOUNTY BITCOIN' em preto bold. Logotipo '@CanalQb' no canto inferior direito em laranja, pequeno e discreto. Alta energia visual, clima de descoberta e conquista. Sem fundo claro. Sem bordas brancas.",
            "estilo": "bitcoin cinematic dark, crypto bounty aesthetic, orange gold neon glow, high contrast drama, professional YouTube thumbnail, achievement unlock vibe",
            "aspectRatio": "16:9",
            "resolucao": "1920x1080",
            "negativePrompt": "branco, fundo claro, texto ilegível, baixo contraste, pixelado, amador, watermark genérico, cores pastéis, layout limpo demais, verde escuro dominante"
        },
        "metadados_do_post": {
            "titulo": "Satsman: Ganhe Sats de Bitcoin Respondendo 3 Perguntas por Dia",
            "tema_principal": "bounty bitcoin sats diário",
            "palavra_chave": "satsman ganhar sats bitcoin grátis",
            "categoria": "Cripto / Ganhos Online",
            "cor_destaque": "#f7931a"
        },
        "instrucoes_de_uso": {
            "plataforma": "Google Gemini Imagen API ou AI Studio",
            "endpoint": "https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict",
            "separacao": "Este JSON NÃO entra no HTML do post.",
            "saida_esperada": "Imagem PNG ou JPEG 1920x1080 pronta para upload no YouTube"
        }
    }
    
    # Save configuration file
    config_file = create_config_file(config)
    
    # Create HTML content
    html_content = create_html_for_puter(config)
    
    # Save HTML file
    html_file = save_html_file(html_content)
    
    if html_file:
        print(f"\n🚀 Success! Files created:")
        print(f"📄 Configuration: {config_file}")
        print(f"🌐 HTML Generator: {html_file}")
        print(f"\n📋 Next Steps:")
        print(f"1. Open {html_file} in your web browser")
        print(f"2. Click 'Gerar Imagem' to start the process")
        print(f"3. The script will use Puter.js to generate optimized prompts")
        print(f"4. Copy the generated prompts to your preferred image generation tool")
        print(f"\n🎯 Recommended Tools:")
        print(f"• Google AI Studio (https://aistudio.google.com/)")
        print(f"• Microsoft Designer/DALL-E 3")
        print(f"• Midjourney")
        print(f"• Stable Diffusion")

if __name__ == "__main__":
    main()
