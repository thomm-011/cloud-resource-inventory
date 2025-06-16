Cloud Resource Inventory 🛠️

Ferramenta simples para inventariar recursos na AWS de forma programática, utilizando Python e o SDK boto3.

✅ Funcionalidades atuais
    Listagem de instâncias EC2

    Listagem de buckets S3

    Exportação de resultados para JSON e CSV

📂 Estrutura do Projeto
cloud-resource-inventory/
├── src/
│   └── aws/
│       ├── inventory.py
│       └── exporters.py
├── reports/
├── requirements.txt
└── README.md

Como Executar
    Pré-requisitos

    Conta AWS com credenciais configuradas (via AWS CLI ou variáveis de ambiente)

    Python 3.x

Instalação

git clone https://github.com/thomm-011/cloud-resource-inventory.git
cd cloud-resource-inventory
pip install -r requirements.txt

Exemplo de Uso

# Listar EC2 e salvar como JSON
python src/aws/inventory.py --resource ec2 --output reports/ec2_inventory.json

# Listar S3 e salvar como CSV
python src/aws/inventory.py --resource s3 --output reports/s3_inventory.csv

📝 Próximos Passos (Roadmap Pessoal)
    Adicionar suporte para RDS

    Melhorar a estrutura de exportação (adicionar XLSX)

    Futuramente incluir Azure e GCP (em projetos separados ou como módulos)

👨‍💻 Propósito do Projeto
Este projeto foi criado como uma forma de estudo e prática com:

    Boto3 (SDK da AWS para Python)

    Automação de inventário em nuvem

    Boas práticas de organização de código para infraestrutura

⚠️ Segurança das Credenciais
Este projeto não contém e nunca deve conter credenciais da AWS (Access Key ID, Secret Access Key, etc).

Para rodar o código, configure suas credenciais localmente usando uma das opções:

    Via AWS CLI:

aws configure

Ou via variáveis de ambiente:

export AWS_ACCESS_KEY_ID=xxxx
export AWS_SECRET_ACCESS_KEY=yyyy

📃 Licença
MIT License.

📫 Contato
Dúvidas ou sugestões: thomas.s.cordeiro@hotmail.com
