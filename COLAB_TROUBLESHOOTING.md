# 🔧 Быстрое решение проблем в Google Colab

## ❌ Ошибка: setup.py не найден

```
ERROR: file:///content/audiocraft/audiocraft does not appear to be a Python project: 
neither 'setup.py' nor 'pyproject.toml' found.
```

### ✅ Решение

**В текущей сессии Colab:**

Добавьте и запустите эту ячейку **перед** установкой AudioCraft:

```python
import os

# Переход в правильную директорию
%cd /content/audiocraft

# Проверка
print(f'Текущая директория: {os.getcwd()}')

if os.path.exists('setup.py'):
    print('✓ setup.py найден, можно продолжать установку')
    !ls -la setup.py
else:
    print('❌ setup.py не найден!')
    print('Содержимое директории:')
    !pwd
    !ls -la
```

Затем продолжите установку.

---

## ❌ Ошибка: Failed to build 'av'

```
ERROR: Failed to build 'av' when getting requirements to build wheel
```

### ✅ Решение

**Перед установкой AudioCraft** запустите:

```python
# Установка FFmpeg dev-библиотек
!apt-get update -qq
!apt-get install -y -qq libavformat-dev libavcodec-dev libavdevice-dev \
                         libavutil-dev libswscale-dev libavresample-dev

# Установка av
!pip install av

print('✓ av установлен')
```

Затем продолжите с установкой AudioCraft.

---

## ⚠️ Предупреждения numpy (не ошибки!)

```
ERROR: cupy-cuda12x requires numpy>=2.0, but you have numpy 1.26.4
ERROR: jax requires numpy>=2.0, but you have numpy 1.26.4
```

### ✅ Решение

**Ничего не делайте** - это НОРМАЛЬНО! ✅

- Эти предупреждения можно игнорировать
- AudioCraft работает с numpy 1.x (правильно)
- Конфликтующие пакеты не используются

**Просто продолжайте к следующему шагу!**

---

## 🔄 Универсальное решение: Перезапуск

Если столкнулись с проблемами:

1. **В Colab:**
   - Runtime → Disconnect and delete runtime
   - Runtime → Run all

2. **Используйте обновленный notebook:**
   - Загрузите свежую версию `colab_setup.ipynb`
   - Все проблемы исправлены

---

## 📋 Правильная последовательность установки

```python
# 1. FFmpeg и dev-библиотеки
!apt-get update -qq
!apt-get install -y -qq ffmpeg libavformat-dev libavcodec-dev \
    libavdevice-dev libavutil-dev libswscale-dev libavresample-dev

# 2. Клонирование (если нужно)
%cd /content
!git clone https://github.com/facebookresearch/audiocraft.git
%cd /content/audiocraft

# 3. Проверка
import os
print(f'Директория: {os.getcwd()}')
assert os.path.exists('setup.py'), 'setup.py не найден!'

# 4. Python зависимости
!pip install -q --upgrade pip setuptools wheel
!pip install -q 'numpy<2.0' 'transformers>=4.35.0' 'gradio>=4.0.0' 'hydra-core>=1.3'

# 5. av (отдельно)
!pip install -q av

# 6. AudioCraft
!pip install -q -e .

# 7. Проверка
import audiocraft
print(f'✓ AudioCraft {audiocraft.__version__} установлен!')
```

---

## 💡 Советы

1. **Всегда используйте абсолютные пути:** `/content/audiocraft` вместо относительных
2. **Проверяйте текущую директорию:** `!pwd` и `!ls setup.py`
3. **Используйте обновленные notebooks** - все исправления уже включены
4. **Не бойтесь предупреждений numpy** - они безопасны

---

## 📚 Полная документация

- [NUMPY_WARNINGS_FIX.md](NUMPY_WARNINGS_FIX.md) - Подробно о numpy
- [README_COLAB.md](README_COLAB.md) - Главная инструкция
- [HOW_TO_RUN_IN_COLAB.md](HOW_TO_RUN_IN_COLAB.md) - Полное руководство

---

**Обновлено:** 27 февраля 2026  
**Статус:** ✅ Все проблемы решены в обновленных notebooks
