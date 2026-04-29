import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def load_and_prepare_data(filepath):
    df = pd.read_csv(filepath)
    df['frame.time'] = pd.to_datetime(df['frame.time'], errors='coerce')
    df['goose.float_value'] = pd.to_numeric(df['goose.float_value'], errors='coerce')
    return df

def plot_goose_value_distribution(baseline_df, fdi_df, delay_df):
    plt.figure(figsize=(15, 5))

    plt.subplot(1, 3, 1)
    sns.histplot(baseline_df['goose.float_value'].dropna(), bins=50, kde=True)
    plt.title('Baseline GOOSE Value Distribution')
    plt.xlabel('(Relative Time(seconds)')

    plt.subplot(1, 3, 2)
    sns.histplot(fdi_df['goose.float_value'].dropna(), bins=50, kde=True)
    plt.title('FDI GOOSE Value Distribution')
    plt.xlabel('Relative Time(seconds)')

    plt.subplot(1, 3, 3)
    sns.histplot(delay_df['goose.float_value'].dropna(), bins=50, kde=True)
    plt.title('Delay GOOSE Value Distribution')
    plt.xlabel('(Relative Time(seconds)')

    plt.tight_layout()
    plt.savefig('goose_value_distribution.png')
    plt.close()

def plot_packet_frequency(baseline_df, fdi_df, delay_df):
    plt.figure(figsize=(15, 5)) # Use previous figsize for 3 subplots

    datasets = {
        'Baseline': baseline_df,
        'FDI': fdi_df,
        'Delay': delay_df
    }

    # Define color for consistency across subplots
    line_color = 'steelblue'

    for i, (name, df) in enumerate(datasets.items()):
        plt.subplot(1, 3, i + 1)

        if not df.empty and 'frame.time' in df.columns:
            # Calculate relative time in seconds starting from each dataframe's min time
            start_time = df['frame.time'].min()

            # Create a time series of packets per second
            time_series = pd.Series(1, index=df['frame.time'])
            packets_per_sec = time_series.resample('s').count()

            # Convert packets_per_sec index to relative seconds
            resampled_relative_bins = (packets_per_sec.index - start_time).total_seconds()

            # Filter data to within the 0-120 second range
            plot_mask = (resampled_relative_bins >= 0) & (resampled_relative_bins <= 120)
            plot_x = resampled_relative_bins[plot_mask]
            plot_y = packets_per_sec[plot_mask].values

            # Plot raw packet counts per second as a solid line
            plt.plot(plot_x, plot_y,
                     color=line_color,
                     linewidth=1.5,
                     linestyle='-',
                     marker='',
                     label=f'{name} Packet Count')

            plt.title(f'{name} Packet Rate')
            plt.xlabel('(Time in seconds)')
            plt.ylabel('Packets per Second')
            plt.xlim(0, 120) # Set x-axis limit from 0 to 120 seconds
            plt.grid(True, linestyle='--', alpha=0.7) # Added grid back
            plt.legend(fontsize=9, loc='lower left') # Add legend, moved to lower left
        else:
            plt.title(f'{name} Packet Rate (No Data)')
            plt.xlabel('(Time in seconds)')
            plt.ylabel('Packets per Second')
            plt.xlim(0, 120)
            plt.text(60, 0.5, 'No data available', horizontalalignment='center', verticalalignment='center', transform=plt.gca().transAxes)

    plt.tight_layout()
    plt.savefig('packet_frequency.png')
    plt.close()

def plot_delay_analysis(delay_df):
    plt.figure(figsize=(10, 5))
    sns.lineplot(x=delay_df['frame.time'], y=delay_df['time_diff'])
    plt.title('Time Difference Between Consecutive Packets (Delay Attack)')
    plt.xlabel('(Time in seconds)')
    plt.ylabel('Time Difference (s)')
    plt.savefig('delay_analysis.png')
    plt.close()


def analyze_data():
    baseline_df = load_and_prepare_data('SGSim/C0_Baseline/Baseline01/trial01.csv')
    fdi_df = load_and_prepare_data('SGSim/C1_FDI/C1_FDI_trial01/trial01.csv')
    delay_df = load_and_prepare_data('SGSim/C2_Delay/C2_Delay_30s_trial01/trial01.csv')

    # Calculate time_diff for both baseline_df and delay_df
    baseline_df['time_diff'] = baseline_df['frame.time'].diff().dt.total_seconds()
    delay_df['time_diff'] = delay_df['frame.time'].diff().dt.total_seconds()


    print("Baseline Data Info:")
    baseline_df.info()
    print("\nFDI Data Info:")
    fdi_df.info()
    print("\nDelay Data Info:")
    delay_df.info()

    plot_goose_value_distribution(baseline_df, fdi_df, delay_df)
    plot_packet_frequency(baseline_df, fdi_df, delay_df)
    plot_delay_analysis(delay_df)


if __name__ == "__main__":
    analyze_data()

