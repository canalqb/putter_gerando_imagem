# 📡 Webhook API - Exemplos de Uso

Documentação completa de como usar a API Webhook do CanalQb Image Generator.

## 🔗 Endpoint Webhook

**URL:** `http://seu-servidor:5000/webhook/generate`
**Método:** `POST`
**Content-Type:** `application/json`

## 📝 Estrutura do Request

```json
{
  "prompt": "Descrição da imagem que deseja gerar",
  "width": 1920,
  "height": 1080
}
```

**Parâmetros:**
- `prompt` (obrigatório): Descrição da imagem
- `width` (opcional): Largura da imagem (padrão: 1920)
- `height` (opcional): Altura da imagem (padrão: 1080)

## 📤 Estrutura da Response

```json
{
  "success": true,
  "filename": "webhook_20260528_183424.png",
  "message": "Image generated successfully",
  "timestamp": "2026-05-28T18:34:24"
}
```

## 💻 Exemplos por Linguagem

### JavaScript / Node.js

```javascript
// Exemplo com fetch
async function generateImage(prompt) {
  const response = await fetch('http://localhost:5000/webhook/generate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Webhook-Secret': 'sua-secret-key' // opcional
    },
    body: JSON.stringify({
      prompt: prompt,
      width: 1920,
      height: 1080
    })
  });
  
  const data = await response.json();
  
  if (data.success) {
    // Baixar a imagem
    const imageUrl = `http://localhost:5000/webhook/image/${data.filename}`;
    window.open(imageUrl, '_blank');
  }
  
  return data;
}

// Usar
generateImage('Thumbnail profissional para YouTube sobre Python');
```

### Python

```python
import requests
import json

def generate_image(prompt, webhook_url='http://localhost:5000/webhook/generate'):
    """Gerar imagem via webhook"""
    
    payload = {
        'prompt': prompt,
        'width': 1920,
        'height': 1080
    }
    
    headers = {
        'Content-Type': 'application/json',
        'X-Webhook-Secret': 'sua-secret-key'  # opcional
    }
    
    try:
        response = requests.post(webhook_url, json=payload, headers=headers)
        data = response.json()
        
        if data.get('success'):
            # Baixar a imagem
            image_url = f"http://localhost:5000/webhook/image/{data['filename']}"
            img_response = requests.get(image_url)
            
            # Salvar imagem
            with open(data['filename'], 'wb') as f:
                f.write(img_response.content)
            
            print(f"✅ Imagem salva: {data['filename']}")
            return data['filename']
        else:
            print(f"❌ Erro: {data.get('message')}")
            return None
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return None

# Usar
generate_image('Thumbnail profissional para YouTube sobre Python')
```

### cURL

```bash
curl -X POST http://localhost:5000/webhook/generate \
  -H "Content-Type: application/json" \
  -H "X-Webhook-Secret: sua-secret-key" \
  -d '{
    "prompt": "Thumbnail profissional para YouTube sobre Python",
    "width": 1920,
    "height": 1080
  }'
```

### PHP

```php
<?php
function generateImage($prompt) {
    $url = 'http://localhost:5000/webhook/generate';
    
    $data = array(
        'prompt' => $prompt,
        'width' => 1920,
        'height' => 1080
    );
    
    $options = array(
        'http' => array(
            'header'  => "Content-Type: application/json\r\n" .
                        "X-Webhook-Secret: sua-secret-key\r\n",
            'method'  => 'POST',
            'content' => json_encode($data)
        )
    );
    
    $context  = stream_context_create($options);
    $result = file_get_contents($url, false, $context);
    $response = json_decode($result, true);
    
    if ($response['success']) {
        $imageUrl = "http://localhost:5000/webhook/image/" . $response['filename'];
        echo "✅ Imagem gerada: " . $response['filename'];
        return $response['filename'];
    }
    
    return null;
}

// Usar
generateImage('Thumbnail profissional para YouTube sobre Python');
?>
```

### Ruby

```ruby
require 'net/http'
require 'json'
require 'uri'

def generate_image(prompt)
  uri = URI('http://localhost:5000/webhook/generate')
  
  header = {
    'Content-Type' => 'application/json',
    'X-Webhook-Secret' => 'sua-secret-key'
  }
  
  body = {
    prompt: prompt,
    width: 1920,
    height: 1080
  }.to_json
  
  request = Net::HTTP::Post.new(uri, header)
  request.body = body
  
  response = Net::HTTP.start(uri.hostname, uri.port) do |http|
    http.request(request)
  end
  
  data = JSON.parse(response.body)
  
  if data['success']
    puts "✅ Imagem gerada: #{data['filename']}"
    return data['filename']
  else
    puts "❌ Erro: #{data['message']}"
    return nil
  end
end

# Usar
generate_image('Thumbnail profissional para YouTube sobre Python')
```

### Go

```go
package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "io"
    "net/http"
)

type Request struct {
    Prompt string `json:"prompt"`
    Width  int    `json:"width"`
    Height int    `json:"height"`
}

type Response struct {
    Success  bool   `json:"success"`
    Filename string `json:"filename"`
    Message string `json:"message"`
}

func generateImage(prompt string) (*Response, error) {
    url := "http://localhost:5000/webhook/generate"
    
    payload := Request{
        Prompt: prompt,
        Width:  1920,
        Height: 1080,
    }
    
    jsonData, _ := json.Marshal(payload)
    
    req, _ := http.NewRequest("POST", url, bytes.NewBuffer(jsonData))
    req.Header.Set("Content-Type", "application/json")
    req.Header.Set("X-Webhook-Secret", "sua-secret-key")
    
    client := &http.Client{}
    resp, err := client.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()
    
    body, _ := io.ReadAll(resp.Body)
    
    var result Response
    json.Unmarshal(body, &result)
    
    if result.Success {
        fmt.Printf("✅ Imagem gerada: %s\n", result.Filename)
    }
    
    return &result, nil
}

func main() {
    generateImage("Thumbnail profissional para YouTube sobre Python")
}
```

## 🔐 Segurança

### Webhook Secret (Opcional)

Para proteger seu webhook, configure uma secret key:

```bash
export WEBHOOK_SECRET=sua-chave-secreta-aqui
python webhook_server.py
```

E inclua no header:
```
X-Webhook-Secret: sua-chave-secreta-aqui
```

### Rate Limiting

O servidor possui rate limiting configurável:
- Padrão: 10 requisições por minuto
- Padrão: 100 requisições por hora

Configure em `config.yml`:
```yaml
security:
  rate_limit:
    enabled: true
    requests_per_minute: 10
    requests_per_hour: 100
```

## 📥 Baixar Imagem Gerada

Após receber o filename, baixe a imagem:

**URL:** `http://localhost:5000/webhook/image/{filename}`

### Exemplo em JavaScript:
```javascript
const imageUrl = `http://localhost:5000/webhook/image/${data.filename}`;
// Abrir em nova aba
window.open(imageUrl, '_blank');

// Ou baixar programaticamente
const link = document.createElement('a');
link.href = imageUrl;
link.download = data.filename;
link.click();
```

### Exemplo em Python:
```python
image_url = f"http://localhost:5000/webhook/image/{filename}"
response = requests.get(image_url)

with open(filename, 'wb') as f:
    f.write(response.content)
```

## 🧪 Testar Webhook

### Health Check
```bash
curl http://localhost:5000/health
```

### Teste Simples
```bash
curl -X POST http://localhost:5000/webhook/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Teste de imagem"}'
```

## 🚀 Deploy

### Usando Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "webhook_server.py"]
```

### Usando systemd (Linux)
```ini
[Unit]
Description=CanalQb Image Generator Webhook
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/app
Environment="WEBHOOK_SECRET=sua-secret"
ExecStart=/usr/bin/python3 /path/to/app/webhook_server.py
Restart=always

[Install]
WantedBy=multi-user.target
```

## 📚 Mais Informações

- Documentação completa: README.md
- Configuração: config.yml
- Exemplos de JSON: image_config.json
