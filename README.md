# **Апскейлер изображений**
Этот проект предназначен для увеличения разрешения фотографий.

## **Используемый инструментарий**
В проекте использовались следующие стеки технологий :
- **Язык программирования**:
  - [Python](https://www.python.org/downloads/)
- **Фреймворк для работы с архитектурами нейросетей**:
  - [PyTorch](https://pytorch.org/get-started/locally/)
- **Универсализация взаимодействий с архитектурами**:
  - [Spandrel](https://pypi.org/project/spandrel/)
- **Библиотеки для обработки изображений**:
  - [Pillow](https://pypi.org/project/pillow/)
- **Интерфейс**:
  - [Streamlit](https://pypi.org/project/streamlit/) - для создания пользовательского интерфейса.
  - Был взят модуль для Streamlit под названием [streamlit_image_comparison](https://pypi.org/project/streamlit-image-comparison/), созданный сообществом.
- **Дополнительный библиотеки**:
  - [Numpy](https://pypi.org/project/numpy/)
  - [Tqdm](https://pypi.org/project/tqdm/)
  - [Matplotlib](https://pypi.org/project/matplotlib/)

## **Автоматическая установка и запуск**
Для автоматической установки и запуска проекта необходимо выполнить следующие действия.
1. Установить последнюю версию [Python](https://www.python.org/downloads/), если таковой не имеется.
2. Загрузить репозиторий на компьютер.
3. Запустить файл `setup_and_run.bat` от имени администратора.
4. Откроется окно со страницей проекта.
5. Готово

Останавливается веб-приложение закрытием консольного окна с запущенной программой.

## **Ручная установка и запуск**

Для ручной установки и запуска выполните следующие действия:
- Выполнить первые два шага из раздела автоматической установки.
- Создайте новое окружение и активируйте его:
  ```sh
  python -m venv venv
  venv/Scripts/Activate
  ```
- Установить [PyTorch](https://pytorch.org/get-started/locally/) соответствующий вашему компьютеру.\
  Например выполнив следующую строку:
  ```sh
  pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
  ```
  Либо же другой командой, представленной на [сайте](https://pytorch.org/get-started/locally/).
- Установить необходимые зависимости:
  ```sh
  pip install -r requirements.txt
  ```
- Запустить проект
  ```sh
  streamlit run app.py
  ```

## **Создатель**
Студент Уфимского университета науки и технологий, группы ПРО-433б Калямов Ильфат.\
Для связи:
- [Telegram](https://t.me/for_what_or).
- [VK](https://vk.com/for_what_or)