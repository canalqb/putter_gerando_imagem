#!/usr/bin/env python3
"""
Servidor Webhook para Geração de Imagens
CanalQb Image Generator - API via Webhook
"""

import os
import json
import yaml
import base64
import requests
import urllib.parse
from datetime import datetime
from flask import Flask, request, jsonify, send_file
from functools import wraps
import hashlib
import hmac

app = Flask(__name__)

# Carregar configuração
def load_config():
    config_file = os.path.join(os.path.dirname(__file__), 'config.yml')
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        # Configuração padrão se arquivo não existir
        return {
            'server': {'host': '0.0.0.0', 'port': 5000, 'debug': False},
            'generation': {
                'default_width': 1920,
                'default_height': 1080,
                'timeout': 120,
                'apis': {
                    'pollinations': {
                        'enabled': True,
                        'url': 'https://image.pollinations.ai/prompt',
                        'model': 'flux'
                    }
                }
            },
            'security': {
                'webhook_secret': os.getenv('WEBHOOK_SECRET', 'default_secret_change_me'),
                'rate_limit': {'enabled': True, 'requests_per_minute': 10}
            },
            'storage': {'output_dir': 'generated_images'}
        }

config = load_config()

# Criar diretório de saída
os.makedirs(config['storage']['output_dir'], exist_ok=True)

# Rate limiting simples
rate_limits = {}

def check_rate_limit(ip):
    """Verificar rate limiting"""
    if not config['security']['rate_limit']['enabled']:
        return True
    
    now = datetime.now()
    minute_key = f"{ip}_{now.strftime('%Y%m%d%H%M')}"
    hour_key = f"{ip}_{now.strftime('%Y%m%d%H')}"
    
    if minute_key not in rate_limits:
        rate_limits[minute_key] = 0
    if hour_key not in rate_limits:
        rate_limits[hour_key] = 0
    
    rate_limits[minute_key] += 1
    rate_limits[hour_key] += 1
    
    rpm = config['security']['rate_limit']['requests_per_minute']
    rph = config['security']['rate_limit'].get('requests_per_hour', 100)
    
    if rate_limits[minute_key] > rpm or rate_limits[hour_key] > rph:
        return False
    
    return True

def verify_webhook_signature(data, signature, secret):
    """Verificar assinatura do webhook"""
    if not signature:
        return False
    
    expected_signature = hmac.new(
        secret.encode(),
        json.dumps(data, sort_keys=True).encode(),
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(expected_signature, signature)

def generate_image(prompt, width=1920, height=1080):
    """Gerar imagem usando Pollinations AI"""
    try:
        encoded_prompt = urllib.parse.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        
        params = {
            'width': width,
            'height': height,
            'seed': datetime.now().timestamp(),
            'nologo': 'true',
            'model': 'flux'
        }
        
        response = requests.get(url, params=params, timeout=120, stream=True)
        
        if response.status_code == 200:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"webhook_{timestamp}.png"
            filepath = os.path.join(config['storage']['output_dir'], filename)
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            return filename, filepath
        else:
            return None, None
            
    except Exception as e:
        print(f"Erro ao gerar imagem: {e}")
        return None, None

@app.route('/webhook/generate', methods=['POST'])
def webhook_generate():
    """Endpoint webhook para geração de imagens"""
    
    # Verificar rate limit
    client_ip = request.remote_addr
    if not check_rate_limit(client_ip):
        return jsonify({
            'error': 'Rate limit exceeded',
            'message': 'Too many requests. Please try again later.'
        }), 429
    
    # Verificar assinatura se configurado
    secret = config['security']['webhook_secret']
    if secret and secret != 'default_secret_change_me':
        signature = request.headers.get('X-Webhook-Signature')
        if not verify_webhook_signature(request.json, signature, secret):
            return jsonify({
                'error': 'Invalid signature',
                'message': 'Webhook signature verification failed.'
            }), 401
    
    # Obter dados do webhook
    try:
        data = request.json
        
        # Extrair prompt do JSON
        if 'prompt' in data:
            prompt = data['prompt']
        elif 'descricao_visual' in data:
            prompt = data['descricao_visual']
        else:
            return jsonify({
                'error': 'Missing prompt',
                'message': 'No prompt found in request body.'
            }), 400
        
        # Extrair parâmetros opcionais
        width = data.get('width', config['generation']['default_width'])
        height = data.get('height', config['generation']['default_height'])
        
        # Gerar imagem
        filename, filepath = generate_image(prompt, width, height)
        
        if not filename:
            return jsonify({
                'error': 'Generation failed',
                'message': 'Failed to generate image.'
            }), 500
        
        # Retornar resultado
        return jsonify({
            'success': True,
            'filename': filename,
            'message': 'Image generated successfully',
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal error',
            'message': str(e)
        }), 500

@app.route('/webhook/image/<filename>', methods=['GET'])
def get_image(filename):
    """Endpoint para baixar imagem gerada"""
    try:
        filepath = os.path.join(config['storage']['output_dir'], filename)
        if os.path.exists(filepath):
            return send_file(filepath, mimetype='image/png')
        else:
            return jsonify({
                'error': 'File not found',
                'message': f'Image {filename} not found.'
            }), 404
    except Exception as e:
        return jsonify({
            'error': 'Internal error',
            'message': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Endpoint de health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/', methods=['GET'])
def index():
    """Página inicial"""
    return jsonify({
        'service': 'CanalQb Image Generator Webhook',
        'version': '1.0.0',
        'endpoints': {
            'webhook': '/webhook/generate',
            'download': '/webhook/image/<filename>',
            'health': '/health'
        },
        'documentation': 'README.md'
    })

if __name__ == '__main__':
    # Configurar servidor
    host = config['server']['host']
    port = config['server']['port']
    debug = config['server']['debug']
    
    print(f"🚀 Servidor Webhook iniciado em http://{host}:{port}")
    print(f"📁 Diretório de saída: {config['storage']['output_dir']}")
    print(f"🔐 Webhook Secret: {'Configurado' if config['security']['webhook_secret'] != 'default_secret_change_me' else 'Não configurado (usando padrão)'}")
    
    app.run(host=host, port=port, debug=debug)
