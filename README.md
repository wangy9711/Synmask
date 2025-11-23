# Synmask Selection and Combination Pipeline

This repository contains 2 Jupyter notebooks that demonstrate the step-by-step selection pipeline for Syn-mask and combination pipeline for Synmask  based on structural and immunological criteria.

## 📘 Contents

- **`motif_selection.ipynb`**  
  A complete workflow including:
	-	Extraction of disordered fragments from PDB structures
	-	Identification of unresolved (missing-density) regions from SEQRES/ATOM mismatch
	-	Multi-stage filtering to remove low-complexity motifs, linker-like patterns, and undesired residue compositions
	-	Secondary structure screening using S4PRED, ProtBert, and AlphaFold2+DSSP
	-	Final refinement via amino-acid substitution/removal and re-prediction
	-	Selection of intrinsically disordered Syn-motif candidates for synthesis

- **`motif_combination.ipynb`**  
  A complete workflow including:
  - Random generation and motif-based assembly of Synmask sequences
  - Diversity filtering based on motif usage
  - Secondary structure prediction using S4PRED, ProtBert, and AlphaFold2
  - Immunogenicity screening via NetMHCpan (MHC-I and MHC-II)
  - Motif repetition control to improve expressibility

- **`netMHCpan-4.1`**  
  Command-line tool for MHC class I binding prediction.  

- **`netMHCIIpan-4.1`**  
  Command-line tool for MHC class II binding prediction.  

## 🛠 Requirements

- Python 3.8+
- PyTorch
- HuggingFace Transformers
- NumPy, Pandas, scikit-learn
- GPU recommended for structure and MHC model inference


## 🛠 External Tools

- [**S4PRED**](https://github.com/psipred/s4pred)  
  Used for fast secondary structure prediction of full-length Synmask sequences.  
  Model weights are available via the repository.

- [**ProtBert-BFD-SS3**](https://huggingface.co/Rostlab/prot_bert_bfd_ss3)  
  A transformer-based model for secondary structure prediction.  
  Integrated via HuggingFace Transformers and used for robust disorder region identification.

- **netMHCpan-4.1**  
  Command-line tool for MHC class I binding prediction.  
  Download the binary from the [official website](https://services.healthtech.dtu.dk/service.php?NetMHCpan-4.1).  
  Requires registration and academic license.

- **netMHCIIpan-4.1**  
  Command-line tool for MHC class II binding prediction.  
  Download available via the [official website](https://services.healthtech.dtu.dk/service.php?NetMHCIIpan-4.1).  
  Used for scanning potential CD4⁺ T-cell epitopes across multiple HLA class II alleles.

- **AlphaFold2** (optional)  
  Used for high-accuracy secondary structure filtering in the final stage.  
  For performance reasons, only run on prefiltered sequences.  
  [AlphaFold GitHub Repository](https://github.com/deepmind/alphafold)

## 📂 Notes

- GPU is highly recommended for running AlphaFold2 and ProtBert-based predictions.

## 📈 Output

- Ranked and filtered Syn-motif / Synmask candidates
- Summary tables for each screening stage
- Ready-to-use sequences for downstream experimental validation