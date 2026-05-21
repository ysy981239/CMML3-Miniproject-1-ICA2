# CMML3 Mini-Project 1: Automated Protein-Ligand Interaction Pipeline

## Overview
This repository contains the automated Python scripts used to process protein-ligand complexes for virtual screening. The pipeline handles everything from batch preparation to structural format wrangling and thermodynamic scoring.

## Pipeline Structure
- 01_batch_preparation.py: Automates the registration of complex file paths (specifically targeting the assigned B-series structural cohort).
- 02_extract_diffdock_scores.py: Parses the DiffDock structural outputs and automatically extracts the top-ranked geometric confidence scores for downstream filtering.
- 03_pymol_prodigy_pipeline.py: An end-to-end integration script. It first uses the PyMOL CLI to merge SDF/PDB files and reassign chain identifiers (Protein -> 'A', Ligand -> 'L:LIG') to resolve format incompatibilities. Subsequently, it automatically triggers PRODIGY-LIG to calculate thermodynamic binding free energies (ΔG) and aggregates the final ranking.

## Environment Details
- OS: Linux Server (Ubuntu)
- Python 3.x with Conda
- Key Dependencies: PyMOL CLI, PRODIGY-LIG, DiffDock

## Target Cohort
As per the project division, the code and final data analysis specifically focus on the thermodynamic evaluation of the **B-series cohort (B1-B7)**.
