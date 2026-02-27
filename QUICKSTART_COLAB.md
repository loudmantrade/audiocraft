# Быстрый старт: AudioCraft в Google Colab

## 🚀 Самый быстрый способ

1. **Откройте Colab notebook:**
   - Загрузите [`colab_setup.ipynb`](colab_setup.ipynb) в Google Colab
   - Или используйте прямую ссылку
   
2. **Запустите все ячейки** (Runtime → Run all)

3. **Готово!** Можете генерировать музыку 🎵

## 📋 Что делает notebook

- ✅ Автоматически устанавливает все зависимости
- ✅ Решает проблемы совместимости с Python 3.12
- ✅ Предоставляет готовые примеры
- ✅ Запускает веб-интерфейс Gradio

## 🔧 Если хотите ручную установку

### Минимальная установка (5 команд)

```bash
# 1. Установите ffmpeg
!apt-get install -y ffmpeg

# 2. Клонируйте репозиторий
!git clone https://github.com/facebookresearch/audiocraft.git
%cd audiocraft

# 3. Используйте совместимые зависимости
!pip install -e . --use-pep517

# 4. Установите обновленные пакеты для Python 3.12
!pip install 'numpy<2.0' 'transformers>=4.35.0' 'gradio>=4.0.0' 'hydra-core>=1.3'

# 5. Тест
from audiocraft.models import MusicGen
model = MusicGen.get_pretrained('facebook/musicgen-small')
print("✓ Ready!")
```

## 🎵 Быстрый пример генерации

```python
from audiocraft.models import MusicGen
from IPython.display import Audio

# Загрузка модели
model = MusicGen.get_pretrained('facebook/musicgen-small')
model.set_generation_params(duration=8)

# Генерация
wav = model.generate(["happy rock music with electric guitar"])

# Воспроизведение
display(Audio(wav[0].cpu().numpy(), rate=model.sample_rate))
```

## ⚡ Доступные модели

### MusicGen (музыка)
- `facebook/musicgen-small` - 300M параметров, быстро
- `facebook/musicgen-medium` - 1.5B параметров, качественно  
- `facebook/musicgen-large` - 3.3B параметров, очень качественно
- `facebook/musicgen-melody` - с поддержкой мелодии

### AudioGen (звуки)
- `facebook/audiogen-medium` - звуковые эффекты

## 🐛 Проблемы?

### XFormers не устанавливается
```python
# Используйте стандартный attention
# В config или коде ничего не меняйте - будет работать автоматически
```

### Ошибка памяти
```python
# Используйте малую модель
model = MusicGen.get_pretrained('facebook/musicgen-small')

# Уменьшите длину
model.set_generation_params(duration=5)  # вместо 30

# Очистите память
import gc
gc.collect()
torch.cuda.empty_cache()
```

### NumPy ошибки
```bash
!pip install 'numpy<2.0' --force-reinstall
```

## 📚 Полная документация

- [COLAB_SETUP.md](COLAB_SETUP.md) - подробное руководство
- [README.md](README.md) - основная документация
- [Примеры](demos/) - Jupyter notebooks с примерами

## 🆘 Нужна помощь?

1. Проверьте [Issues на GitHub](https://github.com/facebookresearch/audiocraft/issues)
2. Запустите скрипт диагностики:
   ```bash
   python check_py312_compatibility.py
   ```
3. Создайте новый Issue с полной информацией об ошибке

---

**Время установки:** ~5-10 минут  
**Требования:** GPU (T4 или лучше в Colab)  
**Python:** 3.8+ (включая 3.12 ✓)
