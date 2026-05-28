# 🔑 Deploy Key para Upload Automático

## Chave SSH Gerada

**Chave Pública (adicionar no GitHub):**
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAII7YVkJbJTUp2P2F+rpt09AYWvnABBd/BgSj3UULmfVG cascade@canalqb-deploy
```

## 📋 Passos para Adicionar a Deploy Key

### 1. Criar o Repositório no GitHub
1. Acesse https://github.com/new
2. Nome: `puter_gerando_imagem`
3. Descrição: Sistema de gerador de imagens com JSON personalizado - CanalQb
4. Clique em "Create repository"

### 2. Adicionar a Deploy Key
1. Após criar o repositório, acesse: https://github.com/canalqb/puter_gerando_imagem/settings/keys
2. Clique em "Add deploy key"
3. **Title:** `Cascade Deploy Key`
4. **Key:** Cole a chave pública acima
5. **Marque:** ✅ "Allow write access" (para permitir upload)
6. Clique em "Add deploy key"

### 3. Upload Automático
Após adicionar a chave, execute:
```bash
cd c:/Users/Qb/Desktop/q
git remote set-url origin git@github.com:canalqb/puter_gerando_imagem.git
git push -u origin master
```

## 🔒 Segurança

- A chave privada (`canalqb_deploy_key`) está salva localmente
- A chave pública foi gerada especificamente para este projeto
- Você pode revogar a chave a qualquer momento nas configurações do GitHub
- A chave permite acesso apenas ao repositório `puter_gerando_imagem`

## ✅ Após Upload

O sistema estará disponível em:
https://github.com/canalqb/puter_gerando_imagem

Todos os arquivos serão:
- `image_generator.py` - Script principal
- `prompt_generator.html` - Gerador offline
- `puter_auth_generator.html` - Gerador Puter.js
- `legacy_puter_generator.py` - Script legado
- `image_config.json` - Configuração de exemplo
- `README.md` - Documentação completa
