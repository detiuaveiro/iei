import matplotlib.pyplot as plt
import numpy as np

def generate_scaling_comparison():
    # 1. Setup Data
    np.random.seed(42)
    n_points = 2000

    # Generate "Raw" Data: Stretched distribution
    # X has a large range (0-1000), Y has a small range (0-1)
    x_raw = np.random.normal(loc=500, scale=150, size=n_points)
    y_raw = np.random.normal(loc=0.5, scale=0.05, size=n_points)

    # Clip to strictly match the visual limits for neatness
    x_raw = np.clip(x_raw, 0, 1000)
    y_raw = np.clip(y_raw, 0, 1)

    # Generate "Scaled" Data: Normalized (Min-Max Scaling logic)
    # We manually normalize to 0-1 range for the visualization
    x_scaled = (x_raw - x_raw.min()) / (x_raw.max() - x_raw.min())
    y_scaled = (y_raw - y_raw.min()) / (y_raw.max() - y_raw.min())

    # 2. Plotting
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    # --- Left Plot: Raw Data ---
    axes[0].scatter(x_raw, y_raw, s=2, alpha=0.6, color='#1f77b4') # Blue
    axes[0].set_title("Raw Data", fontsize=16, fontweight='bold', pad=15)
    axes[0].set_xlim(0, 1000)
    axes[0].set_ylim(0, 1)

    # Remove top/right spines for cleaner look
    axes[0].spines['top'].set_visible(False)
    axes[0].spines['right'].set_visible(False)

    # --- Right Plot: Scaled Data ---
    # To make it look "circular" in the plot, we ensure aspect ratio is equal
    axes[1].scatter(x_scaled, y_scaled, s=2, alpha=0.6, color='#ff7f0e') # Orange
    axes[1].set_title("Scaled Data", fontsize=16, fontweight='bold', pad=15)
    axes[1].set_xlim(0, 1)
    axes[1].set_ylim(0, 1)
    axes[1].set_aspect('equal', adjustable='box')

    # Remove top/right spines
    axes[1].spines['top'].set_visible(False)
    axes[1].spines['right'].set_visible(False)

    # 3. Final Layout Adjustments
    plt.tight_layout(pad=4.0)

    # Add a dividing line visually (optional, but matches the requested image style)
    line = plt.Line2D([0.5, 0.5], [0.1, 0.9], transform=fig.transFigure, color="lightgrey")
    fig.add_artist(line)

    print("Generating plot...")
    plt.show()

if __name__ == "__main__":
    generate_scaling_comparison()