-- Создание таблицы типов компаний
CREATE TABLE type_company (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);


-- Добавление нескольких типов компаний для примера
INSERT INTO type_company (name) VALUES
('Тип 1'),
('Тип 2'),
('Тип 3'),
('Тип 4'),
('Тип 5');


-- Создание таблицы партнеров
CREATE TABLE partners (
    id SERIAL PRIMARY KEY,
    type_partner INT REFERENCES type_company(id),
    company_name VARCHAR(255) NOT NULL,
    ur_adress VARCHAR(255) NOT NULL,
    inn VARCHAR(50) NOT NULL,
    director_name VARCHAR(255) NOT NULL,
    phone VARCHAR(50) NOT NULL,
    email VARCHAR(255) NOT NULL,
    rating INT
);


-- Создание таблицы типов продукции
CREATE TABLE product_type (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    coefficient FLOAT NOT NULL
);


-- Добавление типов продукции
INSERT INTO product_type (name, coefficient) VALUES
('Тип продукции 1', 1.0),
('Тип продукции 2', 1.2),
('Тип продукции 3', 1.5),
('Тип продукции 4', 2.0),
('Тип продукции 5', 2.5);


-- Создание таблицы продуктов
CREATE TABLE product (
    id SERIAL PRIMARY KEY,
    type INT REFERENCES product_type(id),
    description VARCHAR(255),
    article INT,
    price FLOAT,
    size FLOAT,
    class_id INT
);


-- Добавление нескольких продуктов
INSERT INTO product (type, description, article, price, size, class_id) VALUES
(1, 'Продукт 1', 1001, 500.0, 10.0, 1),
(2, 'Продукт 2', 1002, 750.0, 12.0, 2),
(3, 'Продукт 3', 1003, 1000.0, 15.0, 3),
(4, 'Продукт 4', 1004, 1500.0, 18.0, 4),
(5, 'Продукт 5', 1005, 2000.0, 20.0, 5);


-- Создание таблицы материалов
CREATE TABLE material (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    defect FLOAT
);


-- Добавление нескольких материалов
INSERT INTO material (name, defect) VALUES
('Материал 1', 0.05),
('Материал 2', 0.10),
('Материал 3', 0.02),
('Материал 4', 0.15),
('Материал 5', 0.08);


-- Создание таблицы связи между продуктами и материалами
CREATE TABLE material_product (
    id SERIAL PRIMARY KEY,
    id_product INT REFERENCES product(id),
    id_material INT REFERENCES material(id)
);


-- Добавление связей между продуктами и материалами
INSERT INTO material_product (id_product, id_material) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5);

-- Сначала добавим данные в таблицу partners
INSERT INTO partners (type_partner, company_name, ur_adress, inn, director_name, phone, email, rating)
VALUES
(1, 'Компания 1', 'Адрес 1', '1234567890', 'Директор 1', '123-45-67', 'company1@mail.com', 5),
(2, 'Компания 2', 'Адрес 2', '2345678901', 'Директор 2', '234-56-78', 'company2@mail.com', 4),
(3, 'Компания 3', 'Адрес 3', '3456789012', 'Директор 3', '345-67-89', 'company3@mail.com', 3),
(4, 'Компания 4', 'Адрес 4', '4567890123', 'Директор 4', '456-78-90', 'company4@mail.com', 2),
(5, 'Компания 5', 'Адрес 5', '5678901234', 'Директор 5', '567-89-01', 'company5@mail.com', 1);





-- Создание таблицы для партнерских продуктов (история продаж)
CREATE TABLE partner_product (
    id SERIAL PRIMARY KEY,
    id_product INT REFERENCES product(id),
    id_partner INT REFERENCES partners(id),
    quantity INT,
    date_of_sale DATE
);


-- Теперь добавим данные в таблицу partner_product
INSERT INTO partner_product (id_product, id_partner, quantity, date_of_sale)
VALUES
(1, 1, 100, '2024-11-01'),
(2, 2, 150, '2024-11-02'),
(3, 3, 200, '2024-11-03'),
(4, 4, 250, '2024-11-04'),
(5, 5, 300, '2024-11-05');

