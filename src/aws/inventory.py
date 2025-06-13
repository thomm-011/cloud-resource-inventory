#!/usr/bin/env python3
"""
AWS Resource Inventory Script
Coleta informações de recursos AWS e exporta para diferentes formatos
"""

import boto3
import json
import csv
from datetime import datetime
from typing import Dict, List, Any
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AWSInventory:
    def __init__(self, profile_name=None, region='us-east-1'):
        """Inicializa o inventário AWS"""
        self.session = boto3.Session(profile_name=profile_name)
        self.region = region
        self.inventory_data = {}
        
    def get_ec2_instances(self) -> List[Dict]:
        """Coleta informações das instâncias EC2"""
        try:
            ec2 = self.session.client('ec2', region_name=self.region)
            
            response = ec2.describe_instances()
            instances = []
            
            for reservation in response['Reservations']:
                for instance in reservation['Instances']:
                    # Extrair tags
                    tags = {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
                    
                    instance_info = {
                        'InstanceId': instance['InstanceId'],
                        'InstanceType': instance['InstanceType'],
                        'State': instance['State']['Name'],
                        'LaunchTime': instance.get('LaunchTime', '').isoformat() if instance.get('LaunchTime') else '',
                        'Platform': instance.get('Platform', 'Linux'),
                        'VpcId': instance.get('VpcId', ''),
                        'SubnetId': instance.get('SubnetId', ''),
                        'PrivateIpAddress': instance.get('PrivateIpAddress', ''),
                        'PublicIpAddress': instance.get('PublicIpAddress', ''),
                        'KeyName': instance.get('KeyName', ''),
                        'SecurityGroups': [sg['GroupName'] for sg in instance.get('SecurityGroups', [])],
                        'Tags': tags,
                        'Name': tags.get('Name', 'N/A'),
                        'Environment': tags.get('Environment', 'N/A'),
                        'Owner': tags.get('Owner', 'N/A')
                    }
                    instances.append(instance_info)
            
            logger.info(f"Encontradas {len(instances)} instâncias EC2")
            return instances
            
        except Exception as e:
            logger.error(f"Erro ao coletar instâncias EC2: {str(e)}")
            return []

    def get_s3_buckets(self) -> List[Dict]:
        """Coleta informações dos buckets S3"""
        try:
            s3 = self.session.client('s3')
            
            response = s3.list_buckets()
            buckets = []
            
            for bucket in response['Buckets']:
                bucket_name = bucket['Name']
                
                # Obter região do bucket
                try:
                    location = s3.get_bucket_location(Bucket=bucket_name)
                    region = location['LocationConstraint'] or 'us-east-1'
                except:
                    region = 'unknown'
                
                # Obter tamanho do bucket (estimativa)
                try:
                    s3_resource = self.session.resource('s3')
                    bucket_resource = s3_resource.Bucket(bucket_name)
                    size = sum(obj.size for obj in bucket_resource.objects.all())
                    object_count = sum(1 for _ in bucket_resource.objects.all())
                except:
                    size = 0
                    object_count = 0
                
                # Obter tags
                try:
                    tags_response = s3.get_bucket_tagging(Bucket=bucket_name)
                    tags = {tag['Key']: tag['Value'] for tag in tags_response['TagSet']}
                except:
                    tags = {}
                
                bucket_info = {
                    'BucketName': bucket_name,
                    'CreationDate': bucket['CreationDate'].isoformat(),
                    'Region': region,
                    'SizeBytes': size,
                    'ObjectCount': object_count,
                    'SizeGB': round(size / (1024**3), 2),
                    'Tags': tags,
                    'Environment': tags.get('Environment', 'N/A'),
                    'Owner': tags.get('Owner', 'N/A')
                }
                buckets.append(bucket_info)
            
            logger.info(f"Encontrados {len(buckets)} buckets S3")
            return buckets
            
        except Exception as e:
            logger.error(f"Erro ao coletar buckets S3: {str(e)}")
            return []

    def get_rds_instances(self) -> List[Dict]:
        """Coleta informações das instâncias RDS"""
        try:
            rds = self.session.client('rds', region_name=self.region)
            
            response = rds.describe_db_instances()
            instances = []
            
            for db in response['DBInstances']:
                # Obter tags
                try:
                    tags_response = rds.list_tags_for_resource(ResourceName=db['DBInstanceArn'])
                    tags = {tag['Key']: tag['Value'] for tag in tags_response['TagList']}
                except:
                    tags = {}
                
                instance_info = {
                    'DBInstanceIdentifier': db['DBInstanceIdentifier'],
                    'DBInstanceClass': db['DBInstanceClass'],
                    'Engine': db['Engine'],
                    'EngineVersion': db['EngineVersion'],
                    'DBInstanceStatus': db['DBInstanceStatus'],
                    'AllocatedStorage': db['AllocatedStorage'],
                    'StorageType': db.get('StorageType', ''),
                    'MultiAZ': db['MultiAZ'],
                    'VpcId': db.get('DbSubnetGroup', {}).get('VpcId', ''),
                    'AvailabilityZone': db.get('AvailabilityZone', ''),
                    'BackupRetentionPeriod': db['BackupRetentionPeriod'],
                    'InstanceCreateTime': db.get('InstanceCreateTime', '').isoformat() if db.get('InstanceCreateTime') else '',
                    'Tags': tags,
                    'Environment': tags.get('Environment', 'N/A'),
                    'Owner': tags.get('Owner', 'N/A')
                }
                instances.append(instance_info)
            
            logger.info(f"Encontradas {len(instances)} instâncias RDS")
            return instances
            
        except Exception as e:
            logger.error(f"Erro ao coletar instâncias RDS: {str(e)}")
            return []

    def get_lambda_functions(self) -> List[Dict]:
        """Coleta informações das funções Lambda"""
        try:
            lambda_client = self.session.client('lambda', region_name=self.region)
            
            response = lambda_client.list_functions()
            functions = []
            
            for func in response['Functions']:
                # Obter tags
                try:
                    tags_response = lambda_client.list_tags(Resource=func['FunctionArn'])
                    tags = tags_response['Tags']
                except:
                    tags = {}
                
                function_info = {
                    'FunctionName': func['FunctionName'],
                    'Runtime': func['Runtime'],
                    'Handler': func['Handler'],
                    'CodeSize': func['CodeSize'],
                    'Description': func.get('Description', ''),
                    'Timeout': func['Timeout'],
                    'MemorySize': func['MemorySize'],
                    'LastModified': func['LastModified'],
                    'Version': func['Version'],
                    'VpcId': func.get('VpcConfig', {}).get('VpcId', ''),
                    'Tags': tags,
                    'Environment': tags.get('Environment', 'N/A'),
                    'Owner': tags.get('Owner', 'N/A')
                }
                functions.append(function_info)
            
            logger.info(f"Encontradas {len(functions)} funções Lambda")
            return functions
            
        except Exception as e:
            logger.error(f"Erro ao coletar funções Lambda: {str(e)}")
            return []

    def run_inventory(self) -> Dict[str, Any]:
        """Executa o inventário completo"""
        logger.info(f"Iniciando inventário AWS na região {self.region}")
        
        self.inventory_data = {
            'timestamp': datetime.now().isoformat(),
            'region': self.region,
            'account_id': self.session.client('sts').get_caller_identity()['Account'],
            'resources': {
                'ec2_instances': self.get_ec2_instances(),
                's3_buckets': self.get_s3_buckets(),
                'rds_instances': self.get_rds_instances(),
                'lambda_functions': self.get_lambda_functions()
            }
        }
        
        # Calcular totais
        totals = {}
        for resource_type, resources in self.inventory_data['resources'].items():
            totals[resource_type] = len(resources)
        
        self.inventory_data['summary'] = totals
        
        logger.info("Inventário concluído!")
        logger.info(f"Resumo: {totals}")
        
        return self.inventory_data

    def export_to_json(self, filename: str):
        """Exporta inventário para JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.inventory_data, f, indent=2, ensure_ascii=False, default=str)
        logger.info(f"Inventário exportado para {filename}")

    def export_to_csv(self, resource_type: str, filename: str):
        """Exporta um tipo específico de recurso para CSV"""
        if resource_type not in self.inventory_data['resources']:
            logger.error(f"Tipo de recurso '{resource_type}' não encontrado")
            return
        
        resources = self.inventory_data['resources'][resource_type]
        if not resources:
            logger.warning(f"Nenhum recurso do tipo '{resource_type}' encontrado")
            return
        
        # Obter todas as chaves possíveis
        all_keys = set()
        for resource in resources:
            all_keys.update(resource.keys())
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=sorted(all_keys))
            writer.writeheader()
            
            for resource in resources:
                # Converter listas e dicts para strings
                clean_resource = {}
                for key, value in resource.items():
                    if isinstance(value, (list, dict)):
                        clean_resource[key] = str(value)
                    else:
                        clean_resource[key] = value
                writer.writerow(clean_resource)
        
        logger.info(f"Recursos {resource_type} exportados para {filename}")

def main():
    """Função principal"""
    # Exemplo de uso
    inventory = AWSInventory(region='us-east-1')
    
    # Executar inventário
    data = inventory.run_inventory()
    
    # Exportar resultados
    inventory.export_to_json('aws_inventory.json')
    inventory.export_to_csv('ec2_instances', 'ec2_instances.csv')
    inventory.export_to_csv('s3_buckets', 's3_buckets.csv')
    inventory.export_to_csv('rds_instances', 'rds_instances.csv')
    inventory.export_to_csv('lambda_functions', 'lambda_functions.csv')

if __name__ == '__main__':
    main()