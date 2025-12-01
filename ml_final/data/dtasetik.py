import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_price_history(products_count=30, days=90):
    """
    Генерирует историю цен для товаров на 90 дней
    """
    # Базовые цены для разных категорий товаров (в рублях)
    base_prices = {
        2: 50000,  # Смартфоны
        3: 80000,  # Ноутбуки
        4: 15000,  # Наушники
        6: 5000    # Техника для кухни
    }
    
    price_history = []
    history_id = 1
    
    # Дата начала отслеживания
    start_date = datetime.now() - timedelta(days=days)
    
    for product_id in range(1, products_count + 1):
        # Определяем категорию товара
        if product_id <= 7:
            category_id = 2  # Смартфоны
        elif product_id <= 14:
            category_id = 3  # Ноутбуки
        elif product_id <= 20:
            category_id = 4  # Наушники
        else:
            category_id = 6  # Техника для кухни
        
        # Базовая цена с вариациями
        base_price = base_prices[category_id] * random.uniform(0.8, 1.2)
        current_price = base_price
        
        for day in range(days):
            date = start_date + timedelta(days=day)
            
            # Генерируем изменение цены
            change_percent = np.random.normal(0, 0.02)  # Среднее изменение 0%, std 2%
            
            # Сезонные эффекты (пятница/выходные - рост, понедельник - спад)
            if date.weekday() in [4, 5, 6]:  # Пятница, суббота, воскресенье
                change_percent += 0.01
            elif date.weekday() == 0:  # Понедельник
                change_percent -= 0.005
            
            # Случайные акции и распродажи
            if random.random() < 0.05:  # 5% вероятность акции
                change_percent -= random.uniform(0.1, 0.3)  # Скидка 10-30%
            
            # Применяем изменение цены
            price_change = current_price * change_percent
            current_price += price_change
            
            # Ограничиваем минимальную цену (не менее 50% от базовой)
            current_price = max(current_price, base_price * 0.5)
            
            # Округляем до кратного 10 рублям
            current_price = round(current_price / 10) * 10
            
            price_history.append({
                'id': history_id,
                'product_id': product_id,
                'price': float(current_price),
                'created_at': date.strftime('%Y-%m-%d %H:%M:%S')
            })
            
            history_id += 1
    
    return pd.DataFrame(price_history)

def generate_products_dataset():
    """
    Создает датасет товаров (уже предоставлен в задании)
    """
    products = []
    
    # Смартфоны (1-7)
    smartphones = [
        (1, '482159736', 'Смартфон iPhone 15 128GB', 2, 'Apple'),
        (2, '5938472610', 'Смартфон iPhone 15 256GB', 2, 'Apple'),
        (3, '620184735', 'Смартфон Samsung Galaxy S24 128GB', 2, 'Samsung'),
        (4, '7493825160', 'Смартфон Samsung Galaxy S23 256GB', 2, 'Samsung'),
        (5, '815937402', 'Смартфон Xiaomi 13 Lite 128GB', 2, 'Xiaomi'),
        (6, '9264738151', 'Смартфон Xiaomi Redmi Note 12 128GB', 2, 'Xiaomi'),
        (7, '1038574926', 'Смартфон OPPO Reno 10 256GB', 2, 'OPPO')
    ]
    
    # Ноутбуки (8-14)
    laptops = [
        (8, '284619537', 'Ноутбук MacBook Pro 14" M3 512GB', 3, 'Apple'),
        (9, '3957281640', 'Ноутбук MacBook Air 13" M2 256GB', 3, 'Apple'),
        (10, '462839175', 'Ноутбук ASUS VivoBook 15 i5 512GB', 3, 'ASUS'),
        (11, '5739462810', 'Ноутбук ASUS ZenBook 13 i7 1TB', 3, 'ASUS'),
        (12, '684157392', 'Ноутбук Lenovo IdeaPad 5 i5 512GB', 3, 'Lenovo'),
        (13, '7952684031', 'Ноутбук Lenovo ThinkPad T14 i7 512GB', 3, 'Lenovo'),
        (14, '826394715', 'Ноутбук HP Envy 13 i5 512GB', 3, 'HP')
    ]
    
    # Наушники (15-20)
    headphones = [
        (15, '9374851260', 'Наушники AirPods Pro 2', 4, 'Apple'),
        (16, '148259637', 'Наушники AirPods 3', 4, 'Apple'),
        (17, '2593671480', 'Наушники Sony WH-1000XM5', 4, 'Sony'),
        (18, '360478259', 'Наушники Sony LinkBuds S', 4, 'Sony'),
        (19, '4715893601', 'Наушники Samsung Galaxy Buds2 Pro', 4, 'Samsung'),
        (20, '582690471', 'Наушники JBL Tune 770NC', 4, 'JBL')
    ]
    
    # Техника для кухни (21-30)
    kitchen = [
        (21, '6937015820', 'Электрочайник Philips HD9359 1.7L', 6, 'Philips'),
        (22, '704812693', 'Электрочайник Tefal KO851 1.7L', 6, 'Tefal'),
        (23, '8159237041', 'Электрочайник Bosch TWK 550', 6, 'Bosch'),
        (24, '926034815', 'Блендер Braun Multiquick 7 MQ 7045', 6, 'Braun'),
        (25, '1371459260', 'Блендер Philips HR3556 2L', 6, 'Philips'),
        (26, '248256137', 'Блендер Moulinex LM935 1.5L', 6, 'Moulinex'),
        (27, '3593672480', 'Кофеварка DeLonghi ECAM 320', 6, 'DeLonghi'),
        (28, '460478359', 'Кофеварка Philips EP5400', 6, 'Philips'),
        (29, '5715894601', 'Тостер Bosch TAT 7A1', 6, 'Bosch'),
        (30, '682690571', 'Тостер Tefal Toast & Go TT1', 6, 'Tefal')
    ]
    
    all_products = smartphones + laptops + headphones + kitchen
    
    for product in all_products:
        products.append({
            'id': product[0],
            'article': product[1],
            'name': product[2],
            'category_id': product[3],
            'brand': product[4],
            'image_url': f"/images/product_{product[0]}.jpg",
            'description': f"Описание товара {product[2]}"
        })
    
    return pd.DataFrame(products)

# Генерируем датасеты
print("Генерация датасета товаров...")
products_df = generate_products_dataset()

print("Генерация истории цен на 90 дней...")
price_history_df = generate_price_history(30, 90)

# Сохраняем в CSV
products_df.to_csv('products_dataset.csv', index=False, encoding='utf-8')
price_history_df.to_csv('price_history_dataset.csv', index=False, encoding='utf-8')

# Выводим статистику
print(f"\n✅ Сгенерировано товаров: {len(products_df)}")
print(f"✅ Сгенерировано записей истории цен: {len(price_history_df)}")
print(f"✅ Период покрытия: {price_history_df['created_at'].min()} - {price_history_df['created_at'].max()}")

# Показываем пример данных
print("\nПример товаров:")
print(products_df.head(3).to_string(index=False))

print("\nПример истории цен:")
print(price_history_df.head(5).to_string(index=False))

# Аналитика по ценам
print(f"\n📊 Статистика цен:")
print(f"Средняя цена: {price_history_df['price'].mean():.2f} руб.")
print(f"Минимальная цена: {price_history_df['price'].min():.2f} руб.")
print(f"Максимальная цена: {price_history_df['price'].max():.2f} руб.")
print(f"Стандартное отклонение: {price_history_df['price'].std():.2f} руб.")