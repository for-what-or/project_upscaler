import json
import numpy as np
import streamlit as st
import time
from io import BytesIO
from PIL import Image
from src.model import *
from src.model_folder import *
from src.ui.dialogs import *
from streamlit_image_comparison import image_comparison

config = json.load(open('src/config.json'))
model_list = json.load(open('src/model_list.json'))

models_path = config["models_path"]
model_edit_permission = config["model_edit_permission"]

@st.cache_resource
def get_model(model_type):
    return load_sr_model(models_path + '/' + model_type + '.pth')

def main():
    model_list = json.load(open('src/model_list.json'))
    st.set_page_config(
        page_title="Апскейлер",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("🖼️ Апскейлер изображений")
    st.markdown("""
    Увеличение разрешения изображений с помощью нейронных сетей.  
    Поддерживает обработку больших изображений по частям.
    """)

    with st.sidebar:
        if st.button("Инструкция"):
            instruction_dialog()

        st.header("⚙️ Настройки")
        
        model_device = st.radio(
            "Устройство",
            ["cuda"],
            index=0,
            help="Выберите устройство для обработки изображений (рекомендуется cuda)"
        )
        
        model_type = st.radio(
            "Модели",
            load_model_list(models_path),
            index=0,
            help="Выберите модель нейросети"
        )
        
        if st.button("Управление моделями"):
            # Окно для управления моделями
            if model_edit_permission:
                manage_models_dialog()
            else:
                st.error("Доступ запрещен")

        selected_model = next((model for model in model_list if model["model_name"] == model_type), None)
        scale_factor = selected_model["scale_factor"] if selected_model else 1
        st.info(f"Коэффициент увеличения для модели **{model_type}: {selected_model['scale_factor']}**")
        
        tile_size = st.slider(
            "Размер тайла",
            32, 512, 128,
            help="Меньшие значения для экономии памяти, большие для скорости"
        )
        
        show_metrics = st.checkbox("Показать метрики качества", False)

    col1, col2 = st.columns(2)
    proc_time = 0
    with col1:
        global image
        image = None
        uploaded_file = st.file_uploader(
            "📤 Загрузите изображение",
            type=["jpg", "png", "jpeg"],
            help="Поддерживаются файлы JPG, JPEG и PNG."
        )
        
        if uploaded_file:
            image = Image.open(uploaded_file)
            '''st.image(
                image,
                caption="Исходное изображение",
                use_container_width=True
            )'''

    with col2:
        global result_img
        result_img = None
        if uploaded_file:
            if st.button("🚀 Увеличить разрешение", type="primary"):
                start_time = time.time()
                device = torch.device(model_device if torch.cuda.is_available() else "cpu")

                with st.spinner("Загрузка модели..."):
                    model = get_model(model_type)
                
                model.to(device)
                
                with st.spinner("Обработка изображения..."):
                    tiles, positions = split_image(image, tile_size)
                    processed_tiles = []
                    
                    
                    progress_text = "Обработка тайлов."
                    my_bar = st.progress(0, text=progress_text)

                    for i, tile in enumerate(tiles):
                        with torch.no_grad():
                            processed_tile = model(tile)
                        processed_tiles.append(processed_tile)
                        progress_text = f"Обработано тайлов. ({i+1}/{len(tiles)})"
                        my_bar.progress(int((i+1)/len(tiles)*100), text=progress_text)
                    
                    result = merge_tiles(processed_tiles, positions, image.size, scale_factor)
                    
                    result_img = result.permute(1, 2, 0).clamp(0, 1).cpu().numpy()
                    result_img = Image.fromarray((result_img * 255).astype(np.uint8))
                
                proc_time = time.time() - start_time
                
                '''st.image(
                    result_img,
                    caption=f"Увеличенное изображение",
                    use_container_width=True
                )'''
                
                # Кнопка скачивания
                buf = BytesIO()
                result_img.save(buf, format="PNG")
                st.download_button(
                    "Скачать результат",
                    buf.getvalue(),
                    f"upscaled_picture.png",
                    "image/png"
                )
                
    if image and result_img:
        image_comparison(
            img1=image,
            img2=result_img,
            width=1280,
            label1="Исходное изображение",
            label2="Результат",
        )
    
    if show_metrics:
        st.subheader("📊 Метрики")
        st.metric("Время обработки", f"{proc_time:.2f} сек")
        st.metric("Размер оригинала", f"{image.size[0]}x{image.size[1]}")
        st.metric("Размер результата", f"{result_img.size[0]}x{result_img.size[1]}")