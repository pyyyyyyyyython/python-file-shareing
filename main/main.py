import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtCore import Qt
from PyQt5 import uic

import socket
import subprocess
import json

# UI 파일은 동일한 디렉터리에 위치
form_class = uic.loadUiType("E:/Dev/python/파이썬_영상다운로드도구/main/main.ui")[0]

# 화면 출력에 필요한 class
class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.is_server_running = False  # 서버 상태 추적 변수 추가
        self.setupUi(self)

        # 사용자 연결 화면 시그널 연결

        # 서버의 주소 입력 칸(path, QLineEdit)연결
        '''
        텍스트 입력이므로 연결하지 않음
        연결 시도 함수(server_connect)에서 다음 코드로 사용
        `self.path.text()`
        '''

        # 서버 연결 버튼(connect, QPushButton)연결
        self.connect.clicked.connect(lambda: (self.server_connect(), self.server_tree())) # 서버 연결 및 파일 트리 표시

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

        # 내 파일 공유 화면 시그널

        # 공유할 파일 위치 찾기
        # 공유할 파일 위치 지정 버튼(find_start, QPushButton)
        self.find_start.clicked.connect(self.find_path)

        # 공유할 파일 위치 적기(folder_path, QLineEdit)
        '''
        파일 위치 선택 관련 처리하는 find_path() 함수에서 진행
        '''

        # 서버를 시작하는 버튼(server_start, QPushButton)
        self.server_start.clicked.connect(self.start_server)

        # 서버를 중지하는 버튼(server_stop, QPushButton)
        self.server_stop.clicked.connect(self.stop_server)

        # 서버가 시작되어 서버의 주소를 출력하는 부분(server_juso, QTextEdit)
        '''
        서버 시작 함수(start_server)에서 관리
        '''

        # 서버의 로그를 출력하는 부분(log, QPlainTextEdit)
        '''
        서버 시작 함수(start_server)에서 관리
        '''

    # 서버 연결 관련 함수
    def server_connect(self):
        # TODO: 서버 연결 로직을 구현할 함수
        pass

    def server_tree(self):
        """서버의 파일 구조를 트리 형태로 표시하는 함수"""
        try:
            # 서버 주소 가져오기
            server_url = self.path.text().strip()
            
            if not server_url:
                QMessageBox.warning(self, '경고', '서버 주소를 입력해주세요.')
                return
                
            # QStandardItemModel 생성
            model = QStandardItemModel()
            model.setHorizontalHeaderLabels(['파일/폴더'])
            
            import urllib.request
            
            try:
                # 서버에서 디렉토리 정보 가져오기
                with urllib.request.urlopen(f"{server_url}?format=json") as response:
                    data = json.loads(response.read().decode())
                    
                    # 루트 아이템 생성
                    root = QStandardItem("/")
                    model.appendRow(root)
                    
                    # 파일과 폴더 정렬
                    folders = []
                    files = []
                    
                    for item in data:
                        if item.get('type') == 'directory':
                            folders.append(item)
                        else:
                            files.append(item)
                            
                    # 폴더 먼저 추가
                    for folder in sorted(folders, key=lambda x: x['name']):
                        folder_item = QStandardItem("📁 " + folder['name'])
                        folder_item.setData(folder['name'], Qt.UserRole)
                        root.appendRow(folder_item)
                        
                    # 그 다음 파일 추가
                    for file in sorted(files, key=lambda x: x['name']):
                        file_item = QStandardItem("📄 " + file['name'])
                        file_item.setData(file['name'], Qt.UserRole)
                        root.appendRow(file_item)
                        
                    # TreeView에 모델 설정
                    self.treeView.setModel(model)
                    self.treeView.expandAll()
                    
            except urllib.error.URLError as e:
                QMessageBox.critical(self, '오류', f'서버 연결 실패: {str(e)}')
            except json.JSONDecodeError:
                QMessageBox.critical(self, '오류', '서버 응답 형식이 잘못되었습니다.')
                
        except Exception as e:
            QMessageBox.critical(self, '오류', f'예기치 않은 오류 발생: {str(e)}')

    def server_download(self):
        # TODO: 선택된 파일을 다운로드할 함수
        pass

    def find_path(self):
        """파일 탐색기를 통해 서버 시작 경로를 선택하는 함수"""
        # QFileDialog를 사용하여 디렉토리 선택 대화상자 표시
        self.folder_path.setText(QFileDialog.getExistingDirectory(self, '파일 위치를 선택하세요'))
        # 선택된 경로를 folder_path QLineEdit에 표시
        self.folder_path.setText(self.path)

    def start_server(self):
        """HTTP 서버를 시작하는 함수"""
        try:
            # QLineEdit에서 서버 경로를 가져와서 공백 제거
            server_path = self.folder_path.text().strip()
            
            # 경로가 비어있는지 확인
            if not server_path:
                QMessageBox.warning(self, '경고', '서버 시작 경로를 선택해주세요.')
                return
                
            # 이미 실행 중인 서버가 있는지 확인
            if hasattr(self, 'server_process'):
                QMessageBox.warning(self, '경고', '서버가 이미 실행 중입니다.')
                return
                
            # subprocess.Popen을 사용하여 Python HTTP 서버 시작
            # 포트 8080으로 설정하고 지정된 경로에서 실행
            self.server_process = subprocess.Popen(
                ['python', '-m', 'http.server', '8080'], 
                cwd=server_path,
                text=True
            )
            
            # 현재 시스템의 IP 주소를 확인하고 서버 주소 표시
            ip_address = socket.gethostbyname(socket.gethostname())
            self.server_juso.setText(f'http://{ip_address}:8080')
            
        except Exception as e:
            # 오류 발생 시 에러 메시지 표시
            QMessageBox.critical(self, '오류', f'서버 시작 중 오류 발생: {str(e)}')
            self.server_juso.setText('서버 시작 실패')

    def stop_server(self):
        """실행 중인 HTTP 서버를 중지하는 함수"""
        try:
            # 서버 프로세스 종료
            self.server_process.kill()
            self.server_process.kill()
            # 프로세스가 완전히 종료될 때까지 최대 5초 대기
            self.server_process.wait(timeout=5)

            # 서버 프로세스 객체 제거
            if hasattr(self, 'server_process'):
                delattr(self, 'server_process')

            # 서버 중지 메시지를 빨간색으로 표시
            self.server_juso.setHtml('<span style="color:red;">서버가 중지되었습니다.</span>')
            if hasattr(self, 'server_process'):
                delattr(self, 'server_process')
        except Exception as e:
            # 서버 중지 실패 시 에러 메시지 표시
            QMessageBox.critical(self, '알림', '서버가 중지되지 않았습니다. \n서버가 시작되지 않았거나 이미 중지되었을 수 있습니다.')






if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)
    #WindowClass의 인스턴스 생성
    myWindow = WindowClass()
    #프로그램 화면을 보여주는 코드
    myWindow.show()
    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()