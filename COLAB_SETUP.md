# Запуск AudioCraft в Google Colab с Python 3.12

## Проблема

Google Colab по умолчанию использует Python 3.12, в то время как AudioCraft был разработан для Python 3.9. Это может привести к проблемам совместимости с некоторыми зависимостями.

## Решения

### Вариант 1: Использование готового Colab Notebook (Рекомендуется)

1. Загрузите файл `colab_setup.ipynb` в Google Colab
2. Выполните все ячейки последовательно
3. Notebook автоматически:
   - Установит все зависимости
   - Решит проблемы совместимости
   - Предоставит примеры использования

**Прямая ссылка для загрузки в Colab:**
```
https://colab.research.google.com/github/[YOUR_REPO]/audiocraft/blob/main/colab_setup.ipynb
```

### Вариант 2: Ручная установка в Colab

#### Шаг 1: Установка системных зависимостей

```bash
!apt-get update -qq
!apt-get install -y -qq ffmpeg
```

#### Шаг 2: Клонирование репозитория

```python
!git clone https://github.com/facebookresearch/audiocraft.git
%cd audiocraft
```

#### Шаг 3: Обновление зависимостей для Python 3.12

```python
# Используем обновленный файл requirements
!cp requirements_py312.txt requirements.txt

# Или устанавливаем вручную с правильными версиями
!pip install torch>=2.1.0 torchaudio>=2.1.0
!pip install transformers>=4.35.0 gradio>=4.0.0
!pip install hydra-core>=1.3 flashy>=0.0.2
!pip install 'numpy<2.0'  # Важно: numpy 2.0 имеет breaking changes
```

#### Шаг 4: Установка AudioCraft

Используйте обновленный setup.py:

```bash
!pip install -e . -f requirements_py312.txt
```

Или с патчем:
```bash
!cp setup_py312.py setup.py
!pip install -e .
```

### Вариант 3: Использование предустановленного образа

В Colab можно использовать старую версию Python через pyenv (сложнее):

```python
# НЕ РЕКОМЕНДУЕТСЯ: требует перезапуска runtime
!apt-get install -y pyenv
!pyenv install 3.9.18
!pyenv global 3.9.18
# Требуется перезапуск Colab runtime
```

## Основные проблемы совместимости и решения

### 1. XFormers недоступен для Python 3.12

**Проблема:** `xformers` может не иметь колес (wheels) для Python 3.12

**Решение:**
```python
# В config.yaml или при запуске установите:
efficient_attention_backend: torch  # вместо xformers

# Или в коде:
model.set_custom_progress_callback(None)
# Используйте стандартный PyTorch attention
```

**В setup.py:**
```python
'xformers>=0.0.23; python_version<"3.12"',  # Условная установка
```

### 2. NumPy 2.0 breaking changes

**Проблема:** NumPy 2.0 изменил API, несовместимый с некоторыми пакетами

**Решение:**
```bash
pip install 'numpy<2.0'
```

### 3. Проблемы с `distutils` (удален в Python 3.12)

**Проблема:** `distutils` был удален из стандартной библиотеки

**Решение:** Используйте `setuptools`:
```bash
pip install setuptools wheel
```

Пакеты должны импортировать из setuptools:
```python
# Вместо:
from distutils.core import setup

# Используйте:
from setuptools import setup
```

### 4. Устаревшие версии Gradio

**Проблема:** Старые версии Gradio несовместимы с Python 3.12

**Решение:**
```bash
pip install 'gradio>=4.0.0'
```

### 5. Проблемы с Hydra

**Проблема:** Старые версии Hydra могут иметь проблемы с importlib

**Решение:**
```bash
pip install 'hydra-core>=1.3'
```

## Проверка установки

После установки выполните:

```python
import sys
import torch
import audiocraft

print(f"Python: {sys.version}")
print(f"PyTorch: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"AudioCraft: {audiocraft.__version__}")

# Тест импорта моделей
from audiocraft.models import MusicGen, AudioGen
print("✓ All models imported successfully")
```

## Быстрый старт (минимальный пример)

```python
from audiocraft.models import MusicGen
from IPython.display import Audio
import torch

# Загрузка модели
model = MusicGen.get_pretrained('facebook/musicgen-small')

# Генерация музыки
model.set_generation_params(duration=8)
descriptions = ["happy rock song with electric guitar"]
wav = model.generate(descriptions)

# Воспроизведение
display(Audio(wav[0].cpu().numpy(), rate=model.sample_rate))
```

## Рекомендации по использованию GPU в Colab

### Включение GPU

1. В меню: `Runtime` → `Change runtime type`
2. Выберите `T4 GPU` (бесплатно) или `A100/V100` (Colab Pro)
3. Нажмите `Save`

### Проверка доступности GPU

```python
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
```

### Оптимизация использования памяти

```python
# Используйте меньшую модель
model = MusicGen.get_pretrained('facebook/musicgen-small')  # 300M параметров

# Уменьшите batch size
model.set_generation_params(
    duration=8,  # меньше = быстрее
    top_k=250,
)

# Очистка памяти после генерации
import gc
gc.collect()
torch.cuda.empty_cache()
```

## Известные ограничения

1. **XFormers**: Может быть недоступен для Python 3.12, используйте standard PyTorch attention
2. **Память GPU**: Модели требуют значительной VRAM:
   - `musicgen-small`: ~4GB VRAM
   - `musicgen-medium`: ~8GB VRAM
   - `musicgen-large`: ~16GB VRAM
3. **Скорость**: Генерация может быть медленной на бесплатных GPU в Colab

## Отладка проблем

### Логирование

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Проверка версий зависимостей

```python
import pkg_resources
packages = ['torch', 'torchaudio', 'transformers', 'gradio', 'hydra-core', 'audiocraft']
for package in packages:
    try:
        version = pkg_resources.get_distribution(package).version
        print(f"{package}: {version}")
    except:
        print(f"{package}: NOT INSTALLED")
```

### Очистка и переустановка

```bash
# Полная очистка
!pip uninstall -y audiocraft
!rm -rf /content/audiocraft

# Переустановка
!git clone https://github.com/facebookresearch/audiocraft.git
%cd audiocraft
!pip install -e .
```

## Полезные ссылки

- [AudioCraft GitHub](https://github.com/facebookresearch/audiocraft)
- [AudioCraft Documentation](https://facebookresearch.github.io/audiocraft/)
- [MusicGen Demo на HuggingFace](https://huggingface.co/spaces/facebook/MusicGen)
- [Python 3.12 Release Notes](https://docs.python.org/3/whatsnew/3.12.html)

## Поддержка

Если у вас возникли проблемы:

1. Проверьте [Issues на GitHub](https://github.com/facebookresearch/audiocraft/issues)
2. Создайте новый issue с:
   - Версией Python (`sys.version`)
   - Версией PyTorch
   - Полным traceback ошибки
   - Версией Colab (если применимо)

## Вклад

Если вы нашли решение проблемы совместимости с Python 3.12, пожалуйста:
1. Создайте Pull Request в основной репозиторий
2. Обновите этот документ
3. Поделитесь в Issues

---

**Последнее обновление:** 27 февраля 2026  
**Тестировано с:** Python 3.12, PyTorch 2.1.0, Google Colab (T4 GPU)
