import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QMessageBox, QVBoxLayout, QWidget, QHBoxLayout
from datetime import datetime

class WorkTracker(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Work Tracker")
        self.setGeometry(200, 200, 400, 200)

        self.operator_label = QLabel("Operator ID:")
        self.operator_input = QLineEdit()

        self.workorder_label = QLabel("WorkOrder ID:")
        self.workorder_input = QLineEdit()

        self.pt_label = QLabel("PT:")
        self.pt_input = QLineEdit()

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_work)

        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.pause_work)
        self.pause_button.setDisabled(True)

        layout = QVBoxLayout()
        layout.addWidget(self.operator_label)
        layout.addWidget(self.operator_input)
        layout.addWidget(self.workorder_label)
        layout.addWidget(self.workorder_input)
        layout.addWidget(self.pt_label)
        layout.addWidget(self.pt_input)
        layout.addWidget(self.start_button)
        layout.addWidget(self.pause_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Data logging
        self.log_file = "work_log.xlsx"

    def start_work(self):
        operator_id = self.operator_input.text()
        workorder_id = self.workorder_input.text()
        pt = self.pt_input.text()
        if operator_id and workorder_id and pt:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data = {'Operator ID': operator_id, 'WorkOrder ID': workorder_id, 'PT': pt, 'Start Time': timestamp}
            self.log_data(data)
            self.clear_inputs()
            self.start_button.setDisabled(True)
            self.pause_button.setEnabled(True)
        else:
            QMessageBox.warning(self, "Warning", "Please fill in all fields")

    def pause_work(self):
        operator_id = self.operator_input.text()
        workorder_id = self.workorder_input.text()
        pt = self.pt_input.text()
        if operator_id:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data = {'Operator ID': operator_id, 'WorkOrder ID': workorder_id, 'PT': pt, 'Pause Time': timestamp}
            self.log_data(data)
            self.operator_input.clear()
            self.workorder_input.clear()
            self.pt_input.clear()
            self.start_button.setEnabled(True)
            self.pause_button.setDisabled(True)
        else:
            QMessageBox.warning(self, "Warning", "Please fill in Operator ID")

    def log_data(self, data):
        try:
            df = pd.read_excel(self.log_file)
        except FileNotFoundError:
            df = pd.DataFrame(columns=['Operator ID', 'WorkOrder ID', 'PT', 'Start Time', 'Pause Time'])
        df = df.append(data, ignore_index=True)
        df.to_excel(self.log_file, index=False)

    def clear_inputs(self):
        self.operator_input.clear()
        self.workorder_input.clear()
        self.pt_input.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WorkTracker()
    window.show()
    sys.exit(app.exec_())
