from iterator import path_iterator
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QPixmap
import os


class MainWindow(QtWidgets.QMainWindow):
    '''Главное окно'''
    def __init__(self):
        super().__init__()
        self.iterator = None
        self.ui()
        self.next_button.setEnabled(False)
        self.folder_button.clicked.connect(self.select_folder)
        self.annotation_button.clicked.connect(self.select_annotation)
        self.next_button.clicked.connect(self.on_next)

    def ui(self) -> None:
        '''Интерфейс'''
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QVBoxLayout(central)
        layout.setContentsMargins(20,20,20,20)
        layout.setSpacing(15)

        source = QtWidgets.QHBoxLayout()
        source.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.folder_button = QtWidgets.QPushButton("Выбрать папку с датасетом")
        self.annotation_button = QtWidgets.QPushButton("Выбрать файл аннотации")

        for btn in (self.folder_button, self.annotation_button):
                btn.setFixedHeight(36)
                btn.setFont(QtGui.QFont("UI", 10))
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #4A6FA5;
                        color: white;
                        border: none;
                        border-radius: 6px;
                        padding: 6px 12px;
                    }
                    QPushButton:hover {
                        background-color: #3A5A80;
                    }
                """)
        source.addWidget(self.folder_button)
        source.addWidget(self.annotation_button)
        layout.addLayout(source)

        self.image_lable = QtWidgets.QLabel()
        self.image_lable.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.image_lable.setMinimumSize(400,300)
        self.image_lable.setStyleSheet("""
        QLabel {
            background-color: white;
            border: 1px dashed #ccc;
            border-radius: 8px;
        }
        """)     
        self.image_lable.setText("Выберите папку или .csv файл")
        self.image_lable.setFont(QtGui.QFont("Segoe UI", 11))  
        layout.addWidget(self.image_lable)

        self.next_button = QtWidgets.QPushButton("Следующее изображение")
        self.next_button.setFixedHeight(40)
        self.next_button.setFont(QtGui.QFont("Segoe UI", 11))
        self.next_button.setStyleSheet(""" QPushButton {
            background-color: #6c757d;
            color: white;
            border: none;
            border-radius: 6px;
        }
        QPushButton:disabled {
            background-color: #adb5bd;
        }
        QPushButton:hover:!disabled {
            background-color: #5a6268;
        }""")
        layout.addWidget(self.next_button)

    def init_iterator(self, source:str) -> None:
        '''Создаёт итератор'''
        try:
            self.iterator = path_iterator(source)
            self.next_button.setEnabled(True)
            self.image_lable.setText("Нажмите \"Следующее изображение\"")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить источник:\n{e}")
            self.iterator = None
            self.next_button.setEnabled(False) 

    def select_folder(self) -> None:
         folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку")
         if folder:
              self.init_iterator(folder)
    
    def select_annotation(self) -> None:
         file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите файл аннотации", "", "CSV Files (*.csv)")
         if file_path:
              self.init_iterator(file_path)
    
    def on_next(self) ->None:
         '''Навигация'''
         if not self.iterator:
              return
         try:
              next_path = next(self.iterator)
         except StopIteration:
                QtWidgets.QMessageBox.information(self, "Конец", "Все изображения посмотрены")
                self.next_button.setEnabled(False)
                return
         except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка итератора", f"Не удалось получить путь:\n{e}")
            return
         if not os.path.isfile(next_path):
              QtWidgets.QMessageBox.warning(self, "Файл не найден", f"Файл не существует:\n{next_path}")
              return
         pixmap = QPixmap(next_path)
         if pixmap.isNull():
              QtWidgets.QMessageBox.warning(self, "Ошибка формата", f"Файл не изображение:\n{next_path}")
              return
         self.image_lable.setPixmap(pixmap.scaled(self.image_lable.size(), 
                                                  QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                                                  QtCore.Qt.TransformationMode.SmoothTransformation))
         
    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
         '''Изменение изображения при изменении размера'''
         super().resizeEvent(event)
         if self.iterator is not None:
              pixmap = self.image_lable.pixmap()
              if pixmap and not pixmap.isNull():
                self.image_lable.setPixmap(
                    pixmap.scaled(self.image_lable.size(),
                        QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                        QtCore.Qt.TransformationMode.SmoothTransformation
                    )
                )

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())