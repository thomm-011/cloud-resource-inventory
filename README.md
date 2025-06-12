Cloud Resource Inventory

Uma ferramenta completa para inventariar e comparar recursos em múltiplas clouds (AWS, Azure, GCP).
🎯 Funcionalidades

    Inventário Automático: Coleta recursos de múltiplas contas/subscriptions
    Exportação Flexível: Relatórios em Excel, CSV, e JSON
    Comparação de Custos: Análise de preços entre providers
    Dashboard Web: Interface visual para análise
    Alertas: Notificações sobre recursos órfãos ou subutilizados

📁 Estrutura do Projeto

cloud-resource-inventory/
├── src/
│   ├── aws/
│   │   ├── inventory.py
│   │   ├── cost_analyzer.py
│   │   └── config.py
│   ├── azure/
│   │   ├── inventory.py
│   │   ├── cost_analyzer.py
│   │   └── config.py
│   ├── gcp/
│   │   ├── inventory.py
│   │   ├── cost_analyzer.py
│   │   └── config.py
│   ├── exporters/
│   │   ├── excel_exporter.py
│   │   ├── csv_exporter.py
│   │   └── json_exporter.py
│   └── dashboard/
│       ├── app.py
│       ├── templates/
│       └── static/
├── config/
│   ├── aws_accounts.json
│   ├── azure_subscriptions.json
│   └── gcp_projects.json
├── reports/
├── scripts/
│   ├── run_inventory.sh
│   └── schedule_reports.py
├── requirements.txt
├── docker-compose.yml
└── README.md

🚀 Quick Start
Instalação

bash

git clone https://github.com/seu-usuario/cloud-resource-inventory.git
cd cloud-resource-inventory
pip install -r requirements.txt

Configuração

    AWS: Configure credenciais via AWS CLI ou variáveis de ambiente
    Azure: az login ou service principal
    GCP: Configure service account key

Uso Básico

bash

# Inventário completo de todos os providers
python src/main.py --all

# Apenas AWS
python src/main.py --aws --accounts config/aws_accounts.json

# Exportar para Excel
python src/main.py --aws --export excel --output reports/inventory.xlsx

# Executar dashboard
python src/dashboard/app.py

📊 Tipos de Recursos Suportados
AWS

    EC2 (Instances, Volumes, AMIs)
    S3 (Buckets, Objects)
    RDS (Instances, Snapshots)
    VPC (Subnets, Security Groups)
    Lambda Functions
    Load Balancers
    CloudFormation Stacks

Azure

    Virtual Machines
    Storage Accounts
    SQL Databases
    Resource Groups
    Virtual Networks
    App Services

GCP

    Compute Engine
    Cloud Storage
    Cloud SQL
    VPC Networks
    Cloud Functions

💰 Análise de Custos

bash

# Comparar custos entre providers
python src/cost_comparison.py --resource-type vm --region us-east-1

# Relatório de recursos órfãos
python src/orphan_resources.py --all-providers

# Sugestões de otimização
python src/cost_optimizer.py --provider aws

📈 Dashboard Web

Acesse http://localhost:5000 após executar o dashboard para:

    Visualizar inventário em tempo real
    Gráficos de distribuição de recursos
    Comparação de custos por provider
    Histórico de mudanças

🐳 Docker

bash

# Executar com Docker
docker-compose up -d

# Executar inventário via container
docker run -v $(pwd)/config:/app/config cloud-inventory:latest --all

📋 Exemplos de Uso
Cenário 1: Auditoria Mensal

bash

# Script automatizado para auditoria
./scripts/monthly_audit.sh

Cenário 2: Migração Cloud

bash

# Inventário detalhado para planejamento
python src/migration_planner.py --source aws --target azure

Cenário 3: Compliance

bash

# Verificar recursos sem tags obrigatórias
python src/compliance_checker.py --check-tags

🔧 Configuração Avançada
Filtros Personalizados

json

{
  "aws": {
    "regions": ["us-east-1", "us-west-2"],
    "resource_types": ["ec2", "s3", "rds"],
    "tags": {
      "Environment": ["prod", "staging"]
    }
  }
}

Alertas

yaml

alerts:
  - type: "orphaned_resources"
    threshold: 5
    notification: "slack"
  - type: "cost_spike"
    threshold: 20%
    notification: "email"

📊 Relatórios Disponíveis

    Inventário Completo: Lista todos os recursos
    Análise de Custos: Comparação entre providers
    Recursos Órfãos: Recursos sem uso aparente
    Compliance: Verificação de políticas
    Tendências: Evolução do ambiente ao longo do tempo

🤝 Contribuição

    Fork o repositório
    Crie uma branch para sua feature
    Commit suas mudanças
    Push para a branch
    Abra um Pull Request

📝 Roadmap

    Suporte para Oracle Cloud
    Integração com CMDB
    Machine Learning para previsão de custos
    API REST
    Mobile app
    Integração com Terraform

📄 Licença

MIT License - veja LICENSE para detalhes.
🆘 Suporte

    📧 Email: seu-email@exemplo.com
    💬 Issues: GitHub Issues
    📖 Wiki: Documentação Completa

