import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


# ==========================================
# HISTOGRAM
# ==========================================

def compute_histogram(image_path):

    img = Image.open(image_path).convert("RGB")

    matrix = np.array(img)

    red_channel = matrix[:, :, 0]

    pixels = red_channel.flatten()

    histogram = [0] * 256

    for pixel in pixels:
        histogram[pixel] += 1

    return histogram, matrix


# ==========================================
# FORMAT MATRIX RGB
# ==========================================

def matrix_to_text(matrix, title):
    """
    Mengubah matriks RGB menjadi format teks
    """
    text = f"{title}\n\n"
    
    for i, row in enumerate(matrix):
        row_text = ""
        for j, pixel in enumerate(row):
            r = int(pixel[0])
            g = int(pixel[1])
            b = int(pixel[2])
            row_text += f"[{r:3d},{g:3d},{b:3d}]   "
        text += row_text + "\n\n"
    
    return text


# ==========================================
# VISUALISASI
# ==========================================

def compare_plot(
    original_path,
    result_path,
    alpha,
    beta
):

    # ======================================
    # LOAD DATA
    # ======================================

    hist_original, mat_original = (
        compute_histogram(original_path)
    )

    mat_result = np.array(result_path)

    red_channel = mat_result[:, :, 0]

    pixels = red_channel.flatten()

    hist_result = [0] * 256

    for pixel in pixels:
        hist_result[pixel] += 1

    intensity = list(range(256))

    # ======================================
    # MATRIX RGB 3x3
    # ======================================

    # Ambil 3x3 pixel dari pojok kiri atas
    original_3x3 = mat_original[10:13, 10:11]
    result_3x3 = mat_result[10:13, 10:11]

    # Format matriks dengan judul yang berbeda
    original_text = matrix_to_text(
        original_3x3, 
        "MATRIKS RGB (3x3) - CITRA ORIGINAL"
    )

    result_text = matrix_to_text(
        result_3x3, 
        "MATRIKS RGB (3x3) - CITRA HASIL"
    )

    # ======================================
    # PIXEL SAMPLE (0,0) → dianggap sebagai f(1,1)
    # ======================================

    pixel_original = mat_original[0][0]
    pixel_result = mat_result[0][0]

    f11_R = int(pixel_original[0])
    f11_G = int(pixel_original[1])
    f11_B = int(pixel_original[2])

    R_result = int(pixel_result[0])
    G_result = int(pixel_result[1])
    B_result = int(pixel_result[2])

    # ======================================
    # PERHITUNGAN MANUAL dengan indeks f(1,1)
    # ======================================

    R_calc = (alpha * f11_R) + beta
    G_calc = (alpha * f11_G) + beta
    B_calc = (alpha * f11_B) + beta

    R_final = int(np.clip(R_calc, 0, 255))
    G_final = int(np.clip(G_calc, 0, 255))
    B_final = int(np.clip(B_calc, 0, 255))

    # ======================================
    # STATUS CLIPPING
    # ======================================

    clipping_info = []

    if R_calc > 255 or R_calc < 0:
        clipping_info.append(f"f(1,1)_R: {R_calc:.2f} → {R_final}")

    if G_calc > 255 or G_calc < 0:
        clipping_info.append(f"f(1,1)_G: {G_calc:.2f} → {G_final}")

    if B_calc > 255 or B_calc < 0:
        clipping_info.append(f"f(1,1)_B: {B_calc:.2f} → {B_final}")

    if len(clipping_info) == 0:
        clipping_text = "Tidak terjadi clipping"
    else:
        clipping_text = "\n".join(clipping_info)

    # ======================================
    # FORMAT BETA UNTUK TAMPILAN
    # ======================================
    
    if beta >= 0:
        beta_display = f"+ {beta:.0f}"
    else:
        beta_display = f"+ ({beta:.0f})"

    # ======================================
    # FIGURE
    # ======================================

    fig, ax = plt.subplots(
        1,
        3,
        figsize=(20, 6)
    )

    fig.patch.set_facecolor("#0f172a")

    # ======================================
    # PANEL 1: HISTOGRAM
    # ======================================

    ax[0].set_facecolor("#1e293b")

    ax[0].plot(
        intensity,
        hist_original,
        color="#3b82f6",
        linewidth=2,
        label="Citra Original"
    )

    ax[0].plot(
        intensity,
        hist_result,
        color="#ef4444",
        linewidth=2,
        label="Citra Hasil"
    )

    ax[0].set_title(
        "Perbandingan Histogram (Channel Red)",
        color="white",
        fontsize=13,
        fontweight="bold"
    )

    ax[0].set_xlabel("Intensitas Pixel", color="white")
    ax[0].set_ylabel("Frekuensi", color="white")
    ax[0].tick_params(colors="white")
    ax[0].grid(linestyle="--", alpha=0.2, color="white")

    ax[0].legend(
        facecolor="#1e293b",
        edgecolor="#475569",
        labelcolor="white"
    )

    # ======================================
    # PANEL 2: MATRIKS RGB (ORIGINAL VS HASIL)
    # ======================================

    ax[1].axis("off")
    ax[1].set_facecolor("#1e293b")

    # Gabungkan kedua matriks dalam satu tampilan
    combined_text = f"{original_text}\n\n{result_text}"

    ax[1].text(
        0.5,
        0.5,
        combined_text,
        fontsize=8,
        family="monospace",
        color="white",
        ha="center",
        va="center",
        transform=ax[1].transAxes,
        bbox=dict(
            facecolor="#0f172a",
            edgecolor="#3b82f6",
            boxstyle="round,pad=0.8"
        )
    )

    ax[1].set_title(
        "Perbandingan Matriks RGB (3x3)",
        color="white",
        fontsize=13,
        fontweight="bold"
    )

    # ======================================
    # PANEL 3: PERHITUNGAN
    # ======================================

    ax[2].axis("off")
    ax[2].set_facecolor("#1e293b")

    operation_text = f"""
OPERASI BRIGHTNESS & CONTRAST
─────────────────────────────────────────

Rumus:
g(x,y) = α × f(x,y) + β

Parameter:
α (Kontras) = {alpha:.2f}
β (Kecerahan) = {beta:.0f}

─────────────────────────────────────────
PIXEL SAMPLE
─────────────────────────────────────────

f(1,1) = ({f11_R}, {f11_G}, {f11_B})

Hasil Sistem = ({R_result}, {G_result}, {B_result})

─────────────────────────────────────────
PERHITUNGAN MANUAL
─────────────────────────────────────────

f(1,1) = {alpha:.2f} × {f11_R} {beta_display}
       = {R_calc:.2f}
       = {R_final}

f(1,2) = {alpha:.2f} × {f11_G} {beta_display}
       = {G_calc:.2f}
       = {G_final}

f(1,3) = {alpha:.2f} × {f11_B} {beta_display}
       = {B_calc:.2f}
       = {B_final}

─────────────────────────────────────────
STATUS CLIPPING
─────────────────────────────────────────
{clipping_text}
"""

    ax[2].text(
        0.5,
        0.5,
        operation_text,
        fontsize=8.5,
        family="monospace",
        color="#0f172a",
        ha="center",
        va="center",
        transform=ax[2].transAxes,
        bbox=dict(
            facecolor="#f8fafc",
            edgecolor="#3b82f6",
            boxstyle="round,pad=0.8"
        )
    )

    # ======================================
    # TAMPILKAN
    # ======================================

    plt.tight_layout()
    plt.show()