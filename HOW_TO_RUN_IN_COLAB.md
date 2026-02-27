# Как запустить вашу локальную копию AudioCraft в Google Colab

## 🎯 Быстрый выбор метода

| Метод | Сложность | Удобство | Синхронизация | Рекомендация |
|-------|-----------|----------|---------------|--------------|
| **Google Drive** | ⭐ | ⭐⭐⭐ | Автоматическая | ✅ **Лучший для начала** |
| **GitHub** | ⭐⭐ | ⭐⭐⭐ | Через git | ✅ **Лучший для разработки** |
| **ZIP архив** | ⭐ | ⭐ | Ручная | Для разового запуска |

---

## 📦 Метод 1: Google Drive (Рекомендуется для начала)

### На вашем компьютере:

1. **Установите Google Drive Desktop** (если еще не установлен)
   - Скачайте: https://www.google.com/drive/download/

2. **Скопируйте проект в Google Drive:**
   ```bash
   # Найдите папку Google Drive (обычно ~/Google Drive)
   cp -r /Users/agugnin/ai/audiocraft ~/Google\ Drive/My\ Drive/
   ```

3. **Дождитесь синхронизации** (значок облака в системном трее)

### В Google Colab:

1. **Откройте** `run_local_copy_in_colab.ipynb` в Google Colab
2. **Выполните секцию "Вариант 1: Через Google Drive"**
3. **Измените путь** `AUDIOCRAFT_PATH` на ваш путь в Drive
4. **Запустите установку**

### ✅ Преимущества:
- Автоматическая синхронизация изменений
- Не нужен Git
- Просто настроить

### ⚠️ Недостатки:
- Требует место в Google Drive (~500MB)
- Медленнее при первой загрузке

---

## 🔀 Метод 2: GitHub (Лучший для разработки)

### На вашем компьютере:

1. **Создайте Git репозиторий и загрузите код:**
   ```bash
   cd /Users/agugnin/ai/audiocraft
   
   # Инициализируем git (если еще не сделано)
   git init
   
   # Добавляем .gitignore
   cat << 'EOF' > .gitignore
   __pycache__/
   *.pyc
   *.pyo
   *.egg-info/
   dist/
   build/
   .DS_Store
   *.log
   checkpoints/
   outputs/
   EOF
   
   # Добавляем файлы
   git add .
   git commit -m "Initial commit from local copy"
   ```

2. **Создайте репозиторий на GitHub:**
   - Перейдите: https://github.com/new
   - Название: `audiocraft` (или другое)
   - Можно сделать приватным
   - НЕ добавляйте README/LICENSE (уже есть)

3. **Загрузите код:**
   ```bash
   # Замените YOUR_USERNAME на ваш GitHub username
   git remote add origin https://github.com/YOUR_USERNAME/audiocraft.git
   git branch -M main
   git push -u origin main
   ```

### В Google Colab:

1. **Откройте** `run_local_copy_in_colab.ipynb`
2. **Выполните секцию "Вариант 2: Через GitHub"**
3. **Измените** `GITHUB_REPO` на URL вашего репозитория
4. **Запустите установку**

### Для приватного репозитория:

Создайте Personal Access Token:
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token (classic)
3. Дайте права: `repo` (full control)
4. Копируйте токен

В Colab используйте:
```python
GITHUB_TOKEN = "ghp_ваш_токен_здесь"
GITHUB_USER = "ваш_username"
GITHUB_REPO = f"https://{GITHUB_TOKEN}@github.com/{GITHUB_USER}/audiocraft.git"
```

### ✅ Преимущества:
- Версионный контроль
- Легко отслеживать изменения
- Можно работать с разных машин
- Профессиональный подход

### После изменений в Colab:
```bash
!git config user.email "your@email.com"
!git config user.name "Your Name"
!git add .
!git commit -m "Changes from Colab"
!git push
```

---

## 📦 Метод 3: ZIP архив (Для разового запуска)

### На вашем компьютере:

```bash
cd /Users/agugnin/ai

# Создаем архив (исключаем ненужное)
zip -r audiocraft.zip audiocraft \
  -x '*.git*' \
  -x '*__pycache__*' \
  -x '*.pyc' \
  -x '*.log' \
  -x '*checkpoints*' \
  -x '*outputs*'

# Проверяем размер
ls -lh audiocraft.zip
```

### Вариант A: Через Google Drive

1. Загрузите `audiocraft.zip` в Google Drive
2. В Colab используйте секцию "Вариант 3: Через ZIP"

### Вариант B: Прямая загрузка в Colab

1. В Colab выполните:
   ```python
   from google.colab import files
   uploaded = files.upload()  # Выберите audiocraft.zip
   ```

---

## 🚀 После загрузки: Быстрый старт

После того как код загружен любым способом, запустите:

```python
# 1. Установка системных зависимостей
!apt-get update -qq && apt-get install -y -qq ffmpeg

# 2. Обновление pip
!pip install -q --upgrade pip setuptools wheel

# 3. Установка Python пакетов для Python 3.12
!pip install -q 'numpy<2.0' 'transformers>=4.35.0' 'gradio>=4.0.0' 'hydra-core>=1.3'

# 4. Установка AudioCraft в режиме разработки
!pip install -q -e .

# 5. Проверка
import audiocraft
from audiocraft.models import MusicGen
print(f"✓ AudioCraft {audiocraft.__version__} готов!")
```

---

## 🎵 Тестовая генерация

```python
from audiocraft.models import MusicGen
from IPython.display import Audio

# Загружаем модель
model = MusicGen.get_pretrained('facebook/musicgen-small')
model.set_generation_params(duration=8)

# Генерируем
wav = model.generate(["happy electronic dance music"])

# Слушаем
display(Audio(wav[0].cpu().numpy(), rate=model.sample_rate))
```

---

## 🔧 Работа с вашими изменениями

### Редактирование файлов в Colab:

1. **Через файловый браузер:**
   - Открыть панель Files слева
   - Двойной клик на файл
   - Редактировать
   - Ctrl+S для сохранения

2. **Через код:**
   ```python
   # Просмотр файла
   !cat audiocraft/models/musicgen.py | head -50
   
   # Редактирование через sed/awk (для продвинутых)
   # Или используйте графический редактор
   ```

3. **После изменений:**
   ```python
   # Переустановить без зависимостей (быстро)
   !pip install -e . --no-deps
   
   # Или перезапустить Python kernel:
   # Runtime → Restart runtime
   ```

---

## 💾 Сохранение изменений

### Google Drive:
- **Автоматически** синхронизируется
- Просто сохраните файл (Ctrl+S)

### GitHub:
```bash
!git add .
!git commit -m "Описание изменений"
!git push
```

### Скачать измененные файлы:
```python
from google.colab import files

# Скачать один файл
files.download('audiocraft/models/musicgen.py')

# Или создать архив
!zip -r changes.zip audiocraft/models/
files.download('changes.zip')
```

---

## 🐛 Частые проблемы и решения

### Проблема: "ModuleNotFoundError: No module named 'audiocraft'"

**Решение:**
```python
# Убедитесь что вы в правильной папке
import os
print(os.getcwd())

# Должны быть в папке audiocraft с файлом setup.py
!ls -la setup.py

# Переустановите
!pip install -e .
```

### Проблема: "CUDA out of memory"

**Решение:**
```python
# Используйте меньшую модель
model = MusicGen.get_pretrained('facebook/musicgen-small')

# Уменьшите длительность
model.set_generation_params(duration=5)

# Очистите память
import gc
import torch
gc.collect()
torch.cuda.empty_cache()
```

### Проблема: Изменения в коде не применяются

**Решение:**
```python
# Способ 1: Перезапустите Python kernel
# Runtime → Restart runtime → Run all

# Способ 2: Переустановите пакет
!pip install -e . --force-reinstall --no-deps

# Способ 3: Перезагрузите модули
import importlib
import audiocraft
importlib.reload(audiocraft)
```

---

## 📊 Мониторинг ресурсов

```python
# GPU
!nvidia-smi

# Память PyTorch
import torch
if torch.cuda.is_available():
    allocated = torch.cuda.memory_allocated() / 1e9
    reserved = torch.cuda.memory_reserved() / 1e9
    print(f"GPU Memory: {allocated:.2f} GB allocated, {reserved:.2f} GB reserved")

# Диск
!df -h /content

# RAM
!free -h
```

---

## 📝 Чек-лист для начала работы

- [ ] Выбрал метод загрузки (Drive/GitHub/ZIP)
- [ ] Загрузил код в Colab
- [ ] Установил ffmpeg
- [ ] Установил Python зависимости (включая numpy<2.0)
- [ ] Установил audiocraft (`pip install -e .`)
- [ ] Проверил импорт (`import audiocraft`)
- [ ] Запустил тестовую генерацию
- [ ] Включил GPU (Runtime → Change runtime type → T4 GPU)
- [ ] Сохранил notebook для будущего использования

---

## 🎓 Полезные ресурсы

- **Notebook для локальной копии:** `run_local_copy_in_colab.ipynb`
- **Полная документация:** `COLAB_SETUP.md`
- **Быстрый старт:** `QUICKSTART_COLAB.md`
- **Проверка совместимости:** `python check_py312_compatibility.py`

---

## 💡 Рекомендации

1. **Для экспериментов:** Используйте Google Drive (быстро настроить)
2. **Для разработки:** Используйте GitHub (версионный контроль)
3. **Включите GPU:** Runtime → Change runtime type → T4 GPU
4. **Сохраняйте checkpoint'ы:** Периодически коммитьте/синхронизируйте
5. **Используйте маленькую модель** для тестов: `musicgen-small`

---

**Готово! Теперь вы можете разрабатывать AudioCraft прямо в Google Colab! 🎉**
