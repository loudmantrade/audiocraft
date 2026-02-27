# AudioCraft на Lightning.ai - Быстрый старт

## 1. Подключитесь к Lightning.ai

```bash
ssh s_01kjgghfgzrex7pbyr5kffsx2j@ssh.lightning.ai
```

## 2. Запустите установку (одна команда)

```bash
curl -O https://raw.githubusercontent.com/loudmantrade/audiocraft/colab-python312-support/setup_lightning_ai.sh && chmod +x setup_lightning_ai.sh && ./setup_lightning_ai.sh
```

⏱️ Установка займет ~10-15 минут (включая компиляцию Python 3.9)

## 3. Протестируйте

После установки:

```bash
cd ~/audiocraft
python test_lightning.py
```

## 4. Генерируйте музыку

### Через Python:

```python
from audiocraft.models import MusicGen
import torchaudio

# Загрузить модель
model = MusicGen.get_pretrained('facebook/musicgen-small')

# Сгенерировать
model.set_generation_params(duration=10)
wav = model.generate(['веселая электронная танцевальная музыка'])

# Сохранить
torchaudio.save('music.wav', wav[0].cpu(), model.sample_rate)
```

### Через веб-интерфейс:

```bash
cd ~/audiocraft
python -m demos.musicgen_app --share
```

Откроется Gradio интерфейс с публичной ссылкой.

## Что устанавливается

- ✅ **Python 3.9.18** (через pyenv)
- ✅ **PyTorch с CUDA** (GPU ускорение)
- ✅ **AudioCraft** (официальная версия от Meta)
- ✅ **FFmpeg** (для работы с аудио)
- ✅ **Все зависимости** (xformers, transformers, etc.)

## Важно

### Использование Python 3.9 в новых сессиях:

При каждом новом подключении:
```bash
cd ~/audiocraft  # Автоматически активируется Python 3.9
```

Или глобально:
```bash
pyenv global 3.9.18
```

### Проверка версии:

```bash
python --version  # Должно быть: Python 3.9.18
```

## Доступные модели

| Модель | Размер | Качество | Скорость |
|--------|--------|----------|----------|
| `musicgen-small` | 300M | Хорошее | Быстро ⚡⚡⚡ |
| `musicgen-medium` | 1.5B | Отличное | Средне ⚡⚡ |
| `musicgen-large` | 3.3B | Лучшее | Медленно ⚡ |
| `audiogen-medium` | 1.5B | - | Звуковые эффекты |

## Примеры промптов

```python
descriptions = [
    'энергичная электронная танцевальная музыка с синтезаторами',
    'спокойная акустическая гитарная мелодия',
    'эпическая оркестровая музыка для фильма',
    'lo-fi hip hop для учебы',
    'агрессивный рок с электрогитарами и барабанами'
]

model.set_generation_params(duration=30)
wav = model.generate(descriptions)
```

## Проблемы?

### GPU не определяется:
```bash
nvidia-smi
python -c "import torch; print(torch.cuda.is_available())"
```

### Python 3.9 не активен:
```bash
cd ~/audiocraft
python --version
```

### Переустановка:
```bash
cd ~
rm -rf audiocraft .pyenv
./setup_lightning_ai.sh  # Запустить заново
```

## Полная документация

См. [LIGHTNING_AI.md](LIGHTNING_AI.md) для подробностей и troubleshooting.
