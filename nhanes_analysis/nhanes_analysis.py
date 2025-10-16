# CAPSTONE PROJECT 1
# Working with numpy Matrices (Multidimensional Data)
# NHANES Body Measurements Analysis

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import pandas as pd

# Set style for better-looking plots
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

print("="*70)
print("NHANES BODY MEASUREMENTS ANALYSIS")
print("="*70)

# ============================================================================
# SECTION 1: DATA LOADING
# ============================================================================
print("\n### SECTION 1: Loading Data ###\n")
print("Loading the NHANES datasets for adult males and females...")

try:
    # Load the datasets
    male_data = np.genfromtxt('nhanes_adult_male_bmx_2020.csv', delimiter=',', skip_header=1)
    female_data = np.genfromtxt('nhanes_adult_female_bmx_2020.csv', delimiter=',', skip_header=1)
    
    print(f"✓ Male dataset loaded successfully: {male_data.shape}")
    print(f"✓ Female dataset loaded successfully: {female_data.shape}")
    
    # Column names
    columns = ['weight', 'standing_height', 'upper_arm_length', 'upper_leg_length', 
               'arm_circumference', 'hip_circumference', 'waist_circumference']
    
    print(f"\nColumns in the dataset: {columns}")
    
except Exception as e:
    print(f"Error loading data: {e}")
    print("\nPlease ensure the following files are in the same directory:")
    print("- nhanes_adult_male_bmx_2020.csv")
    print("- nhanes_adult_female_bmx_2020.csv")
    exit()

# ============================================================================
# SECTION 2: HISTOGRAMS FOR WEIGHT DISTRIBUTION
# ============================================================================
print("\n### SECTION 2: Weight Distribution Analysis ###\n")
print("Creating histograms to visualize the weight distribution by gender...")

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Female weights histogram
axes[0].hist(female_data[:, 0], bins=30, color='hotpink', alpha=0.7, edgecolor='black')
axes[0].set_title('Female Weights Distribution', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Weight (kg)', fontsize=12)
axes[0].set_ylabel('Frequency', fontsize=12)
axes[0].grid(True, alpha=0.3)

# Male weights histogram
axes[1].hist(male_data[:, 0], bins=30, color='steelblue', alpha=0.7, edgecolor='black')
axes[1].set_title('Male Weights Distribution', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Weight (kg)', fontsize=12)
axes[1].set_ylabel('Frequency', fontsize=12)
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('weight_histograms.png', dpi=300, bbox_inches='tight')
plt.show()

print("✓ Histograms created and saved as 'weight_histograms.png'")

# ============================================================================
# SECTION 3: BOX-AND-WHISKER PLOT FOR WEIGHTS
# ============================================================================
print("\n### SECTION 3: Box Plot Comparison ###\n")
print("Creating box plots to compare male and female weight distributions...")

fig, ax = plt.subplots(figsize=(10, 6))

box_data = [female_data[:, 0], male_data[:, 0]]
bp = ax.boxplot(box_data, labels=['Female', 'Male'], patch_artist=True,
                widths=0.6, showmeans=True,
                boxprops=dict(facecolor='lightblue', alpha=0.7),
                medianprops=dict(color='red', linewidth=2),
                meanprops=dict(marker='D', markerfacecolor='green', markersize=8))

# Color the boxes differently
bp['boxes'][0].set_facecolor('hotpink')
bp['boxes'][1].set_facecolor('steelblue')

ax.set_title('Weight Distribution Comparison: Male vs Female', fontsize=14, fontweight='bold')
ax.set_ylabel('Weight (kg)', fontsize=12)
ax.grid(True, alpha=0.3, axis='y')

plt.savefig('weight_boxplot.png', dpi=300, bbox_inches='tight')
plt.show()

print("✓ Box plot created and saved as 'weight_boxplot.png'")
print("\nComparison Results:")
print(f"  - Male weights range: {male_data[:, 0].min():.2f} to {male_data[:, 0].max():.2f} kg")
print(f"  - Female weights range: {female_data[:, 0].min():.2f} to {female_data[:, 0].max():.2f} kg")
print(f"  - Males are generally heavier than females, as expected.")

# ============================================================================
# SECTION 4: NUMERICAL AGGREGATES
# ============================================================================
print("\n### SECTION 4: Statistical Aggregates ###\n")
print("Computing measures of location, dispersion, and shape for both datasets...\n")

def compute_stats(data, gender):
    print(f"--- {gender} Statistics ---")
    for i, col in enumerate(columns):
        values = data[:, i]
        print(f"\n{col.upper()}:")
        print(f"  Mean: {np.mean(values):.2f}")
        print(f"  Median: {np.median(values):.2f}")
        print(f"  Std Dev: {np.std(values):.2f}")
        print(f"  Min: {np.min(values):.2f}")
        print(f"  Max: {np.max(values):.2f}")
        print(f"  Skewness: {stats.skew(values):.3f}")
        print(f"  Kurtosis: {stats.kurtosis(values):.3f}")
    print()

compute_stats(male_data, "MALE")
compute_stats(female_data, "FEMALE")

# Distribution comparison
print("\n### Distribution Analysis ###")
print("\nComparing left-skewed vs right-skewed distributions:")

for i, col in enumerate(columns):
    male_skew = stats.skew(male_data[:, i])
    female_skew = stats.skew(female_data[:, i])
    
    male_dir = "left-skewed" if male_skew < 0 else "right-skewed"
    female_dir = "left-skewed" if female_skew < 0 else "right-skewed"
    
    print(f"\n{col}:")
    print(f"  Male: {male_dir} (skewness = {male_skew:.3f})")
    print(f"  Female: {female_dir} (skewness = {female_skew:.3f})")

print("\n✓ Statistical analysis complete")

# ============================================================================
# SECTION 5: BODY MASS INDEX COLUMN
# ============================================================================
print("\n### SECTION 5: Body Mass Index Analysis ###\n")
print("Adding BMI column to female dataset...")

# BMI = weight (kg) / (height (m))^2
female_weight = female_data[:, 0]  # weight in kg
female_height = female_data[:, 1] / 100  # height in cm converted to meters

female_bmi = female_weight / (female_height ** 2)

# Add BMI as 8th column
female_data_with_bmi = np.column_stack([female_data, female_bmi])

print(f"✓ BMI column added. New shape: {female_data_with_bmi.shape}")
print(f"\nBMI Statistics for Females:")
print(f"  Mean BMI: {np.mean(female_bmi):.2f}")
print(f"  Median BMI: {np.median(female_bmi):.2f}")
print(f"  Std Dev: {np.std(female_bmi):.2f}")
print(f"  Min BMI: {np.min(female_bmi):.2f}")
print(f"  Max BMI: {np.max(female_bmi):.2f}")

# ============================================================================
# SECTION 6: STANDARDIZED FEMALE DATASET (Z-SCORES)
# ============================================================================
print("\n### SECTION 6: Standardized Female Dataset ###\n")
print("Creating z-score standardized version of the female dataset...")

# Standardize each column (z-scores)
female_standardized = np.zeros_like(female_data)

for i in range(female_data.shape[1]):
    mean = np.mean(female_data[:, i])
    std = np.std(female_data[:, i])
    female_standardized[:, i] = (female_data[:, i] - mean) / std

print(f"✓ Standardization complete. Shape: {female_standardized.shape}")
print(f"\nVerifying standardization (all columns should have mean≈0, std≈1):")

for i, col in enumerate(columns):
    print(f"  {col}: mean={np.mean(female_standardized[:, i]):.4f}, std={np.std(female_standardized[:, i]):.4f}")

# ============================================================================
# SECTION 7: SCATTERPLOT MATRIX (PAIRPLOT)
# ============================================================================
print("\n### SECTION 7: Scatterplot Matrix ###\n")
print("Creating pairplot for standardized height, weight, circumferences, and BMI...")

# Select columns for pairplot: height, weight, arm_circ, hip_circ, waist_circ, BMI
selected_indices = [0, 1, 4, 5, 6]  # weight, height, arm, hip, waist
selected_columns = ['Weight', 'Height', 'Arm Circ', 'Hip Circ', 'Waist Circ', 'BMI']

# Create dataframe with standardized values
df_standardized = pd.DataFrame(female_standardized[:, selected_indices], 
                               columns=selected_columns[:-1])
df_standardized['BMI'] = (female_bmi - np.mean(female_bmi)) / np.std(female_bmi)

# Create pairplot
print("Generating pairplot (this may take a moment)...")
pairplot = sns.pairplot(df_standardized, diag_kind='kde', plot_kws={'alpha': 0.6})
pairplot.fig.suptitle('Standardized Female Body Measurements - Pairplot', y=1.02, fontsize=16)
plt.savefig('standardized_pairplot.png', dpi=300, bbox_inches='tight')
plt.show()

print("✓ Pairplot created and saved as 'standardized_pairplot.png'")

# ============================================================================
# SECTION 8: CORRELATION ANALYSIS
# ============================================================================
print("\n### SECTION 8: Correlation Analysis ###\n")
print("Computing Pearson's and Spearman's correlation coefficients...\n")

# Pearson correlation
pearson_corr = np.corrcoef(df_standardized.T)
print("PEARSON'S CORRELATION MATRIX:")
print(pd.DataFrame(pearson_corr, index=selected_columns, columns=selected_columns).round(3))

# Spearman correlation
spearman_corr = stats.spearmanr(df_standardized).correlation
print("\n\nSPEARMAN'S CORRELATION MATRIX:")
print(pd.DataFrame(spearman_corr, index=selected_columns, columns=selected_columns).round(3))

# Heatmap visualization
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

sns.heatmap(pearson_corr, annot=True, fmt='.2f', cmap='coolwarm', center=0,
            xticklabels=selected_columns, yticklabels=selected_columns,
            ax=axes[0], vmin=-1, vmax=1)
axes[0].set_title("Pearson's Correlation Heatmap", fontsize=14, fontweight='bold')

sns.heatmap(spearman_corr, annot=True, fmt='.2f', cmap='coolwarm', center=0,
            xticklabels=selected_columns, yticklabels=selected_columns,
            ax=axes[1], vmin=-1, vmax=1)
axes[1].set_title("Spearman's Correlation Heatmap", fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('correlation_heatmaps.png', dpi=300, bbox_inches='tight')
plt.show()

print("\n✓ Correlation heatmaps saved as 'correlation_heatmaps.png'")

# ============================================================================
# SECTION 9: WAIST-TO-HEIGHT AND WAIST-TO-HIP RATIOS
# ============================================================================
print("\n### SECTION 9: Body Ratio Analysis ###\n")
print("Computing waist-to-height and waist-to-hip ratios...\n")

# Male ratios
male_waist_height_ratio = male_data[:, 6] / male_data[:, 1]
male_waist_hip_ratio = male_data[:, 6] / male_data[:, 5]

# Female ratios
female_waist_height_ratio = female_data[:, 6] / female_data[:, 1]
female_waist_hip_ratio = female_data[:, 6] / female_data[:, 5]

print("WAIST-TO-HEIGHT RATIO:")
print(f"  Male - Mean: {np.mean(male_waist_height_ratio):.4f}, Std: {np.std(male_waist_height_ratio):.4f}")
print(f"  Female - Mean: {np.mean(female_waist_height_ratio):.4f}, Std: {np.std(female_waist_height_ratio):.4f}")

print("\nWAIST-TO-HIP RATIO:")
print(f"  Male - Mean: {np.mean(male_waist_hip_ratio):.4f}, Std: {np.std(male_waist_hip_ratio):.4f}")
print(f"  Female - Mean: {np.mean(female_waist_hip_ratio):.4f}, Std: {np.std(female_waist_hip_ratio):.4f}")

# ============================================================================
# SECTION 10: BOX PLOTS FOR RATIOS
# ============================================================================
print("\n### SECTION 10: Ratio Distribution Comparison ###\n")
print("Creating box plots for waist-to-height and waist-to-hip ratios...")

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Waist-to-height ratio
bp1 = axes[0].boxplot([female_waist_height_ratio, male_waist_height_ratio], 
                       labels=['Female', 'Male'], patch_artist=True)
bp1['boxes'][0].set_facecolor('hotpink')
bp1['boxes'][1].set_facecolor('steelblue')
axes[0].set_title('Waist-to-Height Ratio Comparison', fontsize=14, fontweight='bold')
axes[0].set_ylabel('Ratio', fontsize=12)
axes[0].grid(True, alpha=0.3, axis='y')

# Waist-to-hip ratio
bp2 = axes[1].boxplot([female_waist_hip_ratio, male_waist_hip_ratio], 
                       labels=['Female', 'Male'], patch_artist=True)
bp2['boxes'][0].set_facecolor('hotpink')
bp2['boxes'][1].set_facecolor('steelblue')
axes[1].set_title('Waist-to-Hip Ratio Comparison', fontsize=14, fontweight='bold')
axes[1].set_ylabel('Ratio', fontsize=12)
axes[1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('ratio_boxplots.png', dpi=300, bbox_inches='tight')
plt.show()

print("✓ Ratio box plots saved as 'ratio_boxplots.png'")

print("\n### INTERPRETATION ###")
print("The waist-to-hip ratio shows the distribution of body fat.")
print("Females typically have lower waist-to-hip ratios (more pear-shaped),")
print("while males have higher ratios (more apple-shaped distribution).")

# ============================================================================
# SECTION 11: BMI ANALYSIS - LOWEST AND HIGHEST
# ============================================================================
print("\n### SECTION 11: BMI Extremes Analysis ###\n")
print("Identifying the 5 participants with lowest and highest BMI...\n")

# Get indices
lowest_bmi_indices = np.argsort(female_bmi)[:5]
highest_bmi_indices = np.argsort(female_bmi)[-5:][::-1]

print("5 LOWEST BMI PARTICIPANTS:")
for rank, idx in enumerate(lowest_bmi_indices, 1):
    print(f"\n  Rank {rank}:")
    print(f"    BMI: {female_bmi[idx]:.2f}")
    print(f"    Weight: {female_data[idx, 0]:.2f} kg")
    print(f"    Height: {female_data[idx, 1]:.2f} cm")

print("\n\n5 HIGHEST BMI PARTICIPANTS:")
for rank, idx in enumerate(highest_bmi_indices, 1):
    print(f"\n  Rank {rank}:")
    print(f"    BMI: {female_bmi[idx]:.2f}")
    print(f"    Weight: {female_data[idx, 0]:.2f} kg")
    print(f"    Height: {female_data[idx, 1]:.2f} cm")

# BMI categories
underweight = np.sum(female_bmi < 18.5)
normal = np.sum((female_bmi >= 18.5) & (female_bmi < 25))
overweight = np.sum((female_bmi >= 25) & (female_bmi < 30))
obese = np.sum(female_bmi >= 30)

print(f"\n\nBMI CATEGORY DISTRIBUTION (Females):")
print(f"  Underweight (BMI < 18.5): {underweight} ({underweight/len(female_bmi)*100:.1f}%)")
print(f"  Normal (18.5 ≤ BMI < 25): {normal} ({normal/len(female_bmi)*100:.1f}%)")
print(f"  Overweight (25 ≤ BMI < 30): {overweight} ({overweight/len(female_bmi)*100:.1f}%)")
print(f"  Obese (BMI ≥ 30): {obese} ({obese/len(female_bmi)*100:.1f}%)")

# ============================================================================
# FINAL SUMMARY
# ============================================================================
print("\n" + "="*70)
print("ANALYSIS COMPLETE")
print("="*70)
print("\nAll visualizations have been saved:")
print("  ✓ weight_histograms.png")
print("  ✓ weight_boxplot.png")
print("  ✓ standardized_pairplot.png")
print("  ✓ correlation_heatmaps.png")
print("  ✓ ratio_boxplots.png")
print("\nThank you for using the NHANES Body Measurements Analysis tool!")
print("="*70)