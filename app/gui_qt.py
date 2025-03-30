
import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout,
    QComboBox, QPushButton, QMessageBox
)
from datetime import datetime
from .models import add_expense

class ExpenseApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Budget Tracker (PyQt6)")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

     
        self.date_input = QLineEdit(datetime.now().strftime("%Y-%m-%d"))
        layout.addWidget(QLabel("Date (YYYY-MM-DD):"))
        layout.addWidget(self.date_input)

        self.category_input = QComboBox()
        self.category_input.addItems(["Food", "Transport", "Entertainment", "Bills", "Health", "Other"])
        layout.addWidget(QLabel("Category:"))
        layout.addWidget(self.category_input)

        self.amount_input = QLineEdit()
        layout.addWidget(QLabel("Amount:"))
        layout.addWidget(self.amount_input)

        self.description_input = QLineEdit()
        layout.addWidget(QLabel("Description:"))
        layout.addWidget(self.description_input)

        self.submit_button = QPushButton("Add Expense")
        self.submit_button.clicked.connect(self.add_expense)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def add_expense(self):
        try:
            date = self.date_input.text()
            category = self.category_input.currentText()
            amount = float(self.amount_input.text())
            description = self.description_input.text()

            add_expense(category, amount, description, date)
            QMessageBox.information(self, "Success", "Expense added!")

            self.category_input.setCurrentIndex(0)
            self.amount_input.clear()
            self.description_input.clear()
        except ValueError:
            QMessageBox.warning(self, "Error", "Amount must be a number.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExpenseApp()
    window.show()
    sys.exit(app.exec())
