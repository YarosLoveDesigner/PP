from fpdf import FPDF


# В вашем методе __init__ добавьте кнопку для экспорта в PDF
class MasterApp(QWidget):
    def __init__(self):
        super().__init__()


        # Ваш основной код...


        # Добавляем кнопку для экспорта данных в PDF
        export_button = QPushButton("Экспорт в PDF")
        export_button.setFixedWidth(150)
        export_button.clicked.connect(self.export_to_pdf)


        # Добавляем кнопку на панель
        top_layout.addWidget(export_button)


   