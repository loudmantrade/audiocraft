#!/bin/bash
# AudioCraft Setup for Lightning.ai
# Installation script with Python 3.9 setup

set -e  # Exit on error

echo "=========================================="
echo "AudioCraft Setup for Lightning.ai"
echo "=========================================="

# Check current Python version
echo -e "\n[1/9] Checking current Python version..."
python --version || true

# Install Python 3.9 using pyenv
echo -e "\n[2/9] Setting up Python 3.9..."
if ! command -v pyenv &> /dev/null; then
    echo "Installing pyenv..."
    curl https://pyenv.run | bash
    
    # Add pyenv to PATH
    export PYENV_ROOT="$HOME/.pyenv"
    export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init -)"
    eval "$(pyenv virtualenv-init -)"
    
    # Add to bashrc for persistence
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
    echo 'eval "$(pyenv init -)"' >> ~/.bashrc
    echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
else
    echo "pyenv already installed"
    export PYENV_ROOT="$HOME/.pyenv"
    export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init -)"
    eval "$(pyenv virtualenv-init -)"
fi

# Install Python 3.9.18 (latest 3.9)
if ! pyenv versions | grep -q "3.9.18"; then
    echo "Installing Python 3.9.18..."
    pyenv install 3.9.18
else
    echo "Python 3.9.18 already installed"
fi

# Set Python 3.9 as local version
pyenv local 3.9.18
echo "✓ Using Python $(python --version)"

# Set Python 3.9 as local version
pyenv local 3.9.18
echo "✓ Using Python $(python --version)"

# Check GPU availability
echo -e "\n[3/9] Checking GPU availability..."
if ! command -v nvidia-smi &> /dev/null; then
    echo "WARNING: nvidia-smi not found. GPU may not be available."
else
    nvidia-smi --query-gpu=name,memory.total --format=csv
    echo "✓ GPU detected"
fi

# Install system dependencies
echo -e "\n[4/9] Installing FFmpeg dependencies..."
sudo apt-get update -qq
sudo apt-get install -y -qq ffmpeg libavformat-dev libavcodec-dev libavdevice-dev libavutil-dev libswscale-dev || true

# Clone/update repository
AUDIOCRAFT_DIR="$HOME/audiocraft"
if [ -d "$AUDIOCRAFT_DIR" ]; then
    echo -e "\n[5/9] Updating existing AudioCraft repository..."
    cd "$AUDIOCRAFT_DIR"
    git fetch origin
    git checkout main
    git pull origin main
else
    echo -e "\n[5/9] Cloning AudioCraft repository (original Meta version)..."
    git clone https://github.com/facebookresearch/audiocraft.git "$AUDIOCRAFT_DIR"
    cd "$AUDIOCRAFT_DIR"
fi

# Verify we're using Python 3.9
echo -e "\n[6/9] Verifying Python 3.9..."
python --version
if ! python -c "import sys; exit(0 if sys.version_info[:2] == (3, 9) else 1)"; then
    echo "ERROR: Python 3.9 required but got $(python --version)"
    exit 1
fi

# Install PyTorch with CUDA support (for Python 3.9)
echo -e "\n[7/9] Installing PyTorch with CUDA support..."
pip install --upgrade pip
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Verify PyTorch CUDA
echo -e "\nVerifying PyTorch CUDA support..."
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}'); print(f'CUDA version: {torch.version.cuda if torch.cuda.is_available() else \"N/A\"}'); print(f'GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"N/A\"}')"

# Install dependencies
echo -e "\n[8/9] Installing AudioCraft dependencies..."
pip install -U audiocraft  # Install from PyPI for stable version

# Or install from source (editable mode)
# pip install -e .

# Verify installation
echo -e "\n[9/9] Verifying installation..."
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
echo "  python"
echo "  >>> from audiocraft.models import MusicGen"
echo "  >>> model = MusicGen.get_pretrained('facebook/musicgen-small')"
echo ""
echo "Or launch web interface:"
echo "  cd $AUDIOCRAFT_DIR"
echo "  python -m demos.musicgen_app --share"
echo ""
echo "To use Python 3.9 in new sessions:"
echo "  cd $AUDIOCRAFT_DIR  # (will auto-activate Python 3.9)"
echo ""
