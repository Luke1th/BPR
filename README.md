# Analysis Of False Data Injection Attacks On IEC 61850 In Digital Substation

## This repository contains the supplementary materials for the thesis.

The supplement is intended to support reproducibility and transparent auditing of the paper’s methodology, implementation and results, with a particular focus on analyzing the nature of False Data Injection (FDI) attacks within Digital Primary Substation (DPS), and vulnerabilities of IEC 61850 standard, and GOOSE communication protocol.

Contents

Pre-requizites

    mininet
    sqlite3

Installation

    Extract comlib_dps.zip and comlib_dss.zip in the same folder

Run

    Topology: ./StartSGTopology.sh
    Available commands: mininet> help (commands starting with sgsim_ were added to the Mininet, use help commnand for description)
    GUI: ./GUI/StartGUI.sh
    SCADA simulation: open webbrowser at localhost:8000
