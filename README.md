# Analysis Of False Data Injection Attacks On IEC 61850 In Digital Substation

## This repository contains the supplementary materials for the thesis ”Analysis Of False Data Injection Attacks On IEC 61850 In Digital Substation".

The supplement is intended to support reproducibility and transparent auditing of the paper’s methodology and results, with a particular focus on the proposed false-alarms-per-hour (FAH) calibration and benchmarking procedure.

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
