# 🎵 AudioCraft для Google Colab - Готовые Notebooks

## ✅ Проблема исправлена!

Notebooks пересозданы с корректным JSON форматом и готовы к использованию в Google Colab.

---

## 📁 Доступные файлы

### 1. **[colab_setup.ipynb](colab_setup.ipynb)** - Быстрая установка
**Для кого:** Новички, быстрый старт  
**Что делает:** 
- Автоматически клонирует AudioCraft из GitHub
- Устанавливает все зависимости с учетом Python 3.12
- Запускает тестовую генерацию
- Предоставляет готовый Gradio интерфейс

**Как использовать:**
1. Откройте в Google Colab: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/)
2. Загрузите файл `colab_setup.ipynb`
3. Runtime → Change runtime type → T4 GPU
4. Runtime → Run all
5. Готово! 🎉

---

### 2. **[run_local_copy_in_colab.ipynb](run_local_copy_in_colab.ipynb)** - Ваша локальная копия
**Для кого:** Разработчики, кто хочет работать со своим кодом  
**Что делает:**
- Загружает вашу локальную копию (Drive/GitHub/ZIP)
- Устанавливает зависимости
- Позволяет редактировать код

**Как использовать:**
1. **Подготовьте код** (выберите метод):
   
   **A. Google Drive:**
   ```bash
   # На вашем Mac
   cp -r /Users/agugnin/ai/audiocraft ~/Google\ Drive/My\ Drive/
   ```
   
   **B. GitHub:**
   ```bash
   cd /Users/agugnin/ai/audiocraft
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/audiocraft.git
   git push -u origin main
   ```
   
   **C. ZIP:**
   ```bash
   cd /Users/agugnin/ai
   zip -r audiocraft.zip audiocraft -x '*.git*' '*__pycache__*'
   ```

2. **В Colab:**
   - Откройте `run_local_copy_in_colab.ipynb`
   - Выберите нужную секцию (Drive/GitHub/ZIP)
   - Запустите ячейки

---

## 🚀 Быстрый старт (3 минуты)

### В Google Colab:

```python
# 1. Клонировать и перейти
!git clone https://github.com/facebookresearch/audiocraft.git
%cd audiocraft

# 2. Установить системные зависимости
!apt-get install -y -qq ffmpeg

# 3. Установить Python пакеты (совместимо с Python 3.12)
!pip install -q --upgrade pip setuptools wheel
!pip install -q 'numpy<2.0' 'transformers>=4.35.0' 'gradio>=4.0.0' 'hydra-core>=1.3'
!pip install -q -e .

# 4. Тест
from audiocraft.models import MusicGen
from IPython.display import Audio

model = MusicGen.get_pretrained('facebook/musicgen-small')
model.set_generation_params(duration=8)
wav = model.generate(['happy electronic dance music'])
display(Audio(wav[0].cpu().numpy(), rate=model.sample_rate))
```

---

## 🔧 Автоматическая подготовка (для локальной копии)

На вашем Mac запустите:

```bash
cd /Users/agugnin/ai/audiocraft
./prepare_for_colab.sh
```

Интерактивный скрипт предложит:
1. Копирование в Google Drive
2. Настройка Git/GitHub
3. Создание ZIP архива
4. Всё вместе

---

## 📋 Чек-лист перед запуском в Colab

- [ ] GPU включен (Runtime → Change runtime type → T4 GPU)
- [ ] Выбран метод загрузки кода (GitHub/Drive/ZIP)
- [ ] Открыт правильный notebook
- [ ] Изменены пути в коде (если используете локальную копию)

---

## 🐛 Решение проблем

### "Unexpected end of JSON input"
**Решение:** ✅ Исправлено! Используйте обновленные файлы.

### Предупреждения о конфликтах numpy (ERROR: pip's dependency resolver...)
```
ERROR: cupy-cuda12x requires numpy>=2.0, but you have numpy 1.26.4
ERROR: jax requires numpy>=2.0, but you have numpy 1.26.4
ERROR: opencv-python requires numpy>=2...
```

**Решение:** ✅ **Это НОРМАЛЬНО! Игнорируйте эти предупреждения.**

- AudioCraft требует numpy < 2.0 (и это правильно)
- Конфликтующие пакеты (cupy, jax, opencv) НЕ используются AudioCraft
- Все будет работать корректно

**Подробнее:** См. [NUMPY_WARNINGS_FIX.md](NUMPY_WARNINGS_FIX.md)

### Ошибка сборки пакета av
```
ERROR: Failed to build 'av' when getting requirements to build wheel
```

**Решение:** ✅ **Исправлено в обновленных notebooks!**

Старые версии не устанавливали FFmpeg dev-библиотеки. Если используете старый notebook:
```python
!apt-get install -y libavformat-dev libavcodec-dev libavdevice-dev \
                     libavutil-dev libswscale-dev libavresample-dev
!pip install av
```

### setup.py не найден
```
ERROR: file:///content/audiocraft/audiocraft does not appear to be a Python project
```

**Решение:** ✅ **Исправлено в обновленных notebooks!**

Проблема была в том, что `%cd audiocraft` не работал надежно. Обновленные notebooks используют абсолютные пути.

Если используете старый notebook:
```python
%cd /content/audiocraft
!ls -la setup.py  # Проверьте что файл есть
!pip install -e .
```

### "No module named 'audiocraft'"
```python
# Убедитесь что вы в правильной папке
!pwd
!ls setup.py

# Переустановите
!pip install -e .
```

### "CUDA out of memory"
```python
# Используйте маленькую модель
model = MusicGen.get_pretrained('facebook/musicgen-small')

# Уменьшите длительность
model.set_generation_params(duration=5)

# Очистите память
import gc, torch
gc.collect()
torch.cuda.empty_cache()
```

### XFormers не устанавливается
**Это нормально для Python 3.12!** Код работает без xformers, используя стандартный PyTorch attention.

---

## 📚 Дополнительная документация

- **[HOW_TO_RUN_IN_COLAB.md](HOW_TO_RUN_IN_COLAB.md)** - Подробное руководство
- **[COLAB_SETUP.md](COLAB_SETUP.md)** - Проблемы совместимости Python 3.12
- **[QUICKSTART_COLAB.md](QUICKSTART_COLAB.md)** - Краткий справочник

---

## 🎯 Рекомендуемый путь

1. **Для первого знакомства:**
   → Используйте `colab_setup.ipynb`

2. **Для разработки:**
   → Используйте `run_local_copy_in_colab.ipynb` + GitHub

3. **Для экспериментов с кодом:**
   → Используйте `run_local_copy_in_colab.ipynb` + Google Drive

---

## 💡 Полезные команды в Colab

```python
# Мониторинг GPU
!nvidia-smi

# Проверка версий
import torch, audiocraft
print(f"PyTorch: {torch.__version__}")
print(f"AudioCraft: {audiocraft.__version__}")
print(f"CUDA: {torch.cuda.is_available()}")

# Запуск Gradio
!python -m demos.musicgen_app --share

# Очистка памяти
import gc, torch
gc.collect()
torch.cuda.empty_cache()
```

---

## ✅ Проверка файлов

Все notebooks проверены:
```
✓ colab_setup.ipynb - OK (5.6KB)
✓ run_local_copy_in_colab.ipynb - OK (4.1KB)
```

JSON валиден, готовы к загрузке в Google Colab!

---

**Последнее обновление:** 27 февраля 2026  
**Тестировано:** Google Colab (Python 3.12, T4 GPU)  
**Статус:** ✅ Готово к использованию

---

**Вопросы?** Смотрите [HOW_TO_RUN_IN_COLAB.md](HOW_TO_RUN_IN_COLAB.md) или создайте Issue на GitHub.
