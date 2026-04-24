This repository contains the supplementary materials for the "Analysis Of False Data Injection Attacks On
IEC 61850 In Digital Substation" thesis.

# Smart Grid Simulator (SGSim) - the main simulator used for this Thesis.
# SGSim is a tool for simulation of communication and cyber attacks in digital primary and secondary substations.

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
