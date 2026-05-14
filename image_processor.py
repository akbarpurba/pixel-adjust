from PIL import Image
import numpy as np


def process_image(image_path, alpha, beta):
    """
    =========================================
    PROCESS IMAGE RGB
    =========================================

    alpha = contrast
    beta = brightness

    Rumus:
    g(x,y) = α × f(x,y) + β
    """

    # =========================================
    # MEMBUKA GAMBAR RGB
    # =========================================

    img = Image.open(image_path).convert("RGB")

    # =========================================
    # UBAH KE ARRAY NUMPY
    # =========================================

    matrix = np.asarray(
        img,
        dtype=np.float32
    )

    # =========================================
    # OPERASI BRIGHTNESS & CONTRAST
    # =========================================

    result = (alpha * matrix) + beta

    # =========================================
    # CLIPPING PIXEL
    # =========================================

    result = np.clip(
        result,
        0,
        255
    )

    # =========================================
    # KONVERSI UINT8
    # =========================================

    result = result.astype(
        np.uint8
    )

    # =========================================
    # KEMBALIKAN KE IMAGE
    # =========================================

    result_img = Image.fromarray(
        result
    )

    return result_img