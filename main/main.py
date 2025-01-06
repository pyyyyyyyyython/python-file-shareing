import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic


# UI 파일은 동일한 디렉터리에 위치
form_class = uic.loadUiType("main.ui")[0]

# 화면 출력에 필요한 class
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        # 사용자 연결 화면 시그널 연결
        # 서버의 주소 입력 칸(path, QLineEdit)연결
        '''
        텍스트 입력이므로 연결하지 않음
        연결 시도 QPushButton에서 다음 코드로 사용
        `self.path.text()`
        '''
        # 서버 연결 버튼(connect, QPushButton)연결
        self.connect.clicked.connect(self.server_connect) # server_connect 함수: 서버 연결을 요청
        # 서버 연결 로딩바(connect_progress, QProgressBar)연결
        '''
        상태 로딩이므로 연결하지 않음
        연결 요청 함수 server_connect() 에서 변경
        다음 코드 사용:
        read document
        '''
        # 연결된 서버의 파일을 모두 출력하는 tree view(treeView, QTreeView)연결
        '''
        관련 정보가 부족하여 이후 작성
        서버 파일 구조 함수 server_tree() 에서 사용
        '''
        # 선택된 파일 다운로드 버튼(select_download, QPushButton) 연결
        self.select_download.clicked.connect(self.server_download)
        # 파일 다운로드 상태 바(progressBar, QProgressBar) 연결
        '''
        상태 로딩이므로 연결하지 않음
        다운로드 함수 server_download() 에서 변경
        다음 코드 사용:
        read document
        '''




if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)
    #WindowClass의 인스턴스 생성
    myWindow = WindowClass()
    #프로그램 화면을 보여주는 코드
    myWindow.show()
    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()