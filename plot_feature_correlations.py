import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Extract data for each participant from df_final
x_p1, y_p1 = df_final[0]  # Data for participant 1
x_p2, y_p2 = df_final[1]  # Data for participant 2

# Create DataFrames for each participant
df_p1 = x_p1.join(y_p1)
df_p2 = x_p2.join(y_p2)

# Extract the relevant columns for each participant (similar to df_means)
df_p1_means = df_p1.iloc[:, np.r_[0:56, -1]]
df_p2_means = df_p2.iloc[:, np.r_[0:56, -1]]

# Clean column names for each participant
features_p1 = df_p1_means.columns.tolist()
features_p2 = df_p2_means.columns.tolist()
features_clean_p1 = clean_column_names(features_p1, True)
features_clean_p2 = clean_column_names(features_p2, True)
df_p1_clean = df_p1_means.copy()
df_p2_clean = df_p2_means.copy()
df_p1_clean.columns = features_clean_p1
df_p2_clean.columns = features_clean_p2

# Calculate correlations with F-ISA for each participant
corr_p1 = df_p1_clean.corr()['F-ISA'].drop('F-ISA')
corr_p2 = df_p2_clean.corr()['F-ISA'].drop('F-ISA')

# Create a DataFrame to hold both sets of correlations
combined_corr = pd.DataFrame({
    'Participant 1': corr_p1,
    'Participant 2': corr_p2
})

# Sort the DataFrame by Participant 2's correlation values in ascending order
combined_corr = combined_corr.sort_values(by='Participant 2', ascending=True)

# Reshape for seaborn (convert to long format)
combined_corr_long = combined_corr.reset_index().melt(
    id_vars='index', 
    var_name='Participant', 
    value_name='Correlation'
)

# Set up the figure with a larger size and better DPI
plt.figure(figsize=(16, 14), dpi=300)

# Set the style with a clean white background
sns.set_style("whitegrid")
sns.set_context("paper", font_scale=1.2)

# Create the grouped bar chart with improved spacing
ax = sns.barplot(
    x='Correlation', 
    y='index', 
    hue='Participant', 
    data=combined_corr_long,
    saturation=1.0,
    width=0.85,  # Slightly reduced width for better spacing
    palette=['#1f77b4', '#ff7f0e']  # Explicitly set the colors
)

# Add horizontal separator lines between features with improved visibility
feature_names = combined_corr.index.tolist()
for i in range(1, len(feature_names)):
    line_pos = i - 0.5
    plt.axhline(y=line_pos, color='gray', linestyle='-', alpha=0.3, linewidth=0.5)

# Add a vertical line at x=0 with improved visibility
plt.axvline(x=0, color='black', linestyle='-', alpha=0.7, linewidth=1.0)

# Customize the appearance with improved typography and spacing
plt.xlabel('Correlation with F-ISA', fontsize=14, fontweight='bold', labelpad=10)
plt.ylabel('Features', fontsize=14, fontweight='bold', labelpad=10)
plt.title('Feature Correlations with F-ISA by Participant', fontsize=16, fontweight='bold', pad=20)

# Improve the legend
plt.legend(
    title='Participant',
    title_fontsize=12,
    fontsize=11,
    bbox_to_anchor=(1.02, 1),
    loc='upper left',
    borderaxespad=0
)

# Customize the grid
plt.grid(axis='x', alpha=0.2, linestyle='--')

# Adjust the layout to prevent label cutoff
plt.tight_layout()

# Add a subtle border around the plot
for spine in plt.gca().spines.values():
    spine.set_visible(True)
    spine.set_color('gray')
    spine.set_linewidth(0.5)

# Show the plot
plt.savefig("figures/feature_corr_by_participant.png", bbox_inches='tight', dpi=300) 