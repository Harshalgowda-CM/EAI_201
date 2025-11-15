"""
Windows Version - FULL EDA SCRIPT
All paths fixed for your system.

This script will:
1. Load zoo.csv, class.csv, auxiliary_metadata.json
2. Merge + clean dataset
3. Produce 4 visualizations (Pie chart, Violin, Count plot, Heatmap)
4. Compute class imbalance + high correlations
5. Save cleaned dataset + all figures in eda_outputs/ folder
"""

import pandas as pd
import numpy as np
import json
import matplotlib.pyplot as plt
import os

# ============ FIXED WINDOWS PATH ============
DATA_DIR = r"C:\Users\ub14-glab-012\Desktop\Harshal_24UG00313"
ZOO_FILE = os.path.join(DATA_DIR, "zoo.csv")
CLASS_FILE = os.path.join(DATA_DIR, "class.csv")
AUX_FILE = os.path.join(DATA_DIR, "auxiliary_metadata.json")

OUTPUT_DIR = os.path.join(DATA_DIR, "eda_outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

FIG_FORMAT = "png"


# ===================== LOAD DATA =====================
def load_data():
    zoo = pd.read_csv(ZOO_FILE)
    class_df = pd.read_csv(CLASS_FILE)
    with open(AUX_FILE, "r") as f:
        aux = pd.DataFrame(json.load(f))
    return zoo, class_df, aux


# ===================== MERGE & CLEAN =====================
def merge_and_clean(zoo, class_df, aux):
    merged = zoo.merge(
        class_df,
        left_on="class_type",
        right_on="Class_Number",
        how="left"
    )

    merged = merged.merge(aux, on="animal_name", how="left")

    # Fix inconsistent metadata names
    merged["diet"] = merged["diet"].fillna(merged.get("diet_type")).fillna("Unknown")
    merged["habitat"] = merged["habitat"].fillna(merged.get("habitats")).fillna("Unknown")

    for col in ["diet_type", "habitats"]:
        if col in merged.columns:
            merged.drop(col, axis=1, inplace=True)

    merged["Class_Type"] = merged["Class_Type"].astype(str)
    merged["legs"] = pd.to_numeric(merged["legs"], errors="coerce")

    return merged


# ===================== PLOTS =====================
def plot_pie(df, outpath):
    plt.figure(figsize=(7, 7))
    df["Class_Type"].value_counts().plot.pie(autopct="%1.1f%%", startangle=90)
    plt.title("Figure 1 — Class Distribution (by name)")
    plt.axis("equal")
    plt.savefig(outpath, bbox_inches="tight")
    plt.show()


def plot_violin(df, outpath):
    labels = df["Class_Type"].value_counts().index.tolist()
    data = [df[df["Class_Type"] == cls]["legs"].dropna().values for cls in labels]

    fig, ax = plt.subplots(figsize=(12, 6))
    parts = ax.violinplot(data, showmedians=True)

    for i, arr in enumerate(data):
        if len(arr) == 0:
            med = 0
        else:
            med = np.median(arr)
        ax.text(i + 1, med + 0.3, f"median={med:.1f}", ha="center")

    ax.set_title("Figure 2 — Legs Distribution by Class (Violin Plot)")
    ax.set_xticks(np.arange(1, len(labels) + 1))
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.set_ylabel("Number of Legs")
    plt.tight_layout()
    plt.savefig(outpath, bbox_inches="tight")
    plt.show()


def plot_count(df, outpath):
    ct = pd.crosstab(df["habitat"], df["diet"])
    habitats = ct.index.tolist()
    diets = ct.columns.tolist()

    x = np.arange(len(habitats))
    width = 0.8 / len(diets)

    fig, ax = plt.subplots(figsize=(14, 6))
    for i, diet in enumerate(diets):
        ax.bar(x + i * width, ct[diet], width, label=diet)

    ax.set_xticks(x + width)
    ax.set_xticklabels(habitats, rotation=45, ha="right")
    ax.set_title("Figure 3 — Habitat Type by Diet (Counts)")
    ax.legend()
    plt.tight_layout()
    plt.savefig(outpath, bbox_inches="tight")
    plt.show()


def plot_heatmap(df, outpath):
    num_df = df.select_dtypes(include=[np.number])
    corr = num_df.corr()

    fig, ax = plt.subplots(figsize=(10, 8))
    cax = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)

    cols = corr.columns
    ax.set_xticks(np.arange(len(cols)))
    ax.set_yticks(np.arange(len(cols)))
    ax.set_xticklabels(cols, rotation=45, ha="right")
    ax.set_yticklabels(cols)

    for i in range(len(cols)):
        for j in range(len(cols)):
            ax.text(j, i, f"{corr.iloc[i, j]:.2f}",
                    ha="center", va="center", fontsize=8)

    fig.colorbar(cax)
    plt.title("Figure 4 — Numeric Feature Correlation Heatmap")
    plt.tight_layout()
    plt.savefig(outpath, bbox_inches="tight")
    plt.show()

    return corr


# ===================== STATS =====================
def compute_stats(df):
    print("\n=== CLASS COUNTS ===")
    counts = df["Class_Type"].value_counts()
    print(counts)

    largest = counts.max()
    smallest = counts.min()
    ratio = largest / smallest
    print(f"\nClass Imbalance Ratio = {ratio:.2f}")

    return counts, ratio


def high_corr_pairs(df, threshold=0.8):
    corr = df.select_dtypes(include=[np.number]).corr()
    cols = corr.columns
    print(f"\n=== High Correlation Pairs (|corr| > {threshold}) ===")

    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            if abs(corr.iloc[i, j]) > threshold:
                print(f"{cols[i]} <-> {cols[j]} = {corr.iloc[i, j]:.2f}")


# ===================== MAIN =====================
def main():
    zoo, class_df, aux = load_data()

    df = merge_and_clean(zoo, class_df, aux)

    # Save cleaned dataset
    df.to_csv(os.path.join(OUTPUT_DIR, "merged_cleaned_zoo.csv"), index=False)

    # Plots
    plot_pie(df, os.path.join(OUTPUT_DIR, "figure1_class_distribution.png"))
    plot_violin(df, os.path.join(OUTPUT_DIR, "figure2_legs_violin.png"))
    plot_count(df, os.path.join(OUTPUT_DIR, "figure3_habitat_diet.png"))
    corr = plot_heatmap(df, os.path.join(OUTPUT_DIR, "figure4_heatmap.png"))

    # Stats
    compute_stats(df)
    high_corr_pairs(df)


if __name__ == "__main__":
    main()
