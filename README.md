## Инструменты для машинного обучения

- **Язык программирования**: Python - наиболее подходящий для задач машинного обучения.
- **Библиотеки для обработки изображений**:
  - Pillow
- **Интерфейс**:
  - Streamlit - для создания пользовательского интерфейса.

```sh
pip install -r docs/requirements.txt
```

To create a `setup.py` file in the root directory, you can use the following command:

```sh
touch setup.py
```

Then, add the following content to the `setup.py` file:

```python
from setuptools import setup, find_packages

setup(
    name="project_upscaler",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        
    ],
)
```

- [torch](https://pytorch.org/get-started/locally/)
