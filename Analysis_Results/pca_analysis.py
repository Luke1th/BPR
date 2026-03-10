import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import os
import sys
from scipy import stats # Import scipy.stats for t-test

# Define file paths
baseline_file = 'SGSim/C0_Baseline/Baseline.csv'
fdi_file = 'SGSim/C1_FDI/FDI.csv'

# Load datasets, explicitly defining frame.time as string to avoid parsing issues
try:
    df_baseline = pd.read_csv(baseline_file, dtype={'frame.time': str})
    df_fdi = pd.read_csv(fdi_file, dtype={'frame.time': str})
except FileNotFoundError as e:
    print(f"Error loading file: {e}")
    sys.exit(1)

# Add labels
df_baseline['label'] = 'baseline'
df_fdi['label'] = 'fdi'

# Combine datasets
df_combined = pd.concat([df_baseline, df_fdi], ignore_index=True)

# --- Feature Engineering ---
# Convert 'frame.time' to datetime objects and then to epoch for numerical representation
df_combined['frame.time_dt'] = pd.to_datetime(df_combined['frame.time'], format='%Y-%m-%dT%H:%M:%S.%f%z')
df_combined['frame.time_epoch'] = df_combined['frame.time_dt'].astype(int) / 10**9 # Convert to seconds

# Calculate 'time_delta' (time difference between consecutive packets)
# Calculate within each group to avoid mixing time sequences from baseline and FDI
df_combined['time_delta'] = df_combined.groupby('label')['frame.time_epoch'].diff().fillna(0)


# --- Preprocessing ---
# Identify numerical columns for PCA
numerical_cols = df_combined.select_dtypes(include=['number']).columns.tolist()

# Exclude any known identifier columns that are not features to be analyzed
# 'frame.number' is still an identifier. 'frame.time_epoch' and 'time_delta' are engineered features.
exclude_cols = ['frame.number']
features = [col for col in numerical_cols if col not in exclude_cols]

# We need to make sure 'goose.float_value', 'frame.time_epoch', and 'time_delta' are included.
# 'frame.time_epoch' and 'time_delta' are already numerical.
# If they are not in the numerical_cols for some reason (e.g., all NaNs), then we need to handle that.
# For now, let's assume they are correctly identified as numerical.
# Make sure goose.float_value is in features too.
if 'goose.float_value' not in features:
    features.append('goose.float_value')

if len(features) < 2:
    print(f"Error: Not enough numerical features (excluding identifiers) found for PCA. Found: {features}")
    sys.exit(1)

# Separate features (X) and labels (y)
X = df_combined[features]
y = df_combined['label']

# Handle missing values (if any) - using mean imputation
X = X.fillna(X.mean())

# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# --- Perform PCA ---
pca = PCA()
X_pca = pca.fit_transform(X_scaled)

# Explained variance ratio
explained_variance_ratio = pca.explained_variance_ratio_
print("Explained variance ratio by principal components:")
for i, ratio in enumerate(explained_variance_ratio):
    print(f"PC{i+1}: {ratio:.4f}")

# --- Visualization ---
plt.figure(figsize=(12, 8))
if X_pca.shape[1] >= 2:
    # Plot first two principal components
    plt.scatter(X_pca[y == 'baseline', 0], X_pca[y == 'baseline', 1], label='Baseline', alpha=0.7, s=50)
    plt.scatter(X_pca[y == 'fdi', 0], X_pca[y == 'fdi', 1], label='FDI', alpha=0.7, s=50)
    plt.xlabel(f'Principal Component 1 ({explained_variance_ratio[0]*100:.2f}%)')
    plt.ylabel(f'Principal Component 2 ({explained_variance_ratio[1]*100:.2f}%)')
    plt.title('PCA of Baseline vs. FDI Data', fontsize=16)
    plt.legend(fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig('pca_2d_plot.png')
    print("2D PCA plot saved as 'pca_2d_plot.png'")
else:
    print("Not enough principal components to create a 2D plot.")

# --- Interpretation ---
if len(features) > 0 and X_pca.shape[1] > 0:
    # Display component loadings for the first few principal components
    num_components_to_show = min(3, pca.n_components_) # Show up to 3 components
    loadings = pd.DataFrame(pca.components_, columns=features, index=[f'PC{i+1}' for i in range(pca.n_components_)])

    print(f"\nTop 5 Feature loadings for the first {num_components_to_show} Principal Components:")
    for i in range(num_components_to_show):
        print(f"\n--- Principal Component {i+1} ---")
        # Sort by absolute value to see most influential features
        top_features = loadings.iloc[i].abs().sort_values(ascending=False).head(5).index
        print(loadings.iloc[i][top_features].sort_values(ascending=False))

print("\nPCA analysis script finished.")

# --- Statistical Significance (t-test) for goose.float_value ---
print("\n--- T-test for goose.float_value mean difference ---")

# Ensure 'goose.float_value' is present
if 'goose.float_value' in df_combined.columns:
    baseline_goose = df_combined[df_combined['label'] == 'baseline']['goose.float_value']
    fdi_goose = df_combined[df_combined['label'] == 'fdi']['goose.float_value']

    print("\nDescriptive statistics for 'goose.float_value' (Baseline):")
    print(baseline_goose.describe())
    print("\nDescriptive statistics for 'goose.float_value' (FDI):")
    print(fdi_goose.describe())

    # Perform independent t-test
    t_statistic, p_value = stats.ttest_ind(baseline_goose, fdi_goose, equal_var=False) # Welch's t-test assuming unequal variances

    print(f"\nMean 'goose.float_value' (Baseline): {baseline_goose.mean():.4f}")
    print(f"Mean 'goose.float_value' (FDI): {fdi_goose.mean():.4f}")
    print(f"T-statistic: {t_statistic:.4f}")
    print(f"P-value: {p_value:.4e}") # Use scientific notation for p-value

    alpha = 0.05
    if p_value < alpha:
        print(f"Conclusion: Reject the null hypothesis. The difference in means of 'goose.float_value' between Baseline and FDI is statistically significant (p < {alpha}).")
    else:
        print(f"Conclusion: Fail to reject the null hypothesis. There is no statistically significant difference in means of 'goose.float_value' between Baseline and FDI (p >= {alpha}).")
else:
    print("Error: 'goose.float_value' column not found in the combined dataframe.")