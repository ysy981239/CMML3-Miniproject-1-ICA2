import os
import re
import pandas as pd

results_dir = 'results_batch'
data = []

print(f"🔍 Scanning '{results_dir}' directory and matching protein paths...")

# Iterate through all complex subdirectories
for complex_name in os.listdir(results_dir):
    complex_path = os.path.join(results_dir, complex_name)
    
    if os.path.isdir(complex_path):
        ligand_file = None
        confidence = None
        
        # 1. Infer protein filename (e.g., "B7_1_formaldehyde" -> "B7.pdb")
        protein_id = complex_name.split('_')[0]
        pdb_filename = f"{protein_id}.pdb"
        
        # 2. Search for the protein file across possible absolute paths
        possible_protein_paths = [
            os.path.join('/root/miniproject/proteinPDB', pdb_filename),
            os.path.join('/root/miniproject/DiffDock/proteinPDB', pdb_filename),
            os.path.join('/root/miniproject', pdb_filename)
        ]
        
        protein_file = 'Protein_Not_Found'
        for path in possible_protein_paths:
            if os.path.exists(path):
                protein_file = path
                break
        
        # 3. Locate the rank-1 SDF ligand file and extract the confidence score
        for file in os.listdir(complex_path):
            if file.startswith('rank1') and 'confidence' in file and file.endswith('.sdf'):
                ligand_file = os.path.abspath(os.path.join(complex_path, file))
                match = re.search(r'confidence([-\d\.]+)', file)
                if match:
                    clean_score = match.group(1).rstrip('.')
                    confidence = float(clean_score)

        if ligand_file and confidence is not None:
            data.append({
                'Complex_Name': complex_name,
                'Confidence_Score': confidence,
                'Protein_Path': protein_file,
                'Ligand_Path': ligand_file
            })

# 4. Compile and rank the dataset
if not data:
    print("⚠️ Extraction failed: No rank-1 SDF files with confidence scores were found.")
else:
    df = pd.DataFrame(data)
    # Sort by Confidence_Score in descending order (higher is better for DiffDock)
    df = df.sort_values(by='Confidence_Score', ascending=False)
    
    output_csv = 'top_docking_results.csv'
    df.to_csv(output_csv, index=False)
    print(f"✅ Successfully extracted and ranked {len(df)} results! Saved as: {output_csv}")