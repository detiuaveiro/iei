import matplotlib.pyplot as plt
# PdfPages is no longer needed
import seaborn as sns
import pandas as pd
import numpy as np

def generate_analysis_pdf():
    # 1. Setup Synthetic Data
    np.random.seed(42)
    n = 300
    
    data = {
        'age': np.random.normal(35, 10, n).astype(int),
        'salary': np.random.normal(60000, 15000, n),
        'department': np.random.choice(['Sales', 'Eng', 'HR'], n),
        'performance_score': np.random.uniform(1, 10, n)
    }
    # Add correlation: higher age -> slightly higher salary
    data['salary'] += (data['age'] * 500)
    
    df = pd.DataFrame(data)

    # 2. Generate Separate PDFs
    
    # --- Plot 1: Distribution (Univariate) ---
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.histplot(data=df, x="salary", kde=True, color="skyblue", ax=ax1)
    
    ax1.set_title("1. Distribution: Salary Histogram + KDE", fontsize=14, fontweight='bold')
    ax1.set_xlabel("Salary")
    
    # Transparency settings
    fig1.patch.set_alpha(0.0)
    ax1.patch.set_alpha(0.0)
    
    fig1.savefig("01_distribution.pdf", transparent=True)
    plt.close(fig1)

    # --- Plot 2: Correlation (Bivariate) ---
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=df, x="age", y="salary", hue="department", palette="deep", ax=ax2)
    
    ax2.set_title("2. Correlation: Age vs Salary", fontsize=14, fontweight='bold')
    
    # Transparency settings
    fig2.patch.set_alpha(0.0)
    ax2.patch.set_alpha(0.0)
    
    fig2.savefig("02_correlation.pdf", transparent=True)
    plt.close(fig2)

    # --- Plot 3: Comparison (Box Plot) ---
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=df, x="department", y="salary", palette="pastel", ax=ax3)
    
    ax3.set_title("3. Comparison: Salary by Dept (Box Plot)", fontsize=14, fontweight='bold')
    ax3.set_xlabel("Department")
    ax3.set_ylabel("Salary")
    
    # Transparency settings
    fig3.patch.set_alpha(0.0)
    ax3.patch.set_alpha(0.0)
    
    fig3.savefig("03_boxplot.pdf", transparent=True)
    plt.close(fig3)

    # --- Plot 4: Comparison (Violin Plot) ---
    fig4, ax4 = plt.subplots(figsize=(10, 6))
    sns.violinplot(data=df, x="department", y="salary", palette="muted", split=True, ax=ax4)
    
    ax4.set_title("4. Comparison: Salary Density (Violin Plot)", fontsize=14, fontweight='bold')
    ax4.set_xlabel("Department")
    ax4.set_ylabel("Salary")
    
    # Transparency settings
    fig4.patch.set_alpha(0.0)
    ax4.patch.set_alpha(0.0)
    
    fig4.savefig("04_violinplot.pdf", transparent=True)
    plt.close(fig4)
        
    print("Successfully generated 4 separate PDF files.")

if __name__ == "__main__":
    # Settings for nicer visuals
    sns.set_theme(style="whitegrid")
    generate_analysis_pdf()
