import cv2
import numpy as np

# Открываем три камеры (номера могут быть 0, 1, 2 и т.д.)
cap1 = cv2.VideoCapture(5)  # Первая камера
cap2 = cv2.VideoCapture(4)  # Вторая камера
cap3 = cv2.VideoCapture(3)  # Третья камера

# Проверяем, удалось ли открыть камеры
if not (cap1.isOpened() and cap2.isOpened() and cap3.isOpened()):
    print("Ошибка: Не удалось открыть одну или несколько камер!")
    exit()

while True:
    # Читаем кадры с каждой камеры
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()
    ret3, frame3 = cap3.read()

    # Если кадр не получен, пропускаем
    if not (ret1 and ret2 and ret3):
        print("Ошибка: Не удалось получить кадр с одной из камер!")
        break

    # Изменяем размер кадров (опционально, для удобства)
    frame1 = cv2.resize(frame1, (640, 480))
    frame2 = cv2.resize(frame2, (640, 480))
    frame3 = cv2.resize(frame3, (640, 480))

    # Объединяем кадры в одну большую картинку (горизонтально)
    combined_frame = np.hstack((frame1, frame2, frame3))

    # Выводим результат
    cv2.imshow('Multi-Camera Stream', combined_frame)

    # Выход по нажатию 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Освобождаем ресурсы
cap1.release()
cap2.release()
cap3.release()
cv2.destroyAllWindows()