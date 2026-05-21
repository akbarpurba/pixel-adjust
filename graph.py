import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


# ==========================================
# HISTOGRAM
# ==========================================

def compute_histogram(image):
    matrix = np.array(image)
    red_channel = matrix[:, :, 0]
    pixels = red_channel.flatten()
    histogram = [0] * 256

    for pixel in pixels:
        histogram[pixel] += 1

    return histogram, matrix


# ==========================================
# FORMAT MATRIX
# ==========================================

def format_matrix(matrix):
    rows = []
    for row in matrix:
        row_text = ""
        for value in row:
            row_text += f"{int(value):3d} "
        rows.append(row_text)
    return "\n".join(rows)


# ==========================================
# COMPARE PLOT
# ==========================================

def compare_plot(original_path, result_image, alpha, beta):
    # ======================================
    # ORIGINAL IMAGE
    # ======================================
    original_img = Image.open(original_path).convert("RGB")

    # ======================================
    # HISTOGRAM
    # ======================================
    hist_original, mat_original = compute_histogram(original_img)
    hist_result, mat_result = compute_histogram(result_image)
    intensity = list(range(256))

    # ======================================
    # RGB CHANNEL MATRIX 5x5
    # ======================================
    R_original = mat_original[0:5, 0:5, 0]
    G_original = mat_original[0:5, 0:5, 1]
    B_original = mat_original[0:5, 0:5, 2]

    R_result = mat_result[0:5, 0:5, 0]
    G_result = mat_result[0:5, 0:5, 1]
    B_result = mat_result[0:5, 0:5, 2]

    # ======================================
    # SAMPLE PIXEL
    # ======================================
    r = int(mat_original[0][0][0])
    g = int(mat_original[0][0][1])
    b = int(mat_original[0][0][2])

    # ======================================
    # MANUAL CALCULATION
    # ======================================
    calc_r = (alpha * r) + beta
    calc_g = (alpha * g) + beta
    calc_b = (alpha * b) + beta

    final_r = int(np.clip(calc_r, 0, 255))
    final_g = int(np.clip(calc_g, 0, 255))
    final_b = int(np.clip(calc_b, 0, 255))

    # ======================================
    # FIGURE
    # ======================================
    fig, ax = plt.subplots(1, 3, figsize=(24, 8))
    fig.patch.set_facecolor("#0f172a")

    # ======================================
    # PANEL 1 - HISTOGRAM
    # ======================================
    ax[0].set_facecolor("#1e293b")
    ax[0].plot(intensity, hist_original, linewidth=2, color="#60a5fa", label="Original")
    ax[0].plot(intensity, hist_result, linewidth=2, color="#f87171", label="Result")
    ax[0].set_title("Image Analysis Histogram", color="white", fontweight="bold")
    ax[0].set_xlabel("Pixel Intensity", color="white")
    ax[0].set_ylabel("Frequency", color="white")
    ax[0].tick_params(colors="white")
    ax[0].grid(linestyle="--", alpha=0.2)
    legend = ax[0].legend()
    for text in legend.get_texts():
        text.set_color("white")

    # ======================================
    # PANEL 2 - MATRIX (FORMAT 3 KOLOM DENGAN UKURAN FONT 9)
    # ======================================
    ax[1].axis("off")
    ax[1].set_facecolor("#0f172a")
    ax[1].set_title("RGB Matrix 5x5 Comparison", color="white", fontweight="bold", fontsize=14, pad=20)

    # HEADER ORIGINAL
    ax[1].text(0.67, 0.94, "ORIGINAL IMAGE", fontsize=12, fontweight="bold", 
               color="#60a5fa", ha="center", transform=ax[1].transAxes)
    
    # LABEL CHANNEL ORIGINAL
    ax[1].text(0.17, 0.88, "RED", fontsize=10, fontweight="bold", 
               color="#f87171", ha="center", transform=ax[1].transAxes)
    ax[1].text(0.67, 0.88, "GREEN", fontsize=10, fontweight="bold", 
               color="#4ade80", ha="center", transform=ax[1].transAxes)
    ax[1].text(1.17, 0.88, "BLUE", fontsize=10, fontweight="bold", 
               color="#60a5fa", ha="center", transform=ax[1].transAxes)

    # RED ORIGINAL MATRIX (fontsize=9)
    ax[1].text(0.17, 0.82, format_matrix(R_original), fontsize=9, family="monospace", 
               color="#f87171", ha="center", va="top", transform=ax[1].transAxes,
               bbox=dict(facecolor="#1e293b", edgecolor="#ef4444", boxstyle="round,pad=0.5"))
    
    # GREEN ORIGINAL MATRIX (fontsize=9)
    ax[1].text(0.67, 0.82, format_matrix(G_original), fontsize=9, family="monospace", 
               color="#4ade80", ha="center", va="top", transform=ax[1].transAxes,
               bbox=dict(facecolor="#1e293b", edgecolor="#22c55e", boxstyle="round,pad=0.5"))
    
    # BLUE ORIGINAL MATRIX (fontsize=9)
    ax[1].text(1.17, 0.82, format_matrix(B_original), fontsize=9, family="monospace", 
               color="#60a5fa", ha="center", va="top", transform=ax[1].transAxes,
               bbox=dict(facecolor="#1e293b", edgecolor="#3b82f6", boxstyle="round,pad=0.5"))

    # HEADER RESULT
    ax[1].text(0.67, 0.62, "RESULT IMAGE", fontsize=12, fontweight="bold", 
               color="#f87171", ha="center", transform=ax[1].transAxes)
    
    # LABEL CHANNEL RESULT
    ax[1].text(0.17, 0.56, "RED", fontsize=10, fontweight="bold", 
               color="#f87171", ha="center", transform=ax[1].transAxes)
    ax[1].text(0.67, 0.56, "GREEN", fontsize=10, fontweight="bold", 
               color="#4ade80", ha="center", transform=ax[1].transAxes)
    ax[1].text(1.17, 0.56, "BLUE", fontsize=10, fontweight="bold", 
               color="#60a5fa", ha="center", transform=ax[1].transAxes)

    # RED RESULT MATRIX (fontsize=9)
    ax[1].text(0.17, 0.50, format_matrix(R_result), fontsize=9, family="monospace", 
               color="#f87171", ha="center", va="top", transform=ax[1].transAxes,
               bbox=dict(facecolor="#1e293b", edgecolor="#ef4444", boxstyle="round,pad=0.5"))
    
    # GREEN RESULT MATRIX (fontsize=9)
    ax[1].text(0.67, 0.50, format_matrix(G_result), fontsize=9, family="monospace", 
               color="#4ade80", ha="center", va="top", transform=ax[1].transAxes,
               bbox=dict(facecolor="#1e293b", edgecolor="#22c55e", boxstyle="round,pad=0.5"))
    
    # BLUE RESULT MATRIX (fontsize=9)
    ax[1].text(1.17, 0.50, format_matrix(B_result), fontsize=9, family="monospace", 
               color="#60a5fa", ha="center", va="top", transform=ax[1].transAxes,
               bbox=dict(facecolor="#1e293b", edgecolor="#3b82f6", boxstyle="round,pad=0.5"))

    # ======================================
    # PANEL 3 - CALCULATION
    # ======================================
    ax[2].axis("off")
    ax[2].set_facecolor("#0f172a")

    operation_text = f"""
BRIGHTNESS & CONTRAST

Rumus:
g(x,y) = α × f(x,y) + β

α = {alpha:.2f}
β = {beta:.0f}

──────────────────────────

RED(1,1)
({alpha:.2f} × {r}) + ({beta:.0f})
= {calc_r:.2f}
= {final_r}

──────────────────────────

GREEN(1,1)
({alpha:.2f} × {g}) + ({beta:.0f})
= {calc_g:.2f}
= {final_g}

──────────────────────────

BLUE(1,1)
({alpha:.2f} × {b}) + ({beta:.0f})
= {calc_b:.2f}
= {final_b}

──────────────────────────

HASIL RGB(1,1): [{final_r}, {final_g}, {final_b}]
"""

    ax[2].text(0.5, 0.5, operation_text, fontsize=9, family="monospace", 
               color="#0f172a", ha="center", va="center", transform=ax[2].transAxes,
               bbox=dict(facecolor="#f8fafc", edgecolor="#3b82f6", boxstyle="round,pad=0.8"))

    ax[2].set_title("Pixel Calculation", color="white", fontweight="bold", fontsize=14, pad=20)

    # ======================================
    # LAYOUT
    # ======================================
    plt.tight_layout()
    plt.show()