'''
OpenAI - GPT - 4omini로 작성한 코드임.
ui 파일을 연결하지 않고 코드 작성
'''


import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget


class DirectoryTreeView(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("디렉터리 트리 뷰")
        self.setGeometry(100, 100, 600, 400)

        # 중앙 위젯 설정
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # 레이아웃 설정
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # QTreeWidget 생성
        self.tree_widget = QTreeWidget(self)
        self.tree_widget.setHeaderLabels(["파일/폴더 이름"])
        layout.addWidget(self.tree_widget)

        # 현재 디렉터리에서 트리 구조 생성
        self.create_directory_tree(os.getcwd())

    def create_directory_tree(self, parent_dir):
        # parent_dir의 모든 파일과 폴더를 탐색하여 트리 뷰에 추가
        root_item = QTreeWidgetItem(self.tree_widget, [parent_dir])
        self.add_items_recursively(parent_dir, root_item)

    def add_items_recursively(self, parent_dir, parent_item):
        # 디렉터리 내의 모든 파일과 폴더를 추가
        try:
            for item in os.listdir(parent_dir):
                item_path = os.path.join(parent_dir, item)
                tree_item = QTreeWidgetItem(parent_item, [item])

                if os.path.isdir(item_path):
                    # 디렉터리인 경우, 하위 디렉터리를 재귀적으로 추가
                    self.add_items_recursively(item_path, tree_item)
                else:
                    # 파일인 경우, 파일로 추가
                    continue
        except PermissionError:
            # 권한 문제가 발생할 수 있으므로 예외 처리
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DirectoryTreeView()
    window.show()
    sys.exit(app.exec_())
