import sys
from fpdf import FPDF
import logging
logging.basicConfig(level=logging.DEBUG)

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem, QLineEdit, QTableWidget, QTableWidgetItem,
    QDialog, QFormLayout, QMessageBox, QSpinBox, QComboBox
)
from PySide6.QtCore import Qt, QSize
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker


# Подключение к базе данных
DATABASE_URI = 'postgresql://postgres:root@localhost:5432/asd'
engine = create_engine(DATABASE_URI)
Base = declarative_base()

# Модели для базы данных
class TypeCompany(Base):
    __tablename__ = 'type_company'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)


class Partners(Base):
    __tablename__ = 'partners'
    id = Column(Integer, primary_key=True)
    type_partner = Column(Integer, ForeignKey('type_company.id'))
    company_name = Column(String(255), nullable=False)
    ur_adress = Column(String(255), nullable=False)
    inn = Column(String(50), nullable=False)
    director_name = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False)
    rating = Column(Integer, nullable=True)
    type_company = relationship("TypeCompany")

class ProductType(Base):
    __tablename__ = 'product_type'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    coefficient = Column(Float, nullable=False)


class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    type = Column(Integer, ForeignKey('product_type.id'))
    description = Column(String(255))
    article = Column(Integer)
    price = Column(Float)
    size = Column(Float)
    class_id = Column(Integer)

    product_type = relationship("ProductType")

class Material(Base):
    __tablename__ = 'material'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    defect = Column(Float)

class MaterialProduct(Base):
    __tablename__ = 'material_product'
    id = Column(Integer, primary_key=True)
    id_product = Column(Integer, ForeignKey('product.id'))
    id_material = Column(Integer, ForeignKey('material.id'))

class PartnerProduct(Base):
    __tablename__ = 'partner_product'
    id = Column(Integer, primary_key=True)
    id_product = Column(Integer, ForeignKey('product.id'))
    id_partner = Column(Integer, ForeignKey('partners.id'))
    quantity = Column(Integer)
    date_of_sale = Column(String(50))  # Use a string for simplicity here


    product = relationship("Product")
    partner = relationship("Partners")


# Создание таблиц в базе данных
Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()


# Функция для расчета скидки
def calculate_discount(sales_volume):
    if sales_volume <= 10000:
        return 0
    elif 10000 < sales_volume <= 50000:
        return 5
    elif 50000 < sales_volume <= 300000:
        return 10
    else:
        return 15




# Функция для расчета необходимого материала
def calculate_material_needed(product_id, quantity):
    product = session.query(Product).filter_by(id=product_id).first()
    if not product:
        raise ValueError("Продукт не найден.")


    materials = session.query(MaterialProduct).filter_by(id_product=product_id).all()
    total_material_needed = 0


    for material_product in materials:
        material = session.query(Material).filter_by(id=material_product.id_material).first()
        if not material:
            continue
        # Расчет материала с учетом брака
        material_needed = product.size * quantity * material.defect
        total_material_needed += material_needed


    return total_material_needed


# Главный класс приложения
class MasterApp(QWidget):
    def __init__(self):
        super().__init__()


        # Установка иконки приложения
        self.setWindowTitle("Мастер пол")
        self.setWindowIcon(QIcon("/logo.png"))  # Замените на путь к вашему логотипу
        self.setFixedSize(1440, 1024)


        # Главный макет
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)


        # Верхняя панель
        top_panel = QWidget()
        top_panel.setStyleSheet("background-color: #F4E8D3; padding: 5px;")
        top_layout = QHBoxLayout(top_panel)


        # Иконка и текст для верхней панели
        top_icon_label = QLabel()
        top_icon_label.setPixmap(QIcon("logo.png").pixmap(50, 50))  # Замените на путь к вашему логотипу
        top_label = QLabel("Мастер пол")
        top_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-left: 0px;")


        search_box = QLineEdit()
        search_box.setPlaceholderText("Поиск")
        search_box.setFixedWidth(200)
        search_box.setStyleSheet("padding: 5px; margin-left: 10px;")


        add_partner_button = QPushButton("Добавить партнёра")
        add_partner_button.setFixedWidth(150)
        add_partner_button.clicked.connect(self.show_add_partner_dialog)


        # Добавляем элементы в верхнюю панель
        top_layout.addWidget(top_icon_label)
        top_layout.addWidget(top_label)
        top_layout.addWidget(search_box)
        top_layout.addWidget(add_partner_button)
        top_layout.addStretch()
        main_layout.addWidget(top_panel)


        # Панель навигации
        navigation_panel = QWidget()
        navigation_panel.setFixedHeight(100)
        navigation_panel.setStyleSheet("background-color: #F4E8D3;")
        nav_layout = QHBoxLayout(navigation_panel)


        # Кнопки навигации с иконками
        self.partners_button = QPushButton("Партнёры")
        self.partners_button.setIcon(QIcon("partner.png"))  # Замените на путь к вашему логотипу
        self.partners_button.setCheckable(True)
        self.partners_button.setChecked(True)
        self.partners_button.clicked.connect(self.select_partners_tab)


        self.history_button = QPushButton("История")
        self.history_button.setIcon(QIcon("history.png"))  # Замените на путь к вашему логотипу
        self.history_button.setCheckable(True)
        self.history_button.clicked.connect(self.select_history_tab)
        export_button = QPushButton("Экспорт в PDF")
        export_button.setFixedWidth(150)
        export_button.clicked.connect(self.export_to_pdf)
        top_layout.addWidget(export_button)

        self.update_tab_styles()


        nav_layout.addStretch()
        nav_layout.addWidget(self.partners_button)
        nav_layout.addWidget(self.history_button)
        main_layout.addWidget(navigation_panel)

        # Панель с контентом
        content_layout = QHBoxLayout()
        right_panel = QWidget()
        self.right_layout = QVBoxLayout(right_panel)
        self.right_layout.setContentsMargins(10, 10, 10, 0)

        self.partners_list = QListWidget()
        self.partners_list.setStyleSheet("background-color: #FFFFFF; border: none;")
        self.partners_list.itemClicked.connect(self.highlight_selected_partner)
        self.partners_list.itemDoubleClicked.connect(self.edit_partner)

        self.load_partners_from_db()

        self.history_table = QTableWidget()
        self.history_table.setColumnCount(4)
        self.history_table.setHorizontalHeaderLabels(["Продукция", "Наименование партнёра", "Количество продукции", "Дата продажи"])

        self.right_layout.addWidget(self.partners_list)
        content_layout.addWidget(right_panel)
        main_layout.addLayout(content_layout)
    

    


        self.setLayout(main_layout)
    
    def search_partners(self):
        """
        Метод для динамического поиска партнеров по имени.
        Фильтрует список партнеров в зависимости от текста в поле поиска.
        """
        search_text = self.findChild(QLineEdit).text().lower()  # Получаем текст из поля поиска
        partners = session.query(Partners).filter(Partners.company_name.ilike(f"%{search_text}%")).all()


        self.partners_list.clear()  # Очищаем текущий список


        # Добавляем найденных партнеров в список
        for partner in partners:
            item = QListWidgetItem()
            item_widget = self.create_partner_item(partner)
            item.setSizeHint(QSize(item_widget.sizeHint().width(), item_widget.sizeHint().height() + 20))
            self.partners_list.addItem(item)
            self.partners_list.setItemWidget(item, item_widget)
            item.setData(Qt.UserRole, partner)  # Сохраняем объект партнёра в item


    def load_partners_from_db(self):
        self.partners_list.clear()
        partners = session.query(Partners).all()
        for partner in partners:
            item = QListWidgetItem()
            item_widget = self.create_partner_item(partner)
            item.setSizeHint(QSize(item_widget.sizeHint().width(), item_widget.sizeHint().height() + 20))
            self.partners_list.addItem(item)
            self.partners_list.setItemWidget(item, item_widget)
            item.setData(Qt.UserRole, partner)  # Сохраняем объект партнёра в item

    def load_history_from_db(self):
        # Очистить таблицу истории
        self.history_table.setRowCount(0)


        # Выполняем запрос к базе данных, объединяя таблицы PartnerProduct, Product и Partners
        partner_products = session.query(PartnerProduct, Product, Partners).join(
            Product, Product.id == PartnerProduct.id_product).join(
            Partners, Partners.id == PartnerProduct.id_partner).all()


        print(f"Найдено записей: {len(partner_products)}")  # Отладочная информация


        # Заполняем таблицу данными
        for row_num, (partner_product, product, partner) in enumerate(partner_products):
            print(f"Добавление строки: {row_num}")  # Отладочная информация


            # Добавляем строку в таблицу
            self.history_table.insertRow(row_num)


            # Вставляем данные в ячейки таблицы
            self.history_table.setItem(row_num, 0, QTableWidgetItem(product.description))  # Продукция (description из Product)
            self.history_table.setItem(row_num, 1, QTableWidgetItem(partner.company_name))  # Наименование партнёра
            self.history_table.setItem(row_num, 2, QTableWidgetItem(str(partner_product.quantity)))  # Количество продукции
            self.history_table.setItem(row_num, 3, QTableWidgetItem(str(partner_product.date_of_sale)))  # Дата продажи



    def create_partner_item(self, partner=None):
        item_widget = QWidget()
        layout = QVBoxLayout(item_widget)
        layout.setContentsMargins(10, 10, 10, 10)

        if partner:
            type_name = partner.type_company.name if partner.type_company else "Неизвестный тип"
            type_label = QLabel(f"{type_name} | {partner.company_name}")
            director_label = QLabel(f"Директор: {partner.director_name}")
            phone_label = QLabel(f"Телефон: {partner.phone}")
            rating_label = QLabel(f"Рейтинг: {partner.rating}")
            item_widget.setProperty("partner_id", partner.id)  # Добавляем ID партнёра как свойство
        else:
            type_label = QLabel("Тип | Наименование партнёра")
            director_label = QLabel("Директор")
            phone_label = QLabel("+7 223 322 22 32")
            rating_label = QLabel("Рейтинг: 10")

        layout.addWidget(type_label)
        layout.addWidget(director_label)
        layout.addWidget(phone_label)
        layout.addWidget(rating_label)
        item_widget.setStyleSheet("background-color: #FFFFFF; border: 1px solid #F4E8D3; padding: 5px;")
        return item_widget

    def update_tab_styles(self):
        self.partners_button.setStyleSheet("text-align: left; padding: 10px; background-color: #67BA80;" if self.partners_button.isChecked() else "background-color: #FFFFFF; color: black;")
        self.history_button.setStyleSheet("text-align: left; padding: 10px; background-color: #67BA80;" if self.history_button.isChecked() else "background-color: #FFFFFF; color: black;")


    def select_partners_tab(self):
        self.partners_button.setChecked(True)
        self.history_button.setChecked(False)
        self.update_tab_styles()
        self.right_layout.removeWidget(self.history_table)
        self.history_table.setParent(None)
        self.right_layout.addWidget(self.partners_list)


    def select_history_tab(self):
        self.history_button.setChecked(True)
        self.partners_button.setChecked(False)
        self.update_tab_styles()


        # Переключаем виджет на вкладку истории
        self.right_layout.removeWidget(self.partners_list)  # Убираем партнеров
        self.partners_list.setParent(None)
        self.right_layout.addWidget(self.history_table)  # Добавляем таблицу с историей


        # Загружаем историю продаж
        self.load_history_from_db()




    def highlight_selected_partner(self, item):
        for i in range(self.partners_list.count()):
            widget = self.partners_list.itemWidget(self.partners_list.item(i))
            widget.setStyleSheet("background-color: #FFFFFF; border: 1px solid #F4E8D3; padding: 5px;")
        selected_widget = self.partners_list.itemWidget(item)
        selected_widget.setStyleSheet("background-color: #D9E3D5; border: 1px solid #B2C8A2; padding: 5px;")


    def edit_partner(self, item):
        partner = item.data(Qt.UserRole)
        self.show_edit_partner_dialog(partner)

    def show_edit_partner_dialog(self, partner):
        dialog = QDialog(self)
        dialog.setWindowTitle("Редактировать партнёра")
        dialog.setFixedSize(300, 400)
        form_layout = QFormLayout(dialog)
        company_name_edit = QLineEdit(partner.company_name)
        ur_address_edit = QLineEdit(partner.ur_adress)
        inn_edit = QLineEdit(partner.inn)
        director_name_edit = QLineEdit(partner.director_name)
        phone_edit = QLineEdit(partner.phone)
        email_edit = QLineEdit(partner.email)
        type_company_edit = QComboBox()
        types = session.query(TypeCompany).all()
        for t in types:
            type_company_edit.addItem(t.name, t.id)
        type_company_edit.setCurrentIndex(type_company_edit.findData(partner.type_partner))
        form_layout.addRow("Название компании:", company_name_edit)
        form_layout.addRow("Юридический адрес:", ur_address_edit)
        form_layout.addRow("ИНН:", inn_edit)
        form_layout.addRow("ФИО директора:", director_name_edit)
        form_layout.addRow("Телефон:", phone_edit)
        form_layout.addRow("Email:", email_edit)
        form_layout.addRow("Тип компании:", type_company_edit)
        save_button = QPushButton("Сохранить изменения")
        form_layout.addRow(save_button)
        delete_button = QPushButton("Удалить партнёра")
        form_layout.addRow(delete_button)
        save_button.clicked.connect(lambda: self.save_partner_changes(partner, company_name_edit, ur_address_edit, inn_edit, director_name_edit, phone_edit, email_edit, type_company_edit, dialog))
        delete_button.clicked.connect(lambda: self.delete_partner(partner, dialog))
        dialog.exec()


    def save_partner_changes(self, partner, company_name_edit, ur_address_edit, inn_edit, director_name_edit, phone_edit, email_edit, type_company_edit, dialog):
        partner.company_name = company_name_edit.text()
        partner.ur_adress = ur_address_edit.text()
        partner.inn = inn_edit.text()
        partner.director_name = director_name_edit.text()
        partner.phone = phone_edit.text()
        partner.email = email_edit.text()
        partner.type_partner = type_company_edit.currentData()

        session.commit()
        dialog.accept()
        self.load_partners_from_db()


    def delete_partner(self, partner, dialog):
        reply = QMessageBox.question(self, 'Удаление партнёра', f"Вы уверены, что хотите удалить партнёра {partner.company_name}?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            session.delete(partner)
            session.commit()
            dialog.accept()  # Закрываем диалог
            self.load_partners_from_db()  # Обновляем список партнёров после удаления


    def show_add_partner_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Добавить партнёра")
        dialog.setFixedSize(300, 400)
        form_layout = QFormLayout(dialog)


        company_name_edit = QLineEdit()
        ur_address_edit = QLineEdit()
        inn_edit = QLineEdit()
        director_name_edit = QLineEdit()
        phone_edit = QLineEdit()
        email_edit = QLineEdit()


        type_company_edit = QComboBox()
        types = session.query(TypeCompany).all()
        for t in types:
            type_company_edit.addItem(t.name, t.id)


        form_layout.addRow("Название компании:", company_name_edit)
        form_layout.addRow("Юридический адрес:", ur_address_edit)
        form_layout.addRow("ИНН:", inn_edit)
        form_layout.addRow("ФИО директора:", director_name_edit)
        form_layout.addRow("Телефон:", phone_edit)
        form_layout.addRow("Email:", email_edit)
        form_layout.addRow("Тип компании:", type_company_edit)


        save_button = QPushButton("Сохранить")
        form_layout.addRow(save_button)


        save_button.clicked.connect(lambda: self.add_new_partner(company_name_edit, ur_address_edit, inn_edit, director_name_edit, phone_edit, email_edit, type_company_edit, dialog))


        dialog.exec()


    def add_new_partner(self, company_name_edit, ur_address_edit, inn_edit, director_name_edit, phone_edit, email_edit, type_company_edit, dialog):
        new_partner = Partners(
            company_name=company_name_edit.text(),
            ur_adress=ur_address_edit.text(),
            inn=inn_edit.text(),
            director_name=director_name_edit.text(),
            phone=phone_edit.text(),
            email=email_edit.text(),
            type_partner=type_company_edit.currentData()
        )
        session.add(new_partner)
        session.commit()
        dialog.accept()
        self.load_partners_from_db()





    def export_to_pdf(self):
        # Загружаем данные из базы данных
        partner_products = session.query(PartnerProduct, Product, Partners).join(
            Product, Product.id == PartnerProduct.id_product).join(
            Partners, Partners.id == PartnerProduct.id_partner).all()


        # Создаем объект PDF
        pdf = FPDF()
        pdf.add_page()

        pdf.add_font('FreeSans', 'B', './freesans.ttf', uni=True)
        # Устанавливаем шрифт
        pdf.set_font('FreeSans', 'B', 12)


        # Заголовок таблицы
        pdf.cell(200, 10, txt="Отчет по Продукции и Партнерам", ln=True, align='C')
        pdf.ln(10)  # Отступ


        # Заголовки столбцов
        pdf.cell(40, 10, "Продукция", border=1)
        pdf.cell(50, 10, "Наименование партнера", border=1)
        pdf.cell(40, 10, "Количество", border=1)
        pdf.cell(40, 10, "Дата продажи", border=1)
        pdf.ln()  # Переход на новую строку


        # Добавляем строки с данными
        for partner_product, product, partner in partner_products:
            pdf.cell(40, 10, str(product.description), border=1)
            pdf.cell(50, 10, str(partner.company_name), border=1)
            pdf.cell(40, 10, str(partner_product.quantity), border=1)
            pdf.cell(40, 10, str(partner_product.date_of_sale), border=1)
            pdf.ln()


        # Сохраняем PDF на диск
        pdf_output_path = "./partner_products_report.pdf"
        pdf.output(pdf_output_path)


        # Показать сообщение о завершении
        QMessageBox.information(self, "Экспорт завершен", f"Отчет был успешно экспортирован в {pdf_output_path}.")




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MasterApp()
    window.show()
    sys.exit(app.exec())