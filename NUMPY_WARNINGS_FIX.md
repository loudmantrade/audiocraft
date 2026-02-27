# ⚠️ О предупреждениях numpy в Google Colab

## Проблема
После установки зависимостей (шаг 4) вы увидите **красные сообщения об ошибках**:

```
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. 
This behaviour is the source of the following dependency conflicts.
cupy-cuda12x 14.0.1 requires numpy<2.6,>=2.0, but you have numpy 1.26.4 which is incompatible.
tobler 0.13.0 requires numpy>=2.0, but you have numpy 1.26.4 which is incompatible.
opencv-python 4.13.0.92 requires numpy>=2; python_version >= "3.9", but you have numpy 1.26.4 which is incompatible.
jax 0.7.2 requires numpy>=2.0, but you have numpy 1.26.4 which is incompatible.
... и другие
```

## ✅ Это НОРМАЛЬНО и БЕЗОПАСНО!

### Почему это происходит?

1. **AudioCraft требует numpy < 2.0** (версия 1.x)
   - PyTorch, многие ML библиотеки работают только с numpy 1.x
   - AudioCraft не совместим с numpy 2.0

2. **Google Colab предустанавливает пакеты с numpy >= 2.0**
   - cupy-cuda12x (CUDA ускорение для numpy)
   - opencv (компьютерное зрение)  
   - jax/jaxlib (альтернативный ML фреймворк)
   - tobler, xarray-einstats, rasterio (геопространственные/научные пакеты)
   - shap, pytensor (другие ML инструменты)

3. **Эти пакеты НЕ используются AudioCraft**
   - AudioCraft использует только: torch, torchaudio, transformers, encodec
   - Конфликтующие пакеты можно игнорировать

### Что важно проверить?

После установки запустите проверку:

```python
import numpy as np
import torch
import audiocraft
from audiocraft.models import MusicGen

print(f'NumPy: {np.__version__}')  # Должно быть 1.x (например 1.26.4)
print(f'PyTorch: {torch.__version__}')
print(f'AudioCraft: {audiocraft.__version__}')
print(f'CUDA: {torch.cuda.is_available()}')

# Если все импортируется без ошибок - всё работает!
print('✅ Всё в порядке!')
```

### Если есть проблемы с импортом

Только ЕСЛИ вы видите ошибки при импорте audiocraft или torch (не предупреждения pip, а реальные ошибки ImportError):

```python
# Переустановите numpy
!pip install --force-reinstall 'numpy<2.0'

# Переустановите pytorch
!pip install --force-reinstall torch torchaudio

# Переустановите audiocraft
%cd /content/audiocraft
!pip install -e . --no-deps
```

## Можно ли избавиться от предупреждений?

Технически да, но **не рекомендуется**:

```python
# НЕ ДЕЛАЙТЕ ТАК (может сломать другие компоненты Colab):
!pip uninstall -y cupy-cuda12x jax jaxlib opencv-python
```

Это:
- Не решит проблему полностью (останутся другие пакеты)
- Может сломать встроенные функции Colab
- Не нужно, так как AudioCraft работает и так

## Резюме

| Вопрос | Ответ |
|--------|-------|
| ❓ Это опасно? | ❌ Нет, совершенно безопасно |
| ❓ AudioCraft будет работать? | ✅ Да, без проблем |
| ❓ Нужно что-то исправлять? | ❌ Нет, продолжайте работу |
| ❓ Можно игнорировать? | ✅ Да, игнорируйте предупреждения |
| ❓ Когда беспокоиться? | ⚠️ Только если есть ImportError при импорте audiocraft |

---

## 🔧 Другие возможные проблемы

### Ошибка сборки пакета `av`

Если видите:
```
ERROR: Failed to build 'av' when getting requirements to build wheel
× Getting requirements to build wheel did not run successfully.
```

**Причина:** Пакет `av` (Python bindings для FFmpeg) требует dev-библиотек для компиляции.

**Решение:** ✅ **Исправлено в обновленных notebooks!**

Обновленные notebooks автоматически устанавливают необходимые библиотеки.

Если используете старую версию notebook или проблема осталась:
```python
# Установите FFmpeg dev-библиотеки
!apt-get install -y libavformat-dev libavcodec-dev libavdevice-dev \
                     libavutil-dev libswscale-dev libavresample-dev

# Затем установите av отдельно
!pip install av

# И затем AudioCraft
!pip install -e .
```

---

### Ошибка: setup.py не найден

Если видите:
```
ERROR: file:///content/audiocraft/audiocraft does not appear to be a Python project: 
neither 'setup.py' nor 'pyproject.toml' found.
```

**Причина:** Команда `%cd audiocraft` не сработала или вы находитесь в неправильной директории.

**Решение:** ✅ **Исправлено в обновленных notebooks!**

Обновленные notebooks используют абсолютные пути и проверяют наличие setup.py.

Если используете старую версию или проблема осталась:
```python
# Проверьте текущую директорию
import os
print(f'Текущая директория: {os.getcwd()}')
!ls -la setup.py

# Если setup.py не найден, перейдите в правильную папку
%cd /content/audiocraft

# Проверьте снова
!ls -la setup.py

# Теперь установите
!pip install -e .
```

**Важно:** Команда `%cd` в Colab иногда не сохраняет состояние между ячейками. Используйте абсолютные пути `/content/audiocraft`.

---

## ✅ Что делать дальше?

**Просто продолжайте работу!** Переходите к следующим шагам:
- Шаг 5: Проверка установки
- Шаг 6: Тестовая генерация музыки

Если все импорты работают - всё отлично! 🎉

---

**Тестировано:** Google Colab (Python 3.12, T4 GPU)  
**Статус:** Работает корректно несмотря на предупреждения  
**Дата:** 27 февраля 2026
