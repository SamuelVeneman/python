import sys
import asyncio
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QMainWindow
from PyQt5.QtCore import QDateTime, Qt
#from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QFont

from pyppeteer import launch
import winsound

URL = "https://newautopart.net/includes/pullandsave/spokane/yard_locationslist.php?cmd=search&t=yard_locations&psearch=cherokee&psearchtype="

async def get_search_results():
    browser = await launch(headless=True)
    page = await browser.newPage()
    
    search_url = "https://newautopart.net/includes/pullandsave/spokane/yard_locationslist.php?cmd=search&t=yard_locations&psearch=cherokee&psearchtype="
    await page.goto(search_url, timeout=60000)  # Visit the search URL directly
    await asyncio.sleep(5)  # Wait for JavaScript to load search results

    # Extract the search results
    rows = await page.querySelectorAll('table > tbody > tr')
    extracted_results = []
    for row in rows:
        row_data = []
        for i in range(1, 8):  # Extract data from all 7 columns
            cell = await row.querySelector(f'td:nth-child({i})')
            cell_text = await page.evaluate('(element) => element.textContent', cell)
            row_data.append(cell_text.strip() if cell_text else "")
        extracted_results.append(row_data)

    print("Extracted results:", extracted_results)  # Print extracted results to the terminal
    await browser.close()
    return extracted_results

from PyQt5.QtCore import QDateTime

from PyQt5.QtCore import QDateTime

class ResultWindow(QMainWindow):
    def __init__(self, results):
        super().__init__()
        self.setWindowTitle("PullNSave Search Results")

        # Set dark mode stylesheet
        self.setStyleSheet("QMainWindow {background-color: #333333; color: #ffffff;} "
                           "QTableWidget {background-color: #444444; color: #ffffff; "
                           "border: none; gridline-color: #ffffff;}"
                           "QHeaderView::section {background-color: #555555; color: #ffffff; "
                           "padding: 5px;}"
                           "QHeaderView {background-color: #555555; color: #ffffff; "
                           "border: none;}"
                           "QLabel {color: #ffffff;}")

  # Create table
        table = QTableWidget(self)
        table.setColumnCount(7)
        table.setRowCount(len(results))
        table.setHorizontalHeaderLabels(["Stock Ticket", "Row", "Vin", "Year", "Make", "Model", "New"])

        # Add results to the table
        for i, result in enumerate(results):
            for j, cell_value in enumerate(result):
                table.setItem(i, j, QTableWidgetItem(str(cell_value)))

        # Add title to the layout
        title = QLabel("Cherokee Search Results")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 24, QFont.Bold))
        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(table)
        
        # Create central widget and set layout
        central_widget = QWidget()
        central_widget.setLayout(layout)

        # Set central widget and size
        self.setCentralWidget(central_widget)
        self.resize(800, 600)



def show_results():
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(get_search_results())
    window = ResultWindow(results)
    window.show()

    # Play notification sound
    duration = 1000  # milliseconds
    frequency = 440  # Hz
    winsound.PlaySound("*", winsound.SND_ALIAS)

    sys.exit(app.exec_())

if __name__ == "__main__":
    show_results()
