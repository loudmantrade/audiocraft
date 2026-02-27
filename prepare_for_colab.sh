#!/bin/bash
# Скрипт для подготовки AudioCraft к загрузке в Google Colab

set -e

echo "🚀 Подготовка AudioCraft для Google Colab"
echo "=========================================="
echo ""

# Цвета для вывода
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Получаем директорию проекта
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo -e "${BLUE}Текущая директория:${NC} $PROJECT_DIR"
echo ""

# Функция для вывода меню
show_menu() {
    echo "Выберите метод загрузки в Colab:"
    echo ""
    echo "1) 📁 Подготовить для Google Drive"
    echo "2) 🔀 Подготовить для GitHub"
    echo "3) 📦 Создать ZIP архив"
    echo "4) 🎯 Все вместе (Drive + GitHub + ZIP)"
    echo "5) ❌ Выход"
    echo ""
}

# Функция для Google Drive
prepare_for_drive() {
    echo -e "${BLUE}📁 Подготовка для Google Drive...${NC}"
    echo ""
    
    # Проверяем наличие Google Drive
    DRIVE_PATH="$HOME/Google Drive/My Drive"
    if [ ! -d "$DRIVE_PATH" ]; then
        DRIVE_PATH="$HOME/GoogleDrive"
    fi
    
    if [ -d "$DRIVE_PATH" ]; then
        echo -e "${GREEN}✓${NC} Google Drive найден: $DRIVE_PATH"
        echo ""
        echo "Копируем проект в Google Drive..."
        echo "(Это может занять несколько минут)"
        
        TARGET_DIR="$DRIVE_PATH/audiocraft"
        
        # Копируем с исключениями
        rsync -av --progress \
            --exclude='.git/' \
            --exclude='__pycache__/' \
            --exclude='*.pyc' \
            --exclude='*.pyo' \
            --exclude='*.log' \
            --exclude='checkpoints/' \
            --exclude='outputs/' \
            --exclude='.DS_Store' \
            "$PROJECT_DIR/" "$TARGET_DIR/"
        
        echo ""
        echo -e "${GREEN}✓ Проект скопирован в Google Drive${NC}"
        echo -e "${YELLOW}Путь:${NC} $TARGET_DIR"
        echo ""
        echo "📝 В Colab используйте путь:"
        echo "   /content/drive/MyDrive/audiocraft"
        echo ""
    else
        echo -e "${YELLOW}⚠️  Google Drive не найден${NC}"
        echo ""
        echo "Установите Google Drive Desktop:"
        echo "https://www.google.com/drive/download/"
        echo ""
        echo "Или скопируйте проект вручную:"
        echo "  cp -r $PROJECT_DIR ~/Google\ Drive/My\ Drive/"
        echo ""
    fi
}

# Функция для GitHub
prepare_for_github() {
    echo -e "${BLUE}🔀 Подготовка для GitHub...${NC}"
    echo ""
    
    # Проверяем git
    if ! command -v git &> /dev/null; then
        echo -e "${YELLOW}⚠️  Git не установлен${NC}"
        echo "Установите git: https://git-scm.com/downloads"
        return 1
    fi
    
    # Создаем .gitignore если его нет
    if [ ! -f .gitignore ]; then
        echo "Создаем .gitignore..."
        cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# PyTorch
*.pth
*.pt
checkpoints/
outputs/

# Logs
*.log
logs/

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Datasets
dataset/
data/
*.wav
*.mp3
*.flac
EOF
        echo -e "${GREEN}✓${NC} .gitignore создан"
    fi
    
    # Инициализируем git если нужно
    if [ ! -d .git ]; then
        echo "Инициализируем Git репозиторий..."
        git init
        git add .
        git commit -m "Initial commit from local copy"
        echo -e "${GREEN}✓${NC} Git репозиторий инициализирован"
        echo ""
    else
        echo -e "${GREEN}✓${NC} Git репозиторий уже существует"
        echo ""
    fi
    
    # Проверяем remote
    if git remote get-url origin &> /dev/null; then
        REMOTE_URL=$(git remote get-url origin)
        echo -e "Текущий remote: ${YELLOW}$REMOTE_URL${NC}"
        echo ""
    else
        echo "📝 Следующие шаги:"
        echo ""
        echo "1. Создайте репозиторий на GitHub:"
        echo "   https://github.com/new"
        echo ""
        echo "2. Добавьте remote и загрузите код:"
        echo "   git remote add origin https://github.com/YOUR_USERNAME/audiocraft.git"
        echo "   git branch -M main"
        echo "   git push -u origin main"
        echo ""
        echo "3. В Colab используйте:"
        echo "   !git clone https://github.com/YOUR_USERNAME/audiocraft.git"
        echo ""
    fi
    
    # Показываем статус
    echo "Git статус:"
    git status --short || true
    echo ""
}

# Функция для ZIP
prepare_zip() {
    echo -e "${BLUE}📦 Создание ZIP архива...${NC}"
    echo ""
    
    ZIP_FILE="audiocraft_for_colab.zip"
    
    echo "Архивируем проект (исключая ненужные файлы)..."
    
    # Удаляем старый архив если есть
    rm -f "$ZIP_FILE"
    
    # Создаем архив
    zip -r "$ZIP_FILE" . \
        -x '*.git*' \
        -x '*__pycache__*' \
        -x '*.pyc' \
        -x '*.pyo' \
        -x '*.log' \
        -x '*checkpoints*' \
        -x '*outputs*' \
        -x '*.DS_Store' \
        -x '*.wav' \
        -x '*.mp3' \
        -x "$ZIP_FILE" \
        > /dev/null
    
    SIZE=$(du -h "$ZIP_FILE" | cut -f1)
    
    echo -e "${GREEN}✓ Архив создан:${NC} $ZIP_FILE ($SIZE)"
    echo ""
    echo "📝 Как использовать:"
    echo ""
    echo "1. Загрузите $ZIP_FILE в Google Drive"
    echo ""
    echo "2. В Colab:"
    echo "   from google.colab import drive"
    echo "   drive.mount('/content/drive')"
    echo "   !unzip '/content/drive/MyDrive/$ZIP_FILE' -d /content/audiocraft/"
    echo ""
    echo "Или загрузите напрямую в Colab:"
    echo "   from google.colab import files"
    echo "   uploaded = files.upload()"
    echo "   !unzip audiocraft_for_colab.zip"
    echo ""
}

# Функция для создания краткой инструкции
create_quick_guide() {
    echo -e "${BLUE}📄 Создание краткой инструкции...${NC}"
    
    cat > COLAB_QUICK_START.txt << 'EOF'
=======================================================================
  AUDIOCRAFT В GOOGLE COLAB - БЫСТРЫЙ СТАРТ
=======================================================================

📋 ВАШ ПРОЕКТ ГОТОВ К ЗАГРУЗКЕ В COLAB!

Выберите один из методов:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1️⃣  GOOGLE DRIVE (Рекомендуется)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Проект скопирован в Google Drive.
Подождите завершения синхронизации.

В Google Colab:
  1. Откройте: run_local_copy_in_colab.ipynb
  2. Выполните секцию "Вариант 1: Через Google Drive"
  3. Путь: /content/drive/MyDrive/audiocraft

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2️⃣  GITHUB (Для версионного контроля)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Создайте репозиторий: https://github.com/new

2. Загрузите код:
   git remote add origin https://github.com/YOUR_USERNAME/audiocraft.git
   git push -u origin main

3. В Colab:
   !git clone https://github.com/YOUR_USERNAME/audiocraft.git
   %cd audiocraft

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3️⃣  ZIP АРХИВ (Быстро и просто)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Файл: audiocraft_for_colab.zip создан

1. Загрузите ZIP в Google Drive

2. В Colab:
   from google.colab import drive
   drive.mount('/content/drive')
   !unzip '/content/drive/MyDrive/audiocraft_for_colab.zip' -d /content/
   %cd /content/audiocraft

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚡ БЫСТРАЯ УСТАНОВКА В COLAB
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

После загрузки кода запустите:

  # Системные зависимости
  !apt-get install -y ffmpeg

  # Python пакеты
  !pip install -q --upgrade pip setuptools wheel
  !pip install -q 'numpy<2.0' 'transformers>=4.35.0' 'gradio>=4.0.0'

  # Установка AudioCraft
  !pip install -q -e .

  # Проверка
  import audiocraft
  print(f"✓ Ready! Version: {audiocraft.__version__}")

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎵 ТЕСТ ГЕНЕРАЦИИ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  from audiocraft.models import MusicGen
  from IPython.display import Audio

  model = MusicGen.get_pretrained('facebook/musicgen-small')
  model.set_generation_params(duration=8)
  wav = model.generate(["happy rock music"])
  display(Audio(wav[0].cpu().numpy(), rate=model.sample_rate))

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 ПОЛНАЯ ДОКУМЕНТАЦИЯ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  • HOW_TO_RUN_IN_COLAB.md      - Подробное руководство
  • run_local_copy_in_colab.ipynb - Готовый notebook
  • COLAB_SETUP.md              - Решение проблем
  • QUICKSTART_COLAB.md         - Краткий старт

=======================================================================
🚀 Готово! Откройте Colab и начинайте работать!
   https://colab.research.google.com/
=======================================================================
EOF
    
    echo -e "${GREEN}✓${NC} Создан файл: COLAB_QUICK_START.txt"
}

# Главное меню
main() {
    while true; do
        show_menu
        read -p "Ваш выбор (1-5): " choice
        echo ""
        
        case $choice in
            1)
                prepare_for_drive
                create_quick_guide
                read -p "Нажмите Enter для продолжения..."
                clear
                ;;
            2)
                prepare_for_github
                create_quick_guide
                read -p "Нажмите Enter для продолжения..."
                clear
                ;;
            3)
                prepare_zip
                create_quick_guide
                read -p "Нажмите Enter для продолжения..."
                clear
                ;;
            4)
                prepare_for_drive
                echo ""
                prepare_for_github
                echo ""
                prepare_zip
                echo ""
                create_quick_guide
                echo ""
                echo -e "${GREEN}✅ Все готово!${NC}"
                echo ""
                cat COLAB_QUICK_START.txt
                echo ""
                read -p "Нажмите Enter для завершения..."
                break
                ;;
            5)
                echo "Выход..."
                exit 0
                ;;
            *)
                echo -e "${YELLOW}Неверный выбор. Попробуйте снова.${NC}"
                sleep 2
                clear
                ;;
        esac
    done
}

# Запуск
clear
main
