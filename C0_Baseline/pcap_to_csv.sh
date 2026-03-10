#!/bin/bash

# This script finds all .pcapng files in the C0_Baseline directory,
# converts them to CSV format using tshark, and merges them into a
# single CSV file named Baseline.csv.

# Define the base directory where pcapng files are located
BASE_DIR="/home/luk3/Desktop/SGSim/C0_Baseline/"

# Define the output CSV file name
OUTPUT_CSV="/home/luk3/Desktop/SGSim/C0_Baseline/Baseline.csv"

# Find all pcapng files recursively and sort them to ensure a consistent order
PCAPNG_FILES=$(find "$BASE_DIR" -type f -name "*.pcapng" | sort)

# Check if any pcapng files were found
if [ -z "$PCAPNG_FILES" ]; then
    echo "Error: No .pcapng files were found in '$BASE_DIR'."
    exit 1
fi

echo "The following .pcapng files will be processed:"
echo "$PCAPNG_FILES"
echo "---"

# Remove the output file if it already exists to ensure a fresh start
rm -f "$OUTPUT_CSV"

# A flag to handle the CSV header for the very first file
is_first_file=true

# Loop through each found pcapng file
for pcap_file in $PCAPNG_FILES; do
    echo "Processing $pcap_file..."

    if [ "$is_first_file" = true ]; then
        # For the first file, use tshark to extract fields and include the header
        tshark -r "$pcap_file" -T fields \
            -Y "goose || sv" \
            -e frame.number \
            -e frame.time \
            -e eth.src \
            -e eth.dst \
            -e _ws.col.Protocol \
            -e goose.float_value \
            -E header=y -E separator=, -E quote=d \
            > "$OUTPUT_CSV"
        
        # Check if the tshark command failed
        if [ $? -ne 0 ]; then
            echo "Critical Error: tshark failed on the first file: $pcap_file."
            echo "Aborting script. The output file may be empty or incomplete."
            exit 1
        fi
        is_first_file=false
    else
        # For all subsequent files, append the data without the header
        tshark -r "$pcap_file" -T fields \
            -Y "goose || sv" \
            -e frame.number \
            -e frame.time \
            -e eth.src \
            -e eth.dst \
            -e _ws.col.Protocol \
            -e goose.float_value \
            -E header=n -E separator=, -E quote=d \
            >> "$OUTPUT_CSV"

        # Warning in case a specific file fails
        if [ $? -ne 0 ]; then
            echo "Warning: tshark failed to process '$pcap_file'."
            echo "This file's data will be missing from the final CSV."
        fi
    fi
done

echo "---"
echo "Conversion complete!"
echo "All data has been merged into: $OUTPUT_CSV"
