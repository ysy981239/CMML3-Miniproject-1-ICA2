# CMML3 Mini-Project 1: Automated Protein-Ligand Interaction Pipeline

## Overview
This repository contains the automated Python scripts used to process protein-ligand complexes for high-throughput virtual screening. The pipeline handles dataset preparation, automated output extraction from DiffDock simulations, structural format wrangling, and biophysical thermodynamic scoring.

## Pipeline Architecture
The Python-based workflow is structured into three sequential automated modules:
- `01_batch_preparation.py`: Automates the registration of complex file paths (specifically targeting the assigned B-series structural cohort) to generate a task ledger for DiffDock CLI execution (`python -m inference`).
- `02_extract_diffdock_scores.py`: Parses the massive DiffDock structural output directories and automatically extracts the top-ranked geometric confidence scores for downstream filtering using regex.
- `03_pymol_prodigy_pipeline.py`: An end-to-end integration script. It utilizes the PyMOL CLI in headless mode (`-cq`) to merge SDF/PDB files and reassign chain identifiers (Protein -> 'A', Ligand -> 'L:LIG'). Subsequently, it utilizes Python's `subprocess` to trigger PRODIGY-LIG to calculate thermodynamic binding free energies (ΔG) and aggregates the final ranking.

## Environment Details
- OS: Linux Server (Ubuntu)
- Python 3.x with Conda
- Key Dependencies: PyMOL CLI, PRODIGY-LIG, DiffDock

## Target Cohort
As per the project division, the code and final data analysis specifically focus on the thermodynamic evaluation of the **B-series cohort (B1-B7)**.
