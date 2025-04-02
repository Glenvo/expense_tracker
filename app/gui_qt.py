import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout,
    QComboBox, QPushButton, QMessageBox, QStackedLayout, QInputDialog
)
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from .models import add_expense
from .logic import get_monthly_summary


class ClickableLabel(QLabel):
    clicked = pyqtSignal()
    def mousePressEvent(self, event):
        self.clicked.emit()


class ExpenseApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Budget Tracker (PyQt6)")
        self.setStyleSheet("""
            QPushButton {
                background-color: #0078D7;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005bb5;
            }
            QLabel {
                font-size: 13px;
            }
            QLineEdit, QComboBox {
                padding: 6px;
                font-size: 13px;
            }
        """)

        main_layout = QVBoxLayout()
        self.stack = QStackedLayout()
        main_layout.addLayout(self.stack)
        self.setLayout(main_layout)

        self.page_add = QWidget()
        self.page_summary = QWidget()
        self.stack.addWidget(self.page_add)
        self.stack.addWidget(self.page_summary)

        self.setup_add_page()
        self.setup_summary_page()

        self.stack.setCurrentIndex(0)
        self.setMinimumSize(600, 600)
        self.adjustSize()
        frame = self.frameGeometry()
        center_point = QApplication.primaryScreen().availableGeometry().center()
        frame.moveCenter(center_point)
        self.move(frame.topLeft())

    def setup_add_page(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        self.summary_top_label = ClickableLabel("📊 View current month summary")
        self.summary_top_label.setStyleSheet("""
            color: #0078D7;
            text-decoration: underline;
            font-weight: bold;
            font-size: 14px;
            margin-bottom: 15px;
        """)
        self.summary_top_label.clicked.connect(self.goto_summary_page)
        layout.addWidget(self.summary_top_label)

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

        self.page_add.setLayout(layout)

    def setup_summary_page(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = QLabel("📊 Monthly Summary")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)

        self.summary_label = QLabel("📅 Loading summary...")
        self.summary_label.setStyleSheet("""
            font-size: 14px;
            background-color: #f0f5ff;
            border: 1px solid #cce0ff;
            border-radius: 12px;
            padding: 20px;
            margin-top: 10px;
            margin-bottom: 20px;
        """)
        self.summary_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        month_picker_layout = QHBoxLayout()

        self.year1_combo = QComboBox()
        self.month1_combo = QComboBox()
        self.year2_combo = QComboBox()
        self.month2_combo = QComboBox()

        years = [str(y) for y in range(2022, datetime.now().year + 1)]
        months = [f"{m:02d}" for m in range(1, 13)]

        self.year1_combo.addItems(years)
        self.month1_combo.addItems(months)
        self.year2_combo.addItems(years)
        self.month2_combo.addItems(months)

        month_picker_layout.addWidget(QLabel("Compare:"))
        month_picker_layout.addWidget(self.year1_combo)
        month_picker_layout.addWidget(self.month1_combo)
        month_picker_layout.addWidget(QLabel("vs"))
        month_picker_layout.addWidget(self.year2_combo)
        month_picker_layout.addWidget(self.month2_combo)

        layout.addLayout(month_picker_layout)
        layout.addWidget(self.summary_label)

        compare_categories_btn = QPushButton("Compare Categories")
        compare_categories_btn.clicked.connect(self.compare_categories)
        layout.addWidget(compare_categories_btn)


        # === Chart Canvas ===
        self.chart_canvas = FigureCanvas(Figure(figsize=(6, 3)))  
        layout.addWidget(self.chart_canvas, stretch=1)

        # === Buttons ===
        
        back_button = QPushButton("← Back to Add Expense")
        back_button.clicked.connect(self.goto_add_page)
        layout.addWidget(back_button)

        self.page_summary.setLayout(layout)

    
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

    def goto_summary_page(self):
        now = datetime.now()
        year, month = now.year, now.month
        total, df = get_monthly_summary(year, month)

        if df.empty:
            msg = f"📅 {year}-{month:02d} — No expenses found."
        else:
            msg = f"<b>📅 {year}-{month:02d}</b><br><b>Total:</b> ₪{total:.2f}<br><ul>"
            breakdown = df.groupby("category")["amount"].sum()
            for cat, amt in breakdown.items():
                msg += f"<li><b>{cat}:</b> ₪{amt:.2f}</li>"
            msg += "</ul>"

        self.summary_label.setText(msg)
        self.stack.setCurrentIndex(1)

    def goto_add_page(self):
        self.stack.setCurrentIndex(0)

    def compare_categories(self):
        try:
            y1 = int(self.year1_combo.currentText())
            m1 = int(self.month1_combo.currentText())
            y2 = int(self.year2_combo.currentText())
            m2 = int(self.month2_combo.currentText())

            _, df1 = get_monthly_summary(y1, m1)
            _, df2 = get_monthly_summary(y2, m2)

            cat1 = df1.groupby("category")["amount"].sum()
            cat2 = df2.groupby("category")["amount"].sum()

            all_cats = sorted(set(cat1.index).union(set(cat2.index)))
            all_cats.append("Total")  

            vals1 = [cat1.get(cat, 0) for cat in all_cats[:-1]]
            vals2 = [cat2.get(cat, 0) for cat in all_cats[:-1]]
            vals1.append(sum(vals1))  
            vals2.append(sum(vals2))

            # Draw chart
            self.chart_canvas.figure.clear()
            ax = self.chart_canvas.figure.add_subplot(111)

            x = range(len(all_cats))
            ax.bar([i - 0.2 for i in x], vals1, width=0.4, label=f"{y1}-{m1:02d}", color="#0078D7")
            ax.bar([i + 0.2 for i in x], vals2, width=0.4, label=f"{y2}-{m2:02d}", color="#00B050")

            ax.set_xticks(x)
            ax.set_xticklabels(all_cats, rotation=30, ha="right")
            ax.set_title("Category Spending Comparison (₪)")
            ax.set_ylabel("₪")
            ax.legend()
            self.chart_canvas.figure.tight_layout()
            self.chart_canvas.draw()
            

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not generate comparison.\n\n{e}")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ExpenseApp()
    window.show()
    sys.exit(app.exec())
