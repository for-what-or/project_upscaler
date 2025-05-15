import streamlit as st
import os
import json
import time
from src.model_folder import *

config = json.load(open('src/config.json'))
models_path = config["models_path"]
model_edit_permission = config["model_edit_permission"]

@st.dialog("Инструкции")
def instruction_dialog():
    st.subheader("Как использовать приложение")
    st.markdown("""
    1. **Выберите модель**: В боковой панели выберите архитектуру модели, которую хотите использовать.
    2. **Настройте параметры**: Установите параметры, такие как устройство обработки и размер тайла.
    3. **Загрузите изображение**: Используйте кнопку загрузки, чтобы выбрать изображение, которое нужно увеличить.
    4. **Запустите обработку**: Нажмите кнопку для начала увеличения разрешения изображения.
    5. **Просмотрите результат**: После завершения обработки вы сможете увидеть и скачать увеличенное изображение.
    """)

@st.dialog("Управление моделями")
def manage_models_dialog():
    st.subheader("Модели")
    models = load_model_list(models_path)
    st.markdown("### List of Elements")
    st.markdown("\n".join([f"- {e}" for e in models]))
    
    uploaded_file = st.file_uploader(
        "Добавить модель из файла",
        type=["pth"],
        help="Выберите файл модели в формате .pth"
    )
    if uploaded_file:
        model_name = os.path.basename(uploaded_file.name)[:-4]
        model_path = os.path.join(models_path, model_name + ".pth")
        scale_factor = st.number_input(
            "Коэффициент увеличения",
            value=2
        )
        if st.button("Добавить"):
            with open('src/model_list.json', 'r+') as f:
                data = json.load(f)
                if not any(item["model_name"] == model_name for item in data):
                    data.append({"model_name": model_name, "scale_factor": scale_factor})
                    f.seek(0)
                    json.dump(data, f, indent=4)
                    f.truncate()
            if not os.path.exists(model_path):
                with open(model_path, "wb") as f:
                    f.write(uploaded_file.read())
                st.info(f"Модель {model_name} с коэффициентом {scale_factor} добавлена")
                time.sleep(1)
                st.rerun()
            else:
                st.error(f"Модель {model_name} уже существует")
        
    remove_model = st.selectbox(
        "Удалить модель",
        models,
        index=0
    )
    if st.button("Удалить"):
        model_path = os.path.join(models_path, remove_model + ".pth")
        if os.path.exists(model_path):
            os.remove(model_path)
            with open('src/model_list.json', 'r+') as f:
                data = json.load(f)
                data = [item for item in data if item["model_name"] != remove_model]
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()
            st.info(f"Модель {remove_model} удалена")
            time.sleep(1)
            st.rerun()

        else:
            st.error(f"Модель {remove_model} не существует")