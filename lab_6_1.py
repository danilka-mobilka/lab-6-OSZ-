import numpy as np

def create_ascii_image(width=40, height=20):
    #Створює тестове ASCII зображення#
    # Створюємо матрицю яскравості
    img = np.zeros((height, width), dtype=np.uint8)
    
    # Додаємо різні області
    # Темна область (25%)
    img[2:8, 5:15] = 50
    
    # Середня яскравість (50%)
    img[2:8, 20:30] = 128
    
    # Яскрава область (75%)
    img[2:8, 32:38] = 200
    
    # Градієнт
    for i in range(10, 30):
        img[12:16, i] = i * 4
    
    # Вертикальна смуга
    img[5:15, 10:12] = 150
    
    return img

def binary_transform(image, threshold=128):
    #Бінаризація#
    return np.where(image > threshold, 255, 0).astype(np.uint8)

def negative_transform(image):
    #Негатив#
    return 255 - image

def logarithmic_transform(image):
    #Логарифмічне перетворення#
    c = 255 / np.log(1 + np.max(image))
    log_img = c * np.log(1 + image.astype(np.float32))
    return np.uint8(np.clip(log_img, 0, 255))

def gamma_transform(image, gamma=2.2):
    #Гамма-корекція#
    gamma_corrected = np.power(image.astype(np.float32) / 255.0, 1/gamma) * 255
    return np.uint8(np.clip(gamma_corrected, 0, 255))

def solarization_transform(image, threshold=128):
    #Соляризація#
    solarized = image.copy()
    mask = solarized > threshold
    solarized[mask] = 255 - solarized[mask]
    return solarized

def image_to_ascii(image, width=40, height=20):
    #Перетворює матрицю яскравості в ASCII art#
    # Символи від темного до світлого
    ascii_chars = " .:-=+*#%@"
    
    # Масштабуємо зображення до потрібного розміру
    scale_x = image.shape[1] // width
    scale_y = image.shape[0] // height
    
    ascii_art = []
    for y in range(0, image.shape[0], scale_y):
        if len(ascii_art) >= height:
            break
        row = ""
        for x in range(0, image.shape[1], scale_x):
            if len(row) >= width:
                break
            # Беремо середнє значення яскравості в області
            region = image[y:y+scale_y, x:x+scale_x]
            if region.size > 0:
                brightness = np.mean(region)
                # Конвертуємо яскравість в ASCII символ
                char_index = min(int(brightness / 25.5), 9)
                row += ascii_chars[char_index]
        ascii_art.append(row)
    
    return ascii_art

def display_transformations():
    #Відображає всі перетворення в консолі#
    print("=" * 60)
    print("ПОРІВНЯННЯ ПЕРЕТВОРЕНЬ ЗОБРАЖЕНЬ")
    print("=" * 60)
    
    # Створюємо оригінальне зображення
    original = create_ascii_image()
    
    # Застосовуємо перетворення
    binary = binary_transform(original, 128)
    negative = negative_transform(original)
    logarithmic = logarithmic_transform(original)
    gamma = gamma_transform(original, 2.2)
    solarization = solarization_transform(original, 128)
    
    # Конвертуємо в ASCII
    transforms = [original, binary, negative, logarithmic, gamma, solarization]
    titles = [
        "ОРИГІНАЛ",
        "БІНАРИЗАЦІЯ (T=128)",
        "НЕГАТИВ", 
        "ЛОГАРИФМІЧНЕ",
        "ГАММА-КОРЕКЦІЯ (γ=2.2)",
        "СОЛЯРИЗАЦІЯ (T=128)"
    ]
    
    # Відображаємо всі перетворення
    for i, (img, title) in enumerate(zip(transforms, titles)):
        print(f"\n{title}:")
        print("-" * 40)
        
        ascii_art = image_to_ascii(img)
        for row in ascii_art:
            print(row)
        
        # Статистика
        stats = f"Мін: {np.min(img):3d} | Макс: {np.min(img):3d} | Сер: {np.mean(img):5.1f}"
        print(f"Статистика: {stats}")
    
    # Пояснення символів
    print("\n" + "=" * 60)
    print("ПОЯСНЕННЯ СИМВОЛІВ (від темного до світлого):")
    print("  (пробіл) . : - = + * # % @")
    print("  0%      10% 20% 30% 40% 50% 60% 70% 80% 90% 100%")
    print("=" * 60)

def show_histogram_ascii(image, title, width=50):
    #Відображає гістограму в ASCII#
    print(f"\nГІСТОГРАМА: {title}")
    print("-" * (width + 10))
    
    # Рахуємо гістограму
    hist, bins = np.histogram(image, bins=10, range=(0, 255))
    max_count = max(hist)
    
    for i in range(10):
        level = f"{i*25:3d}-{(i+1)*25:3d}:"
        bar_length = int((hist[i] / max_count) * width) if max_count > 0 else 0
        bar = "█" * bar_length
        count = f"({hist[i]} пікселів)"
        print(f"{level} {bar} {count}")

def display_histograms():
    #Відображає гістограми всіх перетворень#
    print("\n" + "=" * 60)
    print("ГІСТОГРАМИ РОЗПОДІЛУ ЯСКРАВОСТІ")
    print("=" * 60)
    
    original = create_ascii_image()
    
    transforms = [
        (original, "ОРИГІНАЛ"),
        (binary_transform(original, 128), "БІНАРИЗАЦІЯ"),
        (negative_transform(original), "НЕГАТИВ"),
        (logarithmic_transform(original), "ЛОГАРИФМІЧНЕ"),
        (gamma_transform(original, 2.2), "ГАММА-КОРЕКЦІЯ"),
        (solarization_transform(original, 128), "СОЛЯРИЗАЦІЯ")
    ]
    
    for img, title in transforms:
        show_histogram_ascii(img, title)

def main():
    #Основна функція#
    display_transformations()
    display_histograms()
    
    print("\n" + "=" * 60)
    print("ОПИС ПЕРЕТВОРЕНЬ:")
    print("1. Бінаризація - перетворює в чорно-біле за порогом")
    print("2. Негатив - інвертує яскравість пікселів") 
    print("3. Логарифмічне - підсилює темні ділянки")
    print("4. Гамма-корекція - коригує яскравість (γ<1 - темніше, γ>1 - світліше)")
    print("5. Соляризація - часткова інверсія яскравості")
    print("=" * 60)

if __name__ == "__main__":
    main()
