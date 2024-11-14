import numpy as np
import pandas as pd
from scipy.stats import shapiro, friedmanchisquare, f_oneway
from scipy.stats import wilcoxon

# Step 1: Data input
data = {
    'Region Pair': ['V1-V2', 'V1-V3', 'V2-V3', 'V1-hMT+', 'V2-hMT+', 'V3-hMT+',
                    'V1-V2', 'V1-V3', 'V2-V3', 'V1-hMT+', 'V2-hMT+', 'V3-hMT+'],
    'Hemisphere': ['Left', 'Left', 'Left', 'Left', 'Left', 'Left', 'Right', 'Right', 'Right', 'Right', 'Right',
                   'Right'],
    'Bielschowsky': [0.994, 0.997, 0.996, 0.993, 0.995, 0.996, 0.999, 0.993, 0.996, 0.998, 0.998, 0.995],
    'Thionin': [0.994, 0.985, 0.996, 0.961, 0.963, 0.948, 0.999, 0.998, 0.999, 0.988, 0.989, 0.989],
    'Parvalbumin': [0.997, 0.989, 0.991, 0.942, 0.921, 0.917, 0.995, 0.978, 0.974, 0.938, 0.925, 0.981]
}

df = pd.DataFrame(data)

# Step 2: Fisher Z-transformation
def fisher_z_transform(r):
    return 0.5 * np.log((1 + r) / (1 - r))

df['Bielschowsky_Z'] = df['Bielschowsky'].apply(fisher_z_transform)
df['Thionin_Z'] = df['Thionin'].apply(fisher_z_transform)
df['Parvalbumin_Z'] = df['Parvalbumin'].apply(fisher_z_transform)

# Step 3: Compute descriptive statistics (means and standard deviations)
means = df[['Bielschowsky_Z', 'Thionin_Z', 'Parvalbumin_Z']].mean()
std_devs = df[['Bielschowsky_Z', 'Thionin_Z', 'Parvalbumin_Z']].std()

print("Means:\n", means)
print("\nStandard Deviations:\n", std_devs)

# Step 4: Check for normality with Shapiro-Wilk test
_, p_biel = shapiro(df['Bielschowsky_Z'])
_, p_thio = shapiro(df['Thionin_Z'])
_, p_parv = shapiro(df['Parvalbumin_Z'])

print("\nShapiro-Wilk p-values:")
print(f"Bielschowsky: {p_biel}, Thionin: {p_thio}, Parvalbumin: {p_parv}")

# Step 5: Perform the appropriate statistical test

# If normal, run ANOVA
if p_biel > 0.05 and p_thio > 0.05 and p_parv > 0.05:
    print("\nData is normally distributed. Running ANOVA...")
    F_stat, p_anova = f_oneway(df['Bielschowsky_Z'], df['Thionin_Z'], df['Parvalbumin_Z'])
    print(f"ANOVA result: F = {F_stat}, p = {p_anova}")

    # Post-hoc analysis (if significant)
    if p_anova < 0.05:
        print("Significant result, performing post-hoc analysis...")
        print("Pairwise comparisons using Wilcoxon signed-rank test (non-parametric post-hoc)...")
        _, p_b_t = wilcoxon(df['Bielschowsky_Z'], df['Thionin_Z'])
        _, p_b_p = wilcoxon(df['Bielschowsky_Z'], df['Parvalbumin_Z'])
        _, p_t_p = wilcoxon(df['Thionin_Z'], df['Parvalbumin_Z'])
        print(f"Bielschowsky vs Thionin: p = {p_b_t}")
        print(f"Bielschowsky vs Parvalbumin: p = {p_b_p}")
        print(f"Thionin vs Parvalbumin: p = {p_t_p}")

        # Apply Bonferroni correction (multiply p-values by 3)
        p_b_t_corr = min(p_b_t * 3, 1.0)  # Ensure that the corrected p-value is <= 1
        p_b_p_corr = min(p_b_p * 3, 1.0)
        p_t_p_corr = min(p_t_p * 3, 1.0)

        # Print corrected p-values
        print(f"Bielschowsky vs Thionin: p (uncorrected) = {p_b_t}, p (Bonferroni corrected) = {p_b_t_corr}")
        print(f"Bielschowsky vs Parvalbumin: p (uncorrected) = {p_b_p}, p (Bonferroni corrected) = {p_b_p_corr}")
        print(f"Thionin vs Parvalbumin: p (uncorrected) = {p_t_p}, p (Bonferroni corrected) = {p_t_p_corr}")

# If not normal, run Friedman test
else:
    print("\nData is not normally distributed. Running Friedman test...")
    stat, p_friedman = friedmanchisquare(df['Bielschowsky_Z'], df['Thionin_Z'], df['Parvalbumin_Z'])
    print(f"Friedman result: chi-square = {stat}, p = {p_friedman}")

    # Post-hoc analysis (if significant)
    if p_friedman < 0.05:
        print("Significant result, performing post-hoc analysis...")
        print("Pairwise comparisons using Wilcoxon signed-rank test (non-parametric post-hoc)...")
        _, p_b_t = wilcoxon(df['Bielschowsky_Z'], df['Thionin_Z'])
        _, p_b_p = wilcoxon(df['Bielschowsky_Z'], df['Parvalbumin_Z'])
        _, p_t_p = wilcoxon(df['Thionin_Z'], df['Parvalbumin_Z'])
        print(f"Bielschowsky vs Thionin: p = {p_b_t}")
        print(f"Bielschowsky vs Parvalbumin: p = {p_b_p}")
        print(f"Thionin vs Parvalbumin: p = {p_t_p}")
