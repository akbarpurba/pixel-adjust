from PIL import Image


def process_image(image_path, alpha, beta):

    """
    =========================================
    PROCESS IMAGE RGB
    =========================================

    Rumus:

    g(x,y) = α × f(x,y) + β

    α = contrast
    β = brightness
    """

    # =========================================
    # OPEN IMAGE RGB
    # =========================================

    img = Image.open(
        image_path
    ).convert("RGB")

    width, height = img.size

    pixels = img.load()

    # =========================================
    # LOOP PIXEL
    # =========================================

    for y in range(height):

        for x in range(width):

            # =====================================
            # RGB PIXEL
            # =====================================

            r, g, b = pixels[x, y]

            # =====================================
            # ARITHMETIC OPERATION
            # =====================================

            new_r = int(
                (alpha * r) + beta
            )

            new_g = int(
                (alpha * g) + beta
            )

            new_b = int(
                (alpha * b) + beta
            )

            # =====================================
            # CLIPPING
            # =====================================

            new_r = max(
                0,
                min(255, new_r)
            )

            new_g = max(
                0,
                min(255, new_g)
            )

            new_b = max(
                0,
                min(255, new_b)
            )

            # =====================================
            # SAVE PIXEL
            # =====================================

            pixels[x, y] = (
                new_r,
                new_g,
                new_b
            )

    return img