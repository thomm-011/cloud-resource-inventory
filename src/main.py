# src/main.py
from aws.inventory import AWSInventory

def main():
    inventory = AWSInventory(region='us-east-1')
    inventory.run_inventory()
    inventory.export_to_json('reports/aws_inventory.json')
    inventory.export_to_csv('ec2_instances', 'reports/ec2_instances.csv')
    inventory.export_to_csv('s3_buckets', 'reports/s3_buckets.csv')
    inventory.export_to_csv('rds_instances', 'reports/rds_instances.csv')
    inventory.export_to_csv('lambda_functions', 'reports/lambda_functions.csv')

if __name__ == '__main__':
    main()
