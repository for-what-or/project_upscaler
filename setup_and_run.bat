@echo off
REM ==============================================
REM setup_and_run.bat
REM Автоматическая установка и запуск Streamlit-приложения
REM ==============================================

:: 1. Проверка Python
echo [1/4] Проверяем наличие Python...
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo ОШИБКА: Python не установлен!
    echo Скачайте его с https://www.python.org/downloads/
    pause
    exit /b
)

:: 2. Создание виртуального окружения
set VENV_NAME=venv
echo [2/4] Создаем виртуальное окружение...
python -m venv %VENV_NAME%

:: 3. Установка зависимостей
echo [3/4] Устанавливаем зависимости...
call %VENV_NAME%\Scripts\activate.bat
python -m pip install --upgrade pip

:: Установка PyTorch с CUDA 12.8
echo Устанавливаем PyTorch (CUDA 12.8)...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128

:: Дополнительные зависимости
if exist requirements.txt (
    echo Устанавливаем зависимости из requirements.txt...
    pip install -r requirements.txt
) else (
    echo Устанавливаем только Streamlit...
    pip install streamlit
)

:: 4. Запуск приложения
set APP_FILE=app.py
echo [4/4] Запускаем приложение...
echo ---------------------------------------------
streamlit run %APP_FILE%

pause