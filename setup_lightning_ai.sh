#!/bin/bash
# AudioCraft Setup for Lightning.ai
# Installation script with Python 3.9 setup

set -e  # Exit on error

echo "=========================================="
echo "AudioCraft Setup for Lightning.ai"
echo "=========================================="

# Check current Python version
echo -e "\n[1/10] Checking current Python version..."
python3 --version || python --version || true

# Install build dependencies for Python compilation
echo -e "\n[2/10] Installing build dependencies..."
sudo apt-get update -qq
sudo apt-get install -y -qq build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev curl \
    libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev \
    libffi-dev liblzma-dev git

# Install Python 3.9 using pyenv
echo -e "\n[3/10] Setting up Python 3.9..."

# Setup pyenv environment variables
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"

if ! command -v pyenv &> /dev/null; then
    echo "Installing pyenv..."
    curl https://pyenv.run | bash
    
    # Add pyenv to bashrc for persistence
    if ! grep -q "PYENV_ROOT" ~/.bashrc; then
        echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
        echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
        echo 'eval "$(pyenv init -)"' >> ~/.bashrc
        echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
    fi
else
    echo "pyenv already installed"
fi

# Initialize pyenv in current shell
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)" 2>/dev/null || true

# Install Python 3.9.18 (latest 3.9)
if ! pyenv versions | grep -q "3.9.18"; then
    echo "Installing Python 3.9.18..."
    pyenv install 3.9.18
else
    echo "Python 3.9.18 already installed"
fi

# Set Python 3.9 as global default temporarily for installation
pyenv global 3.9.18
echo "✓ Using Python $(python --version)"

# Set Python 3.9 as local version
pyenv local 3.9.18
echo "✓ Using Python $(python --version)"

# Check GPU availability
echo -e "\n[4/10] Checking GPU availability..."
if ! command -v nvidia-smi &> /dev/null; then
    echo "WARNING: nvidia-smi not found. GPU may not be available."
else
    nvidia-smi --query-gpu=name,memory.total --format=csv
    echo "✓ GPU detected"
fi

# Install system dependencies
echo -e "\n[5/10] Installing FFmpeg dependencies..."
sudo apt-get update -qq
sudo apt-get install -y -qq ffmpeg libavformat-dev libavcodec-dev libavdevice-dev libavutil-dev libswscale-dev || true

# Clone/update repository
AUDIOCRAFT_DIR="$HOME/audiocraft"
if [ -d "$AUDIOCRAFT_DIR" ]; then
    echo -e "\n[6/10] Updating existing AudioCraft repository..."
    cd "$AUDIOCRAFT_DIR"
    git fetch origin
    git checkout main
    git pull origin main
else
    echo -e "\n[6/10] Cloning AudioCraft repository (original Meta version)..."
    git clone https://github.com/facebookresearch/audiocraft.git "$AUDIOCRAFT_DIR"
    cd "$AUDIOCRAFT_DIR"
fi

# Set Python 3.9 as local version in this directory
pyenv local 3.9.18

# Verify we're using Python 3.9
echo -e "\n[7/10] Verifying Python 3.9..."
python --version
if ! python -c "import sys; exit(0 if sys.version_info[:2] == (3, 9) else 1)"; then
    echo "ERROR: Python 3.9 required but got $(python --version)"
    exit 1
fi

# Install PyTorch with CUDA support (for Python 3.9)
echo -e "\n[8/10] Installing PyTorch with CUDA support..."
pip install --upgrade pip
pip install torch==2.2.0 torchvision==0.17.0 torchaudio==2.2.0 --index-url https://download.pytorch.org/whl/cu118

# Verify PyTorch CUDA
echo -e "\nVerifying PyTorch CUDA support..."
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}'); print(f'CUDA version: {torch.version.cuda if torch.cuda.is_available() else \"N/A\"}'); print(f'GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"N/A\"}')"

# Install dependencies
echo -e "\n[9/10] Installing AudioCraft dependencies..."
pip install -U "audiocraft[dev]"

# Fix numpy compatibility (AudioCraft requires numpy<2)
pip install "numpy<2.0"

# Verify installation
echo -e "\n[10/10] Verifying installation..."
echo "=========================================="
echo "Verifying installation..."
echo "=========================================="
python -c "import audiocraft; print('✓ AudioCraft:', audiocraft.__version__)"
python -c "from audiocraft.models import MusicGen; print('✓ MusicGen available')"
python -c "import torch; print('✓ GPU ready:', torch.cuda.is_available())"

echo -e "\n=========================================="
echo "✓ Installation Complete!"
echo "=========================================="
echo ""
echo "Python version: $(python --version)"
echo "Installation directory: $AUDIOCRAFT_DIR"
echo ""
echo "Quick start:"
echo "  cd $AUDIOCRAFT_DIR  # (Python 3.9 auto-activates)"
echo "  python"
echo "  >>> from audiocraft.models import MusicGen"
echo "  >>> model = MusicGen.get_pretrained('facebook/musicgen-small')"
echo ""
echo "Or launch web interface:"
echo "  cd $AUDIOCRAFT_DIR"
echo "  python -m demos.musicgen_app --share"
echo ""
echo "To use Python 3.9 in all sessions, add to ~/.bashrc:"
echo "  export PYENV_ROOT=\"\$HOME/.pyenv\""
echo "  export PATH=\"\$PYENV_ROOT/bin:\$PATH\""
echo "  eval \"\$(pyenv init -)\""
echo ""
