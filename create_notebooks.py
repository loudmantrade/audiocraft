#!/usr/bin/env python3
"""
Скрипт для создания Jupyter notebooks для Google Colab
"""
import json

# Notebook 1: Простой setup для Colab
colab_simple = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# AudioCraft в Google Colab - Простая установка\n",
                "\n",
                "Этот notebook поможет быстро запустить AudioCraft в Google Colab.\n",
                "\n",
                "⚠️ **Важно:** Включите GPU (Runtime → Change runtime type → T4 GPU)"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## 1. Проверка окружения"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import sys\n",
                "print(f'Python: {sys.version}')\n",
                "\n",
                "import torch\n",
                "print(f'PyTorch: {torch.__version__}')\n",
                "print(f'CUDA: {torch.cuda.is_available()}')\n",
                "if torch.cuda.is_available():\n",
                "    print(f'GPU: {torch.cuda.get_device_name(0)}')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## 2. Установка ffmpeg"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "!apt-get update -qq\n",
                "!apt-get install -y -qq ffmpeg\n",
                "\n",
                "# Устанавливаем dev-библиотеки для сборки пакета av\n",
                "!apt-get install -y -qq libavformat-dev libavcodec-dev libavdevice-dev libavutil-dev libswscale-dev libavresample-dev\n",
                "\n",
                "!ffmpeg -version | head -n 1\n",
                "print('✓ FFmpeg и dev-библиотеки установлены')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## 3. Клонирование AudioCraft"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import os\n",
                "\n",
                "# Клонируем если еще не клонировали\n",
                "if not os.path.exists('/content/audiocraft'):\n",
                "    !git clone https://github.com/facebookresearch/audiocraft.git\n",
                "    print('✓ Репозиторий клонирован')\n",
                "else:\n",
                "    print('✓ Репозиторий уже существует')\n",
                "\n",
                "# Переходим в папку\n",
                "%cd /content/audiocraft\n",
                "\n",
                "# Проверяем наличие setup.py\n",
                "if os.path.exists('setup.py'):\n",
                "    print('✓ setup.py найден')\n",
                "    !ls -la setup.py\n",
                "else:\n",
                "    print('❌ setup.py не найден!')\n",
                "    print('Содержимое текущей директории:')\n",
                "    !pwd\n",
                "    !ls -la"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## 4. Установка зависимостей для Python 3.12"]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "⚠️ **Примечание о предупреждениях numpy:**\n",
                "\n",
                "После установки вы увидите предупреждения типа:\n",
                "```\n",
                "ERROR: ... requires numpy>=2, but you have numpy 1.26.4\n",
                "```\n",
                "\n",
                "**Это нормально и безопасно!** Конфликтующие пакеты (cupy, jax, opencv, tobler) не используются AudioCraft. Все необходимые компоненты будут работать корректно."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Обновляем pip\n",
                "!pip install -q --upgrade pip setuptools wheel\n",
                "\n",
                "print('Установка зависимостей для AudioCraft...')\n",
                "print('⚠️  Вы увидите предупреждения о конфликтах numpy - это нормально!')\n",
                "print('   Предустановленные пакеты Colab требуют numpy 2.x,')\n",
                "print('   но AudioCraft работает только с numpy 1.x')\n",
                "print('   Конфликтующие пакеты (opencv, jax, cupy) не используются AudioCraft.\\n')\n",
                "\n",
                "# Критичные пакеты для Python 3.12\n",
                "!pip install -q 'numpy<2.0'\n",
                "!pip install -q 'transformers>=4.35.0'\n",
                "!pip install -q 'gradio>=4.0.0'\n",
                "!pip install -q 'hydra-core>=1.3'\n",
                "\n",
                "print('\\n✓ Основные зависимости установлены')\n",
                "print('✓ Предупреждения о numpy можно игнорировать')"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Убедимся что мы в правильной директории\n",
                "import os\n",
                "print(f'Текущая директория: {os.getcwd()}')\n",
                "\n",
                "if not os.path.exists('setup.py'):\n",
                "    print('❌ Ошибка: setup.py не найден в текущей директории!')\n",
                "    print('Попробуйте перезапустить с ячейки 3 (клонирование)')\n",
                "else:\n",
                "    # Установка пакета av (требует FFmpeg dev-библиотек)\n",
                "    print('Установка av (Python bindings для FFmpeg)...')\n",
                "    !pip install -q av\n",
                "    \n",
                "    # Установка AudioCraft\n",
                "    print('Установка AudioCraft...')\n",
                "    !pip install -q -e .\n",
                "    print('✓ AudioCraft установлен')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## 5. Проверка установки"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "print('Проверка критичных компонентов...')\n",
                "\n",
                "import numpy as np\n",
                "print(f'✓ NumPy: {np.__version__}')\n",
                "\n",
                "import torch\n",
                "print(f'✓ PyTorch: {torch.__version__}')\n",
                "print(f'  CUDA: {torch.cuda.is_available()}')\n",
                "\n",
                "import transformers\n",
                "print(f'✓ Transformers: {transformers.__version__}')\n",
                "\n",
                "import audiocraft\n",
                "print(f'✓ AudioCraft: {audiocraft.__version__}')\n",
                "\n",
                "from audiocraft.models import MusicGen\n",
                "print('✓ MusicGen доступен')\n",
                "\n",
                "from audiocraft.models import AudioGen  \n",
                "print('✓ AudioGen доступен')\n",
                "\n",
                "print('\\n✅ Все компоненты работают корректно!')\n",
                "print('   (Предупреждения о numpy можно игнорировать)')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## 6. Тестовая генерация музыки"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "from audiocraft.models import MusicGen\n",
                "from IPython.display import Audio\n",
                "\n",
                "# Загружаем маленькую модель\n",
                "print('Загрузка модели...')\n",
                "model = MusicGen.get_pretrained('facebook/musicgen-small')\n",
                "print(f'✓ Модель загружена: {model.name}')"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Настройка параметров\n",
                "model.set_generation_params(\n",
                "    duration=8,\n",
                "    temperature=1.0,\n",
                "    top_k=250,\n",
                ")\n",
                "\n",
                "# Генерация\n",
                "descriptions = ['upbeat electronic dance music with synthesizers']\n",
                "print('Генерация...')\n",
                "wav = model.generate(descriptions)\n",
                "\n",
                "print(f'✓ Сгенерировано: {wav.shape}')\n",
                "\n",
                "# Воспроизведение\n",
                "display(Audio(wav[0].cpu().numpy(), rate=model.sample_rate))"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 7. Запуск Gradio интерфейса\n",
                "\n",
                "Запустите веб-интерфейс для удобной генерации:"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": ["!python -m demos.musicgen_app --share"]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Готово! 🎉\n",
                "\n",
                "Теперь можете:\n",
                "- Генерировать музыку с разными описаниями\n",
                "- Экспериментировать с параметрами\n",
                "- Использовать другие модели (medium, large, melody)\n",
                "\n",
                "### Полезные ссылки\n",
                "- [Документация MusicGen](https://github.com/facebookresearch/audiocraft/blob/main/docs/MUSICGEN.md)\n",
                "- [Документация AudioGen](https://github.com/facebookresearch/audiocraft/blob/main/docs/AUDIOGEN.md)"
            ]
        }
    ],
    "metadata": {
        "accelerator": "GPU",
        "colab": {"gpuType": "T4", "provenance": []},
        "kernelspec": {"display_name": "Python 3", "name": "python3"},
        "language_info": {"name": "python"}
    },
    "nbformat": 4,
    "nbformat_minor": 0
}

# Notebook 2: Запуск локальной копии
local_copy = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Запуск локальной копии AudioCraft в Colab\n",
                "\n",
                "Этот notebook для работы с вашей локальной копией проекта.\n",
                "\n",
                "## Варианты загрузки:\n",
                "1. Google Drive - автосинхронизация\n",
                "2. GitHub - версионный контроль  \n",
                "3. ZIP архив - быстро"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## Вариант 1: Google Drive"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "from google.colab import drive\n",
                "drive.mount('/content/drive')\n",
                "print('✓ Google Drive подключен')"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Укажите путь к вашей папке в Google Drive\n",
                "AUDIOCRAFT_PATH = '/content/drive/MyDrive/audiocraft'\n",
                "\n",
                "import os\n",
                "if os.path.exists(AUDIOCRAFT_PATH):\n",
                "    %cd {AUDIOCRAFT_PATH}\n",
                "    print(f'✓ Перешли в: {AUDIOCRAFT_PATH}')\n",
                "    !ls -la | head -20\n",
                "else:\n",
                "    print(f'❌ Папка не найдена: {AUDIOCRAFT_PATH}')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## Вариант 2: GitHub"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# Замените на URL вашего репозитория\n",
                "GITHUB_REPO = 'https://github.com/YOUR_USERNAME/audiocraft.git'\n",
                "\n",
                "import os\n",
                "if not os.path.exists('/content/audiocraft'):\n",
                "    !git clone {GITHUB_REPO}\n",
                "    print('✓ Репозиторий клонирован')\n",
                "else:\n",
                "    print('✓ Репозиторий уже существует')\n",
                "\n",
                "%cd /content/audiocraft\n",
                "\n",
                "if os.path.exists('setup.py'):\n",
                "    print('✓ setup.py найден')\n",
                "else:\n",
                "    print('⚠️ setup.py не найден - проверьте путь')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## Вариант 3: ZIP архив"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "from google.colab import files\n",
                "import os\n",
                "\n",
                "print('Выберите файл audiocraft.zip...')\n",
                "uploaded = files.upload()\n",
                "\n",
                "if 'audiocraft.zip' in uploaded:\n",
                "    !unzip -q audiocraft.zip -d /content/\n",
                "    %cd /content/audiocraft\n",
                "    \n",
                "    if os.path.exists('setup.py'):\n",
                "        print('✓ Архив распакован и setup.py найден')\n",
                "    else:\n",
                "        print('⚠️ setup.py не найден - проверьте структуру архива')\n",
                "        !ls -la"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## Установка зависимостей"]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "⚠️ **О предупреждениях numpy:** Вы увидите конфликты зависимостей - это нормально для Colab. AudioCraft требует numpy<2.0, некоторые предустановленные пакеты - numpy>=2.0. Конфликтующие пакеты не используются AudioCraft."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import os\n",
                "print(f'Текущая директория: {os.getcwd()}')\n",
                "\n",
                "if not os.path.exists('setup.py'):\n",
                "    print('❌ setup.py не найден!')\n",
                "    print('Убедитесь что вы загрузили код правильно')\n",
                "    print('Содержимое текущей директории:')\n",
                "    !ls -la\n",
                "else:\n",
                "    !apt-get update -qq\n",
                "    !apt-get install -y -qq ffmpeg\n",
                "    !apt-get install -y -qq libavformat-dev libavcodec-dev libavdevice-dev libavutil-dev libswscale-dev libavresample-dev\n",
                "    \n",
                "    !pip install -q --upgrade pip setuptools wheel\n",
                "    !pip install -q 'numpy<2.0' 'transformers>=4.35.0' 'gradio>=4.0.0' 'hydra-core>=1.3'\n",
                "    \n",
                "    # Установка av отдельно\n",
                "    !pip install -q av\n",
                "    \n",
                "    # Установка AudioCraft\n",
                "    !pip install -q -e .\n",
                "    \n",
                "    print('✓ Установка завершена')\n",
                "    print('✓ Предупреждения о numpy можно игнорировать')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## Проверка"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import audiocraft\n",
                "from audiocraft.models import MusicGen\n",
                "print(f'✓ AudioCraft {audiocraft.__version__} готов!')"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## Тест генерации"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "from audiocraft.models import MusicGen\n",
                "from IPython.display import Audio\n",
                "\n",
                "model = MusicGen.get_pretrained('facebook/musicgen-small')\n",
                "model.set_generation_params(duration=5)\n",
                "wav = model.generate(['happy electronic music'])\n",
                "display(Audio(wav[0].cpu().numpy(), rate=model.sample_rate))"
            ]
        }
    ],
    "metadata": {
        "accelerator": "GPU",
        "colab": {"gpuType": "T4", "provenance": []},
        "kernelspec": {"display_name": "Python 3", "name": "python3"},
        "language_info": {"name": "python"}
    },
    "nbformat": 4,
    "nbformat_minor": 0
}

# Сохраняем notebooks
print("Создание notebook файлов...")

with open('colab_setup.ipynb', 'w', encoding='utf-8') as f:
    json.dump(colab_simple, f, indent=1, ensure_ascii=False)
print("✓ colab_setup.ipynb")

with open('run_local_copy_in_colab.ipynb', 'w', encoding='utf-8') as f:
    json.dump(local_copy, f, indent=1, ensure_ascii=False)
print("✓ run_local_copy_in_colab.ipynb")

print("\n✅ Notebooks созданы успешно!")
print("\nПроверка валидности JSON...")

# Проверяем валидность
import subprocess
for nb in ['colab_setup.ipynb', 'run_local_copy_in_colab.ipynb']:
    result = subprocess.run(['python3', '-m', 'json.tool', nb], 
                          capture_output=True)
    if result.returncode == 0:
        print(f"  ✓ {nb} - OK")
    else:
        print(f"  ✗ {nb} - ERROR")
