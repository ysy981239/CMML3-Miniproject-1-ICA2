import os
import csv

protein_dir = "proteinPDB"
ligand_dir = "substrate"
output_csv = "docking_tasks.csv"

# Target specific B-series proteins (B1 to B7)
proteins = [f"B{i}.pdb" for i in range(1, 8)]
data = [["complex_name", "protein_path", "ligand_description"]]

for prot in proteins:
    prot_path = os.path.join(protein_dir, prot)
    if not os.path.exists(prot_path): 
        continue
    
    for lig in os.listdir(ligand_dir):
        if lig.endswith('.sdf'):
            lig_path = os.path.join(ligand_dir, lig)
            complex_name = f"{prot.replace('.pdb', '')}_{lig.replace('.sdf', '')}"
            data.append([complex_name, prot_path, lig_path])

with open(output_csv, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(data)
    
print(f"✅ Successfully generated CSV with {len(data)-1} targeted docking tasks!")