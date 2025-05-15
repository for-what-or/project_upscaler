import os

def load_model_list(models_path):
    # Загрузка списка моделей
    models = []
    for file in os.listdir(models_path):
        if file.endswith(".pth"):
            models.append(file[:-4])
    return models