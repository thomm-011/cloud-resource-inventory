import boto3
import argparse
import os
from exporters import export_to_json, export_to_csv

def list_ec2_instances():
    ec2_client = boto3.client('ec2')
    response = ec2_client.describe_instances()
    instances = []

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances.append({
                'InstanceId': instance['InstanceId'],
                'State': instance['State']['Name'],
                'InstanceType': instance.get('InstanceType'),
                'AvailabilityZone': instance.get('Placement', {}).get('AvailabilityZone')
            })

    return instances

def list_s3_buckets():
    s3_client = boto3.client('s3')
    response = s3_client.list_buckets()
    buckets = []

    for bucket in response['Buckets']:
        buckets.append({
            'BucketName': bucket['Name'],
            'CreationDate': bucket['CreationDate'].strftime("%Y-%m-%d %H:%M:%S")
        })

    return buckets

def main():
    parser = argparse.ArgumentParser(description='AWS Resource Inventory')
    parser.add_argument('--resource', choices=['ec2', 's3'], required=True, help='Tipo de recurso para inventariar')
    parser.add_argument('--output', required=True, help='Caminho do arquivo de saída')
    parser.add_argument('--format', choices=['json', 'csv'], default='json', help='Formato de exportação')

    args = parser.parse_args()

    if args.resource == 'ec2':
        data = list_ec2_instances()
    elif args.resource == 's3':
        data = list_s3_buckets()
    else:
        print("Recurso não suportado.")
        return

    # Cria a pasta reports se não existir
    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    # Exporta
    if args.format == 'json':
        export_to_json(data, args.output)
    elif args.format == 'csv':
        export_to_csv(data, args.output)

if __name__ == "__main__":
    main()