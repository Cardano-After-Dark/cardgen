import sys
import os
import requests
import json
from datetime import datetime
import random
import string
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QTextEdit, QFileDialog, QProgressBar
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QThread, pyqtSignal

class ImageGenerationThread(QThread):
    finished = pyqtSignal(dict)
    progress = pyqtSignal(int)

    def __init__(self, api_key, params):
        super().__init__()
        self.api_key = api_key
        self.params = params

    def run(self):
        host = "https://api.stability.ai/v2beta/stable-image/generate/core"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        self.progress.emit(10)
        response = requests.post(host, headers=headers, json=self.params)
        self.progress.emit(50)

        if response.status_code != 200:
            self.finished.emit({"error": f"Error: {response.status_code} - {response.text}"})
            return

        response_data = response.json()
        self.progress.emit(80)

        if "image" in response_data:
            image_data = response_data["image"]
            self.finished.emit({"success": image_data})
        else:
            self.finished.emit({"error": "No image data in response"})

class StabilityAIImageGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.api_key = ""
        self.initUI()

    def initUI(self):
        # ... (previous UI setup code remains the same)

        # Add progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # Add save directory selection
        save_dir_layout = QHBoxLayout()
        self.save_dir_input = QLineEdit()
        self.save_dir_input.setText(os.path.join(os.path.dirname(__file__), 'out'))
        save_dir_button = QPushButton('Select Save Directory')
        save_dir_button.clicked.connect(self.select_save_directory)
        save_dir_layout.addWidget(QLabel('Save Directory:'))
        save_dir_layout.addWidget(self.save_dir_input)
        save_dir_layout.addWidget(save_dir_button)
        layout.addLayout(save_dir_layout)

        self.setLayout(layout)

    def select_save_directory(self):
        dir_name = QFileDialog.getExistingDirectory(self, "Select Save Directory")
        if dir_name:
            self.save_dir_input.setText(dir_name)

    def generate_image(self):
        if not self.api_key:
            print("Please set your API key first")
            return

        params = {
            "text_prompts": [{"text": self.prompt_input.toPlainText()}],
            "height": 512,
            "width": 512,
            "samples": 1,
            "steps": 50,
            "seed": int(self.seed_input.text()),
            "cfg_scale": 7,
        }

        if self.neg_prompt_input.toPlainText():
            params["text_prompts"].append({"text": self.neg_prompt_input.toPlainText(), "weight": -1})

        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)

        self.thread = ImageGenerationThread(self.api_key, params)
        self.thread.finished.connect(self.handle_generation_result)
        self.thread.progress.connect(self.update_progress)
        self.thread.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def handle_generation_result(self, result):
        self.progress_bar.setVisible(False)
        if "error" in result:
            print(result["error"])
            return

        image_data = result["success"]
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
        random_string = ''.join(random.choices(string.ascii_letters, k=12))
        filename = f"{timestamp}_{random_string}.png"
        save_path = os.path.join(self.save_dir_input.text(), filename)

        # Save image
        with open(save_path, "wb") as f:
            f.write(image_data)

        # Save parameters
        params_filename = os.path.splitext(save_path)[0] + ".txt"
        with open(params_filename, "w") as f:
            json.dump({
                "prompt": self.prompt_input.toPlainText(),
                "negative_prompt": self.neg_prompt_input.toPlainText(),
                "aspect_ratio": self.aspect_ratio_combo.currentText(),
                "seed": int(self.seed_input.text()),
                "output_format": self.output_format_combo.currentText()
            }, f, indent=2)

        pixmap = QPixmap()
        pixmap.loadFromData(image_data)
        self.image_label.setPixmap(pixmap.scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio))
        print(f"Image saved as {save_path}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = StabilityAIImageGenerator()
    ex.show()
    sys.exit(app.exec())