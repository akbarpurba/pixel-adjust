import sys
import numpy as np

from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
    QSlider,
    QApplication,
    QFrame,
    QSizePolicy,
)

from PyQt5.QtGui import (
    QPixmap,
    QFont,
    QMovie,
    QImage
)

from PyQt5.QtCore import (
    Qt,
    QTimer,
    QSize,
    QThread,
    pyqtSignal,
)

from PIL import Image, ImageDraw, ImageFont

from image_processor import process_image
from graph import compare_plot


# =====================================
# WATERMARK CONFIGURATION
# =====================================

# Konfigurasi Watermark - Ubah di sini dengan mudah!
WM_CONFIG = {
    'size_percent': 0.25,      # Ukuran watermark (persentase dari ukuran gambar)
    'position_offset': 30,      # Jarak dari tepi (pixel)
    'positions': ['bottom_right'],  # Posisi: 'top_left', 'top_right', 'bottom_left', 'bottom_right'
    'opacity': 150,            # Opasitas watermark (0-255, 255 = tidak transparan)
}


# =====================================
# THREAD PROCESS IMAGE
# =====================================

class ProcessThread(QThread):

    finished = pyqtSignal(object)

    def __init__(self, image_path, alpha, beta):

        super().__init__()

        self.image_path = image_path
        self.alpha = alpha
        self.beta = beta

    def run(self):

        result = process_image(
            self.image_path,
            self.alpha,
            self.beta
        )

        self.finished.emit(result)


# =====================================
# THREAD FOR GRAPH
# =====================================

class GraphThread(QThread):

    finished = pyqtSignal()

    def __init__(self, original_path, result, alpha, beta):

        super().__init__()

        self.original_path = original_path
        self.result = result
        self.alpha = alpha
        self.beta = beta

    def run(self):

        compare_plot(
            self.original_path,
            self.result,
            self.alpha,
            self.beta
        )

        self.finished.emit()


# =====================================
# MAIN WINDOW
# =====================================

class ImageEditor(QWidget):

    def __init__(self):

        super().__init__()

        self.image_path = None
        self.current_result = None
        self.process_thread = None
        self.graph_thread = None

        # =====================================
        # WINDOW
        # =====================================

        self.setWindowTitle(
            "PixelAdjust App"
        )

        self.resize(1200, 800)

        self.setMinimumSize(
            1000,
            700
        )

        # =====================================
        # TITLE
        # =====================================

        self.title = QLabel(
            "PixelAdjust"
        )

        self.title.setFont(
            QFont(
                "Segoe UI",
                22,
                QFont.Bold
            )
        )

        self.title.setAlignment(
            Qt.AlignCenter
        )

        self.subtitle = QLabel(
            "Digital Image Processing using RGB Matrix"
        )

        self.subtitle.setAlignment(
            Qt.AlignCenter
        )

        self.subtitle.setStyleSheet(
            "color: #94a3b8;"
        )

        # =====================================
        # IMAGE FRAME
        # =====================================

        self.original_frame = QFrame()
        self.result_frame = QFrame()

        self.original_frame.setObjectName(
            "imageFrame"
        )

        self.result_frame.setObjectName(
            "imageFrame"
        )

        self.original_frame.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

        self.result_frame.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

        # =====================================
        # IMAGE TITLE
        # =====================================

        self.original_title = QLabel(
            "Original Image"
        )

        self.result_title = QLabel(
            "Processed Image"
        )

        # =====================================
        # IMAGE LABEL
        # =====================================

        self.original_label = QLabel()
        self.result_label = QLabel()

        self.original_label.setAlignment(
            Qt.AlignCenter
        )

        self.result_label.setAlignment(
            Qt.AlignCenter
        )

        self.original_label.setMinimumSize(
            300,
            250
        )

        self.result_label.setMinimumSize(
            300,
            250
        )

        self.original_label.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

        self.result_label.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

        # =====================================
        # IMAGE LAYOUT
        # =====================================

        left_layout = QVBoxLayout()

        left_layout.addWidget(
            self.original_title
        )

        left_layout.addWidget(
            self.original_label
        )

        right_layout = QVBoxLayout()

        right_layout.addWidget(
            self.result_title
        )

        right_layout.addWidget(
            self.result_label
        )

        self.original_frame.setLayout(
            left_layout
        )

        self.result_frame.setLayout(
            right_layout
        )

        image_layout = QHBoxLayout()

        image_layout.setSpacing(20)

        image_layout.addWidget(
            self.original_frame
        )

        image_layout.addWidget(
            self.result_frame
        )

        # =====================================
        # BUTTON
        # =====================================

        self.open_button = QPushButton(
            "Open Image"
        )

        self.save_button = QPushButton(
            "Save Result"
        )

        self.reset_button = QPushButton(
            "Reset"
        )

        self.graph_button = QPushButton(
            "Image Analysis"
        )

        self.exit_button = QPushButton(
            "Exit"
        )

        self.open_button.clicked.connect(
            self.open_image
        )

        self.save_button.clicked.connect(
            self.save_image
        )

        self.reset_button.clicked.connect(
            self.reset_slider
        )

        self.graph_button.clicked.connect(
            self.show_compare_plot
        )

        self.exit_button.clicked.connect(
            self.close
        )

        buttons = [
            self.open_button,
            self.save_button,
            self.reset_button,
            self.graph_button,
            self.exit_button
        ]

        for button in buttons:

            button.setMinimumHeight(45)
            button.setMaximumWidth(180)

        button_layout = QHBoxLayout()

        button_layout.setSpacing(15)

        button_layout.setAlignment(
            Qt.AlignCenter
        )

        for button in buttons:

            button_layout.addWidget(
                button
            )

        # =====================================
        # BRIGHTNESS
        # =====================================

        self.brightness_label = QLabel(
            "Brightness : 0"
        )

        self.brightness_slider = QSlider(
            Qt.Horizontal
        )

        self.brightness_slider.setMinimum(-100)
        self.brightness_slider.setMaximum(100)
        self.brightness_slider.setValue(0)

        # =====================================
        # CONTRAST
        # =====================================

        self.contrast_label = QLabel(
            "Contrast : 1.0"
        )

        self.contrast_slider = QSlider(
            Qt.Horizontal
        )

        self.contrast_slider.setMinimum(1)
        self.contrast_slider.setMaximum(30)
        self.contrast_slider.setValue(10)

        # =====================================
        # TIMER
        # =====================================

        self.update_timer = QTimer()

        self.update_timer.setSingleShot(True)

        self.update_timer.timeout.connect(
            self.update_image
        )

        self.brightness_slider.valueChanged.connect(
            self.start_update_timer
        )

        self.contrast_slider.valueChanged.connect(
            self.start_update_timer
        )

        # =====================================
        # PIXEL INFO
        # =====================================

        self.pixel_info = QLabel(
            "Pixel [1,1] RGB : -"
        )

        # =====================================
        # CONTROL PANEL
        # =====================================

        self.control_panel = QFrame()

        self.control_panel.setObjectName(
            "controlPanel"
        )

        control_layout = QVBoxLayout()

        control_layout.addLayout(
            button_layout
        )

        control_layout.addWidget(
            self.brightness_label
        )

        control_layout.addWidget(
            self.brightness_slider
        )

        control_layout.addWidget(
            self.contrast_label
        )

        control_layout.addWidget(
            self.contrast_slider
        )

        control_layout.addWidget(
            self.pixel_info
        )

        self.control_panel.setLayout(
            control_layout
        )

        # =====================================
        # MAIN LAYOUT
        # =====================================

        main_layout = QVBoxLayout()

        main_layout.addWidget(
            self.title
        )

        main_layout.addWidget(
            self.subtitle
        )

        main_layout.addLayout(
            image_layout
        )

        main_layout.addWidget(
            self.control_panel
        )

        self.setLayout(
            main_layout
        )

        # =====================================
        # LOADING OVERLAY
        # =====================================

        self.loading_overlay = QFrame(
            self
        )

        self.loading_overlay.hide()

        self.loading_overlay.setStyleSheet("""
            background-color: rgba(0, 0, 0, 150);
            border: none;
        """)

        overlay_layout = QVBoxLayout()

        overlay_layout.setAlignment(
            Qt.AlignCenter
        )

        # =====================================
        # LOADING GIF
        # =====================================

        self.spinner = QLabel()

        self.spinner.setStyleSheet("""
            background-color: transparent;
            border: none;
        """)

        self.movie = QMovie(
            "assets/loading.gif"
        )

        self.movie.setScaledSize(
            QSize(100, 100)
        )

        self.spinner.setMovie(
            self.movie
        )

        self.spinner.setFixedSize(
            100,
            100
        )

        overlay_layout.addWidget(
            self.spinner,
            0,
            Qt.AlignCenter
        )

        self.loading_overlay.setLayout(
            overlay_layout
        )

        # =====================================
        # STYLE
        # =====================================

        self.setStyleSheet("""

            QWidget {
                background-color: #0f172a;
                color: white;
                font-family: Segoe UI;
                font-size: 14px;
            }

            QFrame#imageFrame {
                background-color: #1e293b;
                border-radius: 18px;
                padding: 15px;
            }

            QFrame#controlPanel {
                background-color: #1e293b;
                border-radius: 18px;
                padding: 20px;
            }

            QPushButton {
                background-color: #2563eb;
                border: none;
                border-radius: 12px;
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
            }

            QPushButton:hover {
                background-color: #3b82f6;
            }

            QPushButton:pressed {
                background-color: #1d4ed8;
            }

        """)

    # =====================================
    # RESIZE OVERLAY
    # =====================================

    def resizeEvent(self, event):

        self.loading_overlay.setGeometry(
            0,
            0,
            self.width(),
            self.height()
        )

        super().resizeEvent(event)

    # =====================================
    # TIMER UPDATE
    # =====================================

    def start_update_timer(self):

        self.update_timer.start(250)

    # =====================================
    # OPEN IMAGE
    # =====================================

    def open_image(self):

        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open Image",
            "",
            "Images (*.png *.jpg *.jpeg)"
        )

        if file_name:

            self.image_path = file_name

            self.show_image(
                file_name,
                self.original_label
            )

            self.update_image()

    # =====================================
    # SHOW IMAGE
    # =====================================

    def show_image(self, image_path, label):

        pixmap = QPixmap(
            image_path
        )

        pixmap = pixmap.scaled(
            label.width(),
            label.height(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        label.setPixmap(
            pixmap
        )

    # =====================================
    # ADD WATERMARK TO IMAGE
    # =====================================

    def add_watermark(self, image):
        """Tambahkan watermark ke gambar PIL dengan konfigurasi dari WM_CONFIG"""
        try:
            # Buka gambar watermark
            watermark = Image.open("assets/wm.png")
            
            # Konversi watermark ke mode RGBA jika belum
            if watermark.mode != 'RGBA':
                watermark = watermark.convert('RGBA')
            
            # Atur opasitas watermark
            if WM_CONFIG['opacity'] < 255:
                # Buat alpha channel baru dengan opasitas yang diinginkan
                alpha = watermark.split()[3]
                alpha = alpha.point(lambda p: p * WM_CONFIG['opacity'] // 255)
                watermark.putalpha(alpha)
            
            # Hitung ukuran watermark dari konfigurasi
            wm_width = int(image.width * WM_CONFIG['size_percent'])
            wm_height = int(image.height * WM_CONFIG['size_percent'])
            watermark = watermark.resize((wm_width, wm_height), Image.Resampling.LANCZOS)
            
            # Konversi image ke RGBA jika perlu
            if image.mode != 'RGBA':
                image = image.convert('RGBA')
            
            # Buat layer transparan
            watermark_layer = Image.new('RGBA', image.size, (0, 0, 0, 0))
            
            # Posisi watermark berdasarkan konfigurasi
            offset = WM_CONFIG['position_offset']
            
            for position in WM_CONFIG['positions']:
                if position == 'top_left':
                    pos_x = offset
                    pos_y = offset
                elif position == 'top_right':
                    pos_x = image.width - wm_width - offset
                    pos_y = offset
                elif position == 'bottom_left':
                    pos_x = offset
                    pos_y = image.height - wm_height - offset
                elif position == 'bottom_right':
                    pos_x = image.width - wm_width - offset
                    pos_y = image.height - wm_height - offset
                else:
                    continue
                
                watermark_layer.paste(watermark, (pos_x, pos_y), watermark)
            
            # Composite gambar dengan watermark
            result = Image.alpha_composite(image, watermark_layer)
            
            return result
            
        except FileNotFoundError:
            print("Watermark file not found")
            return image
        except Exception as e:
            print(f"Error adding watermark: {e}")
            return image

    # =====================================
    # UPDATE IMAGE
    # =====================================

    def update_image(self):

        if not self.image_path:
            return

        # Stop thread lama kalau masih jalan
        if self.process_thread and self.process_thread.isRunning():

            self.process_thread.quit()
            self.process_thread.wait()

        self.loading_overlay.show()

        self.movie.start()

        QApplication.processEvents()

        beta = self.brightness_slider.value()

        alpha = (
            self.contrast_slider.value() / 10
        )

        self.brightness_label.setText(
            f"Brightness : {beta}"
        )

        self.contrast_label.setText(
            f"Contrast : {alpha:.2f}"
        )

        self.process_thread = ProcessThread(
            self.image_path,
            alpha,
            beta
        )

        self.process_thread.finished.connect(
            self.on_process_finished
        )

        self.process_thread.start()

    # =====================================
    # PROCESS FINISHED
    # =====================================

    def on_process_finished(self, result):

        # Tambahkan watermark ke hasil
        self.current_result = self.add_watermark(result)

        # =====================================
        # PIL IMAGE -> NUMPY
        # =====================================

        result_array = np.array(
            self.current_result,
            dtype=np.uint8
        )

        # =====================================
        # RGB CONTIGUOUS MEMORY
        # =====================================

        result_array = np.ascontiguousarray(
            result_array
        )

        height, width, channel = (
            result_array.shape
        )

        bytes_per_line = (
            channel * width
        )

        q_image = QImage(
            result_array.data,
            width,
            height,
            bytes_per_line,
            QImage.Format_RGBA8888
        )
        
        # =====================================
        # COPY AGAR MEMORY AMAN
        # =====================================

        q_image = q_image.copy()

        # =====================================
        # QIMAGE -> PIXMAP
        # =====================================

        pixmap = QPixmap.fromImage(
            q_image
        )

        pixmap = pixmap.scaled(
            self.result_label.width(),
            self.result_label.height(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        self.result_label.setPixmap(
            pixmap
        )

        # =====================================
        # PIXEL INFO
        # =====================================

        pixel = self.current_result.getpixel((0, 0))

        self.pixel_info.setText(
            f"Pixel [1,1] RGB : {pixel[:3]}"
        )

        # =====================================
        # STOP LOADING
        # =====================================

        self.movie.stop()

        self.loading_overlay.hide()

        self.process_thread = None

    # =====================================
    # SAVE IMAGE
    # =====================================

    def save_image(self):

        if self.current_result is None:
            return

        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save Image",
            "hasil.png",
            "PNG Files (*.png);;JPG Files (*.jpg)"
        )

        if file_name:
            # Simpan gambar yang sudah ada watermark-nya
            if file_name.lower().endswith(('.jpg', '.jpeg')):
                # Untuk JPG, konversi ke RGB
                rgb_image = self.current_result.convert('RGB')
                rgb_image.save(file_name)
            else:
                # Untuk PNG, simpan dengan transparansi
                self.current_result.save(file_name)

    # =====================================
    # RESET SLIDER
    # =====================================

    def reset_slider(self):

        self.brightness_slider.setValue(0)

        self.contrast_slider.setValue(10)

        if self.image_path:

            self.show_image(
                self.image_path,
                self.result_label
            )
            
            # Reset result
            self.current_result = None
            
            # Update dengan watermark
            self.update_image()

    # =====================================
    # SHOW GRAPH - DENGAN QTimer
    # =====================================

    def show_compare_plot(self):

        if (
            self.image_path
            and self.current_result is not None
        ):

            alpha = (
                self.contrast_slider.value() / 10
            )

            beta = (
                self.brightness_slider.value()
            )

            # Tampilkan loading
            self.loading_overlay.show()
            self.movie.start()
            QApplication.processEvents()

            # Gunakan QTimer untuk memanggil plot di main thread setelah delay kecil
            QTimer.singleShot(100, lambda: self.show_plot(alpha, beta))

    def show_plot(self, alpha, beta):
        compare_plot(
            self.image_path,
            self.current_result,
            alpha,
            beta
        )
        
        self.movie.stop()
        self.loading_overlay.hide()

    # =====================================
    # GRAPH FINISHED
    # =====================================

    def on_graph_finished(self):

        # Hentikan loading
        self.movie.stop()
        self.loading_overlay.hide()
        self.graph_thread = None


# =====================================
# MAIN
# =====================================

if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = ImageEditor()
    window.show()

    sys.exit(app.exec_())