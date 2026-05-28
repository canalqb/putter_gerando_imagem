# 🎨 CanalQb Image Generator - Sistema Completo

Sistema completo para geração de imagens usando APIs gratuitas, configurável via JSON e Webhook API. Ideal para criar thumbnails do YouTube e outras imagens personalizadas.

## 📋 Descrição

Este sistema permite gerar imagens profissionais usando APIs gratuitas como Pollinations AI, com múltiplas formas de interação:
- **Script Python** para uso via terminal
- **Interface Web** para uso interativo
- **Webhook API** para integração com outras aplicações
- **Suporte a Puter.js** para recursos avançados

## 🚀 Funcionalidades

### 1. **image_generator.py** - Script Principal
Script Python principal para geração de imagens usando APIs gratuitas.

**Funcionalidades:**
- Leitura de configuração JSON personalizada
- Geração de imagens via Pollinations AI (gratuito)
- Suporte a diferentes resoluções e aspect ratios
- Tratamento automático de erros (402, timeout, etc.)
- Conversão automática de aspas curvas para retas
- Interface interativa no terminal
- Modo automático via linha de comando
- Feedback detalhado durante o processo
- Criação de interface web para visualização

**Como usar:**
```bash
# Modo automático com arquivo JSON
python image_generator.py image_config.json

# Modo interativo
python image_generator.py
```

### 2. **webhook_server.py** - API Webhook
Servidor Flask para geração de imagens via API HTTP/Webhook.

**Funcionalidades:**
- Endpoint REST para geração de imagens
- Suporte a requisições POST com JSON
- Rate limiting configurável
- Verificação de assinatura de webhook (opcional)
- Download de imagens geradas
- Health check endpoint
- Configuração via YAML

**Como usar:**
```bash
# Instalar dependências
pip install -r requirements.txt

# Configurar secret (opcional)
export WEBHOOK_SECRET=sua-chave-secreta

# Iniciar servidor
python webhook_server.py
```

**Endpoint:** `POST http://localhost:5000/webhook/generate`

### 3. **prompt_generator.html** - Gerador de Prompts Offline
Interface web offline para geração e otimização de prompts.

**Funcionalidades:**
- Geração de prompts otimizados para DALL-E 3, Midjourney
- Múltiplas variações de prompts
- Interface intuitiva com abas
- Links diretos para ferramentas de geração
- Funciona sem conexão com APIs externas
- Copiar prompts com um clique

**Como usar:**
Abra o arquivo `prompt_generator.html` diretamente no navegador.

### 4. **puter_auth_generator.html** - Gerador com Puter.js Autenticado
Interface web usando Puter.js com autenticação oficial.

**Funcionalidades:**
- Autenticação Puter.js (login ou usuário temporário)
- Geração direta de imagens via `puter.ai.txt2img()`
- Otimização de prompts com IA
- Listagem de modelos disponíveis
- Interface profissional com abas

**Como usar:**
Abra o arquivo `puter_auth_generator.html` em um servidor web local.

### 5. **legacy_puter_generator.py** - Script Legado Puter.js
Versão original do script usando Puter.js (mantido para compatibilidade).

## 📁 Estrutura de Arquivos

```
├── image_generator.py          # Script principal de geração de imagens
├── webhook_server.py           # Servidor API Webhook
├── config.yml                  # Configuração do servidor webhook
├── requirements.txt            # Dependências Python para webhook
├── prompt_generator.html       # Gerador de prompts offline
├── puter_auth_generator.html  # Gerador com Puter.js autenticado
├── legacy_puter_generator.py  # Script legado Puter.js
├── image_config.json          # Configuração JSON de exemplo
├── README.md                  # Este arquivo
├── WEBHOOK_EXAMPLES.md        # Exemplos de uso da API Webhook
├── DEPLOY_KEY_INSTRUCTIONS.md # Instruções para Deploy Key
└── resultados.html           # Interface web de resultados (gerada automaticamente)
```

## 🔧 Configuração

### Requisitos para Script Principal
- Python 3.7+
- Bibliotecas Python: `requests`, `json`, `urllib`

### Requisitos para Webhook Server
- Python 3.7+
- Bibliotecas: `flask`, `pyyaml`, `requests`
- Veja `requirements.txt`

### Instalação
```bash
# Clone o repositório
git clone https://github.com/canalqb/puter_gerando_imagem.git
cd puter_gerando_imagem

# Para usar o script principal
pip install requests

# Para usar o webhook server
pip install -r requirements.txt
```

## 🔐 Segurança e Secrets

### Secrets do GitHub (Obrigatório para Forks)

Ao fazer fork deste repositório, você deve configurar os seguintes secrets nas configurações do seu repositório:

**Secrets Necessários:**

1. **`WEBHOOK_SECRET`**
   - **Descrição:** Chave secreta para proteger o webhook
   - **Valor:** Gerar uma string aleatória segura (mínimo 32 caracteres)
   - **Como gerar:** Use `python -c "import secrets; print(secrets.token_urlsafe(32))"`

2. **`PUTER_AUTH_TOKEN`** (Opcional, se usar Puter.js)
   - **Descrição:** Token de autenticação do Puter.js
   - **Valor:** Seu token do Puter.js
   - **Como obter:** Veja seção "Puter.js" abaixo

### Como Configurar Secrets no GitHub:

1. Acesse seu repositório no GitHub
2. Vá em **Settings** → **Secrets and variables** → **Actions**
3. Clique em **New repository secret**
4. Adicione cada secret com o nome e valor correspondente
5. Clique em **Add secret**

### Segurança dos Scripts

**Nenhum script exporta ou expõe:**
- Chaves de API
- Tokens de autenticação
- Dados sensíveis
- Informações de usuários

Todos os dados sensíveis são carregados via:
- Variáveis de ambiente
- Arquivos de configuração locais
- Secrets do GitHub

## 🌐 Puter.js - Autenticação

### Como Criar Conta no Puter

1. Acesse: https://puter.com/
2. Clique em **"Sign Up"** ou **"Create Account"**
3. Preencha com seu email e senha
4. Confirme seu email
5. Pronto! Sua conta está criada

### Como Obter Token de Autenticação

1. Faça login em https://puter.com/
2. Acesse as configurações da sua conta
3. Vá em **"API Keys"** ou **"Developer Settings"**
4. Clique em **"Generate New Key"**
5. Dê um nome para sua chave (ex: "Image Generator")
6. Copie o token gerado
7. Adicione ao secret `PUTER_AUTH_TOKEN` no GitHub

### Documentação Oficial

- **Site:** https://puter.com/
- **Documentação:** https://developer.puter.com/
- **Tutoriais:** https://developer.puter.com/tutorials/

### Por que Usar Puter.js?

- **Gratuito:** Sem custos para uso básico
- **Sem Chaves de API:** Autenticação simplificada
- **Modelos Avançados:** Acesso a Gemini, DALL-E, e outros
- **User-Pays:** Usuários pagam pelo próprio uso
- **Servidorless:** Sem necessidade de infraestrutura

## 📝 Exemplo de Uso

### 1. Criar Configuração JSON
Crie um arquivo `meu_thumbnail.json`:
```json
{
  "modelo": "imagen-3.0-generate-002",
  "prompt": {
    "descricao_visual": "Thumbnail profissional para YouTube...",
    "estilo": "clean tech, professional",
    "aspectRatio": "16:9",
    "resolucao": "1920x1080",
    "negativePrompt": "fundo escuro, baixo contraste"
  },
  "metadados_do_post": {
    "titulo": "Meu Vídeo",
    "site": "https://canalqb.com.br"
  }
}
```

### 2. Gerar Imagem via Script
```bash
python image_generator.py meu_thumbnail.json
```

### 3. Usar Webhook API
```bash
# Iniciar servidor
python webhook_server.py

# Em outro terminal, fazer requisição
curl -X POST http://localhost:5000/webhook/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Thumbnail profissional para YouTube"}'
```

### 4. Visualizar Resultado
O script gera automaticamente `resultados.html` com as imagens geradas.

## 🎯 Casos de Uso

- **Thumbnails do YouTube:** Gerar thumbnails profissionais para vídeos
- **Imagens de Marketing:** Criar imagens para posts e anúncios
- **Arte Generativa:** Explorar diferentes estilos e prompts
- **Prototipagem Rápida:** Testar conceitos visuais rapidamente
- **Integração com Apps:** Usar webhook para integrar com outras aplicações

## 🌐 APIs Suportadas

- **Pollinations AI:** API gratuita e confiável para geração de imagens
- **Hugging Face:** (Opcional) Modelos de Stable Diffusion
- **Puter.js:** (Opcional) Interface via Puter.js com Gemini, DALL-E, etc.

## 📊 Tratamento de Erros

O script inclui tratamento robusto de erros:
- **Erro 402:** Tentativa automática com método alternativo
- **Timeout:** Ajuste automático de tempo de espera
- **Aspas Curvas:** Conversão automática para aspas retas
- **JSON Inválido:** Mensagens detalhadas de erro com localização
- **Rate Limiting:** Proteção contra abuso

## 📡 Webhook API

Para documentação completa da API Webhook, veja: **WEBHOOK_EXAMPLES.md**

Inclui exemplos em:
- JavaScript / Node.js
- Python
- PHP
- Ruby
- Go
- cURL

## 🤝 Contribuição e Forks

### Como Contribuir

1. Faça fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

### Após Fazer Fork

Ao fazer fork deste repositório:

1. **Configure os Secrets** obrigatórios (veja seção "Segurança e Secrets")
2. **Atualize as URLs** se necessário
3. **Teste localmente** antes de usar em produção
4. **Revise a configuração** em `config.yml`

### Diretrizes de Contribuição

- Mantenha o código limpo e bem documentado
- Não exponha dados sensíveis
- Siga o estilo de código existente
- Adicione testes para novas funcionalidades
- Atualize a documentação conforme necessário

## 🔒 Segurança

- As APIs usadas são gratuitas e não requerem chaves de API
- O script não armazena dados sensíveis
- Configurações JSON são locais e personalizáveis
- Secrets são gerenciados via GitHub Secrets
- Rate limiting protege contra abuso

## 📄 Licença

Este projeto é open source e disponível para uso livre.

## 📞 Suporte

- **Site:** https://canalqb.com.br
- **Documentação:** README.md, WEBHOOK_EXAMPLES.md
- **Issues:** GitHub Issues

---

**Desenvolvido para:** CanalQb.com.br  
**Versão:** 2.0.0  
**Última atualização:** 2026
