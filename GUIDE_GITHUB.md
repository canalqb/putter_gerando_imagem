# 📋 Guia para Upload no GitHub

## 🚀 Passo 1: Criar o Repositório no GitHub

1. Acesse https://github.com/new
2. Nome do repositório: `puter_gerando_imagem`
3. Descrição: Sistema de gerador de imagens com JSON personalizado - CanalQb
4. Marque como **Público** ou **Privado** (sua preferência)
5. **NÃO** marque "Initialize this repository with a README" (já temos um)
6. Clique em "Create repository"

## 🔑 Passo 2: Criar Deploy Key para Acesso

### Opção A: Usar Personal Access Token (Recomendado)

1. Acesse https://github.com/settings/tokens
2. Clique em "Generate new token" → "Generate new token (classic)"
3. Nome: `CanalQb Image Generator`
4. Selecione as permissões:
   - ✅ `repo` (controle total sobre repositórios privados)
   - ✅ `workflow` (para GitHub Actions se necessário)
5. Clique em "Generate token"
6. **COPIE O TOKEN** (só aparece uma vez!)

### Opção B: Usar SSH Key

1. No seu computador, gere uma chave SSH:
```bash
ssh-keygen -t ed25519 -C "canalqb@deploy-key"
```

2. Adicione a chave SSH ao GitHub:
   - Acesse https://github.com/settings/keys
   - Clique em "New SSH key"
   - Cole o conteúdo de `~/.ssh/id_ed25519.pub`
   - Dê um nome: `CanalQb Deploy Key`

## 📤 Passo 3: Fazer Upload

### Se estiver usando Personal Access Token:

```bash
cd c:/Users/Qb/Desktop/q
git remote set-url origin https://SEU_TOKEN@github.com/canalqb/puter_gerando_imagem.git
git push -u origin master
```

### Se estiver usando SSH:

```bash
cd c:/Users/Qb/Desktop/q
git remote set-url origin git@github.com:canalqb/puter_gerando_imagem.git
git push -u origin master
```

## ✅ Passo 4: Verificar

1. Acesse https://github.com/canalqb/puter_gerando_imagem
2. Verifique se todos os arquivos estão lá
3. O README.md deve aparecer na página principal

## 🔧 Solução de Problemas

### Erro: "Repository not found"
- O repositório não foi criado no GitHub
- Verifique se o nome está correto: `puter_gerando_imagem`

### Erro: "Permission denied"
- O token não tem permissões suficientes
- Verifique se o token tem permissão `repo`

### Erro: "Authentication failed"
- Token inválido ou expirado
- Gere um novo token

## 📝 Resumo dos Arquivos

Após o upload, o repositório conterá:
- `image_generator.py` - Script principal
- `prompt_generator.html` - Gerador offline
- `puter_auth_generator.html` - Gerador com Puter.js
- `legacy_puter_generator.py` - Script legado
- `image_config.json` - Configuração de exemplo
- `README.md` - Documentação completa

---

**Pronto!** Após seguir estes passos, seu sistema estará disponível no GitHub.
