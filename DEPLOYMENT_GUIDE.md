# 🚀 Guia de Deployment - Training App

## 📋 Pré-requisitos

### Servidor de Produção
- **CPU**: 2+ cores
- **RAM**: 4GB+ recomendado
- **Storage**: 20GB+ SSD
- **OS**: Ubuntu 20.04+ / CentOS 7+ / Debian 10+

### Software Necessário
- Docker Engine (20.10+)
- Docker Compose (2.0+)
- Git
- SSL Certificate (recomendado)

## 🔧 Preparação do Ambiente

### 1. Instalação do Docker
```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.12.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. Configuração do Firewall
```bash
# Ubuntu/Debian com UFW
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable

# CentOS/RHEL com firewalld
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

## 🏭 Deployment para Produção

### 1. Clone do Repositório
```bash
cd /opt
sudo git clone https://github.com/seuusuario/TrabalhoTPPE.git
cd TrabalhoTPPE
sudo chown -R $USER:$USER .
```

### 2. Configuração de Variáveis de Ambiente
```bash
# Criar arquivo .env para produção
cp .env.example .env.prod

# Editar com valores seguros
nano .env.prod
```

**Exemplo de .env.prod:**
```env
# Database
POSTGRES_USER=treinapp_user
POSTGRES_PASSWORD=SuaSenhaSegura123!@#
POSTGRES_DB=treinapp_prod

# API Security
SECRET_KEY=sua-chave-secreta-de-pelo-menos-32-caracteres-aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Environment
ENVIRONMENT=production
DEBUG=false

# CORS (adicionar seus domínios)
CORS_ORIGINS=["https://yourdomain.com","https://www.yourdomain.com"]

# Database URL
DATABASE_URL=postgresql://treinapp_user:SuaSenhaSegura123!@#@db:5432/treinapp_prod
```

### 3. Deploy com Docker Compose
```bash
# Fazer backup de dados existentes (se houver)
docker-compose -f docker-compose.prod.yml exec db pg_dump -U $POSTGRES_USER $POSTGRES_DB > backup-$(date +%Y%m%d).sql

# Subir em produção
docker-compose -f docker-compose.prod.yml up -d --build

# Verificar status
docker-compose -f docker-compose.prod.yml ps
```

## 🔒 Configuração SSL/HTTPS

### 1. Usando Let's Encrypt (Recomendado)
```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx

# Obter certificado
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Configurar renovação automática
sudo crontab -e
# Adicionar linha:
0 12 * * * /usr/bin/certbot renew --quiet
```

### 2. Configuração Manual SSL
```bash
# Criar diretório para certificados
mkdir -p nginx/ssl

# Copiar certificados
cp /path/to/your/cert.pem nginx/ssl/
cp /path/to/your/key.pem nginx/ssl/

# Configurar permissões
chmod 400 nginx/ssl/key.pem
chmod 644 nginx/ssl/cert.pem

# Subir com SSL
docker-compose -f docker-compose.prod.yml --profile ssl up -d
```

## 📊 Monitoramento e Logs

### 1. Logs da Aplicação
```bash
# Ver logs em tempo real
docker-compose -f docker-compose.prod.yml logs -f

# Logs específicos
docker-compose -f docker-compose.prod.yml logs frontend
docker-compose -f docker-compose.prod.yml logs backend
docker-compose -f docker-compose.prod.yml logs db

# Salvar logs
docker-compose -f docker-compose.prod.yml logs > app-logs-$(date +%Y%m%d).log
```

### 2. Monitoramento de Saúde
```bash
# Health checks
curl -f http://localhost/health
curl -f http://localhost:8000/health

# Status dos containers
docker-compose -f docker-compose.prod.yml ps

# Uso de recursos
docker stats
```

## 🔄 Backup e Restauração

### 1. Backup do Banco de Dados
```bash
# Backup automático
docker-compose -f docker-compose.prod.yml exec db pg_dump -U $POSTGRES_USER $POSTGRES_DB | gzip > backup-$(date +%Y%m%d-%H%M%S).sql.gz

# Script de backup automático
cat > backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/opt/backups"
mkdir -p $BACKUP_DIR
cd /opt/TrabalhoTPPE
docker-compose -f docker-compose.prod.yml exec db pg_dump -U $POSTGRES_USER $POSTGRES_DB | gzip > $BACKUP_DIR/backup-$(date +%Y%m%d-%H%M%S).sql.gz
# Manter apenas 7 dias de backup
find $BACKUP_DIR -name "backup-*.sql.gz" -mtime +7 -delete
EOF

chmod +x backup.sh

# Adicionar ao cron
crontab -e
# Adicionar: 0 2 * * * /opt/TrabalhoTPPE/backup.sh
```

### 2. Restauração
```bash
# Restaurar backup
gunzip -c backup-20231220-020000.sql.gz | docker-compose -f docker-compose.prod.yml exec -T db psql -U $POSTGRES_USER -d $POSTGRES_DB
```

## 🚀 Atualizações e Manutenção

### 1. Atualizações de Código
```bash
# Parar aplicação
docker-compose -f docker-compose.prod.yml down

# Atualizar código
git pull origin main

# Rebuild e restart
docker-compose -f docker-compose.prod.yml up -d --build

# Verificar saúde
docker-compose -f docker-compose.prod.yml ps
```

### 2. Rolling Updates (Zero Downtime)
```bash
# Atualizar apenas backend
docker-compose -f docker-compose.prod.yml up -d --no-deps --build backend

# Atualizar apenas frontend
docker-compose -f docker-compose.prod.yml up -d --no-deps --build frontend
```

## 🛡️ Segurança em Produção

### 1. Configurações Recomendadas
- **Firewall**: Apenas portas 80, 443, 22 abertas
- **SSL**: HTTPS obrigatório
- **Secrets**: Nunca commitar senhas no código
- **Updates**: Manter sistema atualizado
- **Backups**: Backup automático diário

### 2. Hardening do Servidor
```bash
# Desabilitar login root via SSH
sudo sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config

# Configurar fail2ban
sudo apt install fail2ban
sudo systemctl enable fail2ban

# Atualizar sistema
sudo apt update && sudo apt upgrade -y
```

## 📈 Escalabilidade

### 1. Múltiplos Workers
```bash
# Editar docker-compose.prod.yml
# Aumentar workers do backend:
command: ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "8"]
```

### 2. Load Balancer
```bash
# Usar nginx como load balancer
# Adicionar múltiplas instâncias do backend
# Configurar nginx upstream
```

## 🆘 Troubleshooting

### Problemas Comuns

1. **Aplicação não inicia**
   ```bash
   # Verificar logs
   docker-compose -f docker-compose.prod.yml logs
   
   # Verificar configurações
   docker-compose -f docker-compose.prod.yml config
   ```

2. **Banco de dados não conecta**
   ```bash
   # Verificar se o banco está rodando
   docker-compose -f docker-compose.prod.yml exec db psql -U $POSTGRES_USER -d $POSTGRES_DB -c "SELECT 1;"
   ```

3. **SSL não funciona**
   ```bash
   # Verificar certificados
   openssl x509 -in nginx/ssl/cert.pem -text -noout
   
   # Testar nginx config
   docker-compose -f docker-compose.prod.yml exec nginx nginx -t
   ```

## 📞 Suporte e Contato

Para suporte técnico:
- **Issues**: GitHub Issues
- **Documentação**: README.md
- **Logs**: Sempre incluir logs completos

---

## ✅ Checklist de Deployment

- [ ] Servidor configurado (Docker, firewall, SSL)
- [ ] Arquivo .env.prod configurado com secrets seguros
- [ ] Domínio apontando para o servidor
- [ ] SSL configurado (Let's Encrypt ou manual)
- [ ] Backup automático configurado
- [ ] Logs e monitoramento configurados
- [ ] Testes de saúde funcionando
- [ ] Documentação atualizada

**🎉 Parabéns! Sua aplicação está pronta para produção!** 