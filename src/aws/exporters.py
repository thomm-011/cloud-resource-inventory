import json
import pandas as pd

def export_to_json(data, output_file):
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Dados exportados para {output_file} (JSON)")

def export_to_csv(data, output_file):
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)
    print(f"Dados exportados para {output_file} (CSV)")