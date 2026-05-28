# 🎨 Gerador de Imagens com JSON Personalizado

Sistema completo para geração de imagens usando APIs gratuitas, configurável via JSON. Ideal para criar thumbnails do YouTube e outras imagens personalizadas.

## 📋 Descrição

Este sistema permite gerar imagens profissionais usando APIs gratuitas como Pollinations AI, com configuração flexível via JSON. Suporta diferentes formatos, estilos e resoluções, com tratamento automático de erros e conversão de aspas.

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

**Estrutura do JSON:**
```json
{
  "modelo": "imagen-3.0-generate-002",
  "prompt": {
    "descricao_visual": "Descrição detalhada da imagem...",
    "estilo": "estilo visual desejado",
    "aspectRatio": "16:9",
    "resolucao": "1920x1080",
    "negativePrompt": "elementos a evitar"
  },
  "metadados_do_post": {
    "titulo": "Título do conteúdo",
    "site": "https://canalqb.com.br"
  }
}
```

### 2. **prompt_generator.html** - Gerador de Prompts Offline
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

### 3. **puter_auth_generator.html** - Gerador com Puter.js Autenticado
Interface web usando Puter.js com autenticação oficial.

**Funcionalidades:**
- Autenticação Puter.js (login ou usuário temporário)
- Geração direta de imagens via `puter.ai.txt2img()`
- Otimização de prompts com IA
- Listagem de modelos disponíveis
- Interface profissional com abas

**Como usar:**
Abra o arquivo `puter_auth_generator.html` em um servidor web local.

### 4. **legacy_puter_generator.py** - Script Legado Puter.js
Versão original do script usando Puter.js (mantido para compatibilidade).

## 📁 Estrutura de Arquivos

```
├── image_generator.py          # Script principal de geração de imagens
├── prompt_generator.html       # Gerador de prompts offline
├── puter_auth_generator.html  # Gerador com Puter.js autenticado
├── legacy_puter_generator.py  # Script legado Puter.js
├── image_config.json          # Configuração JSON de exemplo
├── README.md                  # Este arquivo
└── resultados.html           # Interface web de resultados (gerada automaticamente)
```

## 🔧 Configuração

### Requisitos
- Python 3.7+
- Bibliotecas Python: `requests`, `json`, `urllib`

### Instalação
```bash
# Clone o repositório
git clone https://github.com/canalqb/puter_gerando_imagem.git
cd puter_gerando_imagem

# Instale as dependências (se necessário)
pip install requests
```

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

### 2. Gerar Imagem
```bash
python image_generator.py meu_thumbnail.json
```

### 3. Visualizar Resultado
O script gera automaticamente `resultados.html` com as imagens geradas.

## 🎯 Casos de Uso

- **Thumbnails do YouTube:** Gerar thumbnails profissionais para vídeos
- **Imagens de Marketing:** Criar imagens para posts e anúncios
- **Arte Generativa:** Explorar diferentes estilos e prompts
- **Prototipagem Rápida:** Testar conceitos visuais rapidamente

## 🔒 Segurança

- As APIs usadas são gratuitas e não requerem chaves de API
- O script não armazena dados sensíveis
- Configurações JSON são locais e personalizáveis

## 🌐 APIs Suportadas

- **Pollinations AI:** API gratuita e confiável para geração de imagens
- **Hugging Face:** (Opcional) Modelos de Stable Diffusion
- **Puter.js:** (Opcional) Interface via Puter.js

## 📊 Tratamento de Erros

O script inclui tratamento robusto de erros:
- **Erro 402:** Tentativa automática com método alternativo
- **Timeout:** Ajuste automático de tempo de espera
- **Aspas Curvas:** Conversão automática para aspas retas
- **JSON Inválido:** Mensagens detalhadas de erro com localização

## 🤝 Contribuição

Este projeto é mantido pelo CanalQb - https://canalqb.com.br

Sugestões e melhorias são bem-vindas!

## 📄 Licença

Este projeto é open source e disponível para uso livre.

## 📞 Suporte

Para dúvidas e suporte, visite: https://canalqb.com.br

---

**Desenvolvido para:** CanalQb.com.br  
**Versão:** 1.0.0  
**Última atualização:** 2026
