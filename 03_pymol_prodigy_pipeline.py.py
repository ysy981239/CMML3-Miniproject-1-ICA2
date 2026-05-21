import pandas as pd
import subprocess
import os

# Load the initial geometric ranking data
df = pd.read_csv('top_docking_results.csv')
top_n = df.head(20).copy()
prodigy_scores = []

print("🚀 Initiating PRODIGY-LIG to calculate thermodynamic binding free energies (ΔG) for the Top 20 candidates...")

# Prepare a temporary directory to store the merged complexes
temp_dir = 'temp_complexes'
os.makedirs(temp_dir, exist_ok=True)

for index, row in top_n.iterrows():
    protein = row['Protein_Path']
    ligand = row['Ligand_Path']
    complex_name = row['Complex_Name']
    
    merged_pdb = os.path.abspath(os.path.join(temp_dir, f"{complex_name}_merged.pdb"))
    
    print(f"\n[{index+1}/20] Processing complex: {complex_name} ...")
    
    # --- Step 1: Programmatically merge PDB and SDF files via PyMOL CLI ---
    pml_content = f"""
load {protein}, prot
load {ligand}, lig
alter prot, chain='A'
alter lig, chain='L'
alter lig, resn='LIG'
save {merged_pdb}, all
quit
"""
    pml_file = 'temp_merge.pml'
    with open(pml_file, 'w') as f:
        f.write(pml_content)
        
    subprocess.run("env PATH=/usr/bin:/bin /usr/bin/pymol -cq temp_merge.pml", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # --- Step 2: Execute PRODIGY-LIG biophysical scoring ---
    if not os.path.exists(merged_pdb):
        print(f"❌ PyMOL merging failed for {complex_name}. Skipping...")
        prodigy_scores.append(None)
        continue

    cmd = f'prodigy_lig -i "{merged_pdb}" -c A L:LIG'
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ PRODIGY execution failed:\n{result.stderr.strip()}")
            prodigy_scores.append(None)
            continue
            
        # Parse the ΔG value from the PRODIGY output
        delta_g = None
        for line in result.stdout.split('\n'):
            if "_merged" in line:
                try:
                    # Extract the numerical score from the end of the target line
                    delta_g = float(line.split()[-1])
                    break
                except:
                    pass
                
        if delta_g is not None:
            prodigy_scores.append(delta_g)
            print(f"✅ Calculated ΔG = {delta_g} kcal/mol")
        else:
            print(f"⚠️ Calculation executed but failed to parse the numeric value. Raw output:\n{result.stdout}")
            prodigy_scores.append(None)
            
    except Exception as e:
        prodigy_scores.append(None)
        print(f"❌ System exception encountered: {e}")

# Integrate the thermodynamic scores into the dataframe
top_n['Delta_G (kcal/mol)'] = prodigy_scores

# Filter out failed calculations to ensure accurate sorting
final_ranked = top_n.dropna(subset=['Delta_G (kcal/mol)'])

# Sort by ΔG in ascending order (lower/more negative indicates stronger binding affinity)
final_ranked = final_ranked.sort_values(by='Delta_G (kcal/mol)', ascending=True)

output_final = 'top_20_prodigy_scored.csv'
final_ranked.to_csv(output_final, index=False)

print(f"\n🎉 PRODIGY-LIG thermodynamic evaluation complete! Final ranked dataset saved as: {output_final}")