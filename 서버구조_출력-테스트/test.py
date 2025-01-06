'''
OpenAI - GPT - 4omini로 작성한 코드임.
ui 파일을 연결하지 않고 코드 작성
'''

import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QLineEdit, QPushButton, QWidget, QMessageBox


class FileExplorerClient(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("파일 공유 클라이언트")
        self.setGeometry(100, 100, 600, 400)

        # 중앙 위젯 설정
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # 레이아웃
        self.layout = QVBoxLayout(self.central_widget)

        # 서버 주소 입력 필드와 버튼
        self.server_input = QLineEdit(self)
        self.server_input.setPlaceholderText("서버 주소를 입력하세요 (예: http://127.0.0.1:8000)")
        self.layout.addWidget(self.server_input)

        self.connect_button = QPushButton("연결", self)
        self.connect_button.clicked.connect(self.connect_to_server)
        self.layout.addWidget(self.connect_button)

        # 디렉터리 구조를 표시할 트리 위젯
        self.tree_widget = QTreeWidget(self)
        self.tree_widget.setHeaderLabels(["파일/폴더 이름"])
        self.layout.addWidget(self.tree_widget)

    def connect_to_server(self):
        server_url = self.server_input.text().strip()

        if not server_url:
            QMessageBox.warning(self, "경고", "서버 주소를 입력하세요!")
            return

        try:
            # 서버에서 디렉터리 구조 가져오기
            response = requests.get(server_url)
            if response.status_code != 200:
                QMessageBox.critical(self, "오류", f"서버 응답 실패 (코드: {response.status_code})")
                return

            # HTML을 파싱하여 디렉터리 구조를 표시
            self.parse_directory_structure(server_url, response.text)

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "오류", f"서버에 연결할 수 없습니다: {e}")

    def parse_directory_structure(self, base_url, html_content):
        from bs4 import BeautifulSoup

        # 기존 트리 초기화
        self.tree_widget.clear()

        # HTML 파싱
        soup = BeautifulSoup(html_content, "html.parser")
        links = soup.find_all("a")

        for link in links:
            href = link.get("href")
            if href not in ("../", "/"):
                item = QTreeWidgetItem([href])
                self.tree_widget.addTopLevelItem(item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileExplorerClient()
    window.show()
    sys.exit(app.exec_())
