# YOLO11 Object Detection on X-Ray ID (Roboflow)

- Кастомное обучение YOLO11 для детекции меток на рентгеновских снимках.
- Датасет: [X-Ray ID (Roboflow)](https://universe.roboflow.com/rf-projects/x-ray-id)
- Модель: yolov11n.pt
- Основные этапы:
  - Загрузка датасета через Roboflow API
  - Обучение и валидация YOLO11
  - Визуализация результатов
 
Результат работы модели:
![Sample prediction](res1.jpg)
![Sample prediction](res2.jpg)
![Sample prediction](res3.jpg)


Матрица корреляция для тренировочной выборки
![confusion_matrix](conf_mat.png)
