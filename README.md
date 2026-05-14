============================================================================
# PixelAdjust App - Brightness & Contrast Editor
================================================================================

Aplikasi pengolahan citra digital berbasis GUI untuk mengatur kecerahan 
(brightness) dan kontras (contrast) menggunakan operasi aritmetika citra 
dengan rumus: g(x,y) = α × f(x,y) + β

================================================================================
## PERSYARATAN INSTALASI
================================================================================

- Python 3.7 atau lebih baru
- pip (Python package manager)

================================================================================
## CARA INSTALASI
================================================================================

1. **Clone repository:**
```bash
   git clone https://github.com/akbarpurba/pixel-adjust.git
   cd project-brightness-contrast
```

2. **Install dependencies:**
```bash
   pip install -r requirements.txt
```

3. **Jalankan aplikasi:**
```bash
   python main.py
```

================================================================================
## FITUR
================================================================================

✓ **Brightness control** (-100 s/d 100)
✓ **Contrast control** (0.1 s/d 3.0)
✓ **Preview hasil real-time**
✓ **Save image hasil pemrosesan**
✓ **Informasi nilai RGB pixel (0,0)**
✓ **Compare plot** (histogram, matriks RGB, perhitungan manual)
✓ **Loading animation saat proses**
✓ **Reset slider ke nilai default**

================================================================================
## PENUTUP
================================================================================

Aplikasi ini dikembangkan untuk memenuhi tugas mata kuliah Pengolahan Citra 
Digital. Operasi brightness dan contrast menerapkan operasi aritmetika citra 
dengan clipping nilai pixel 0-255.

Dibuat oleh: **Akbar Maulana Purba**, **Sinta Suwanda** dan **Maira Maulydia**
================================================================================
