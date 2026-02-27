#!/bin/bash
# AudioCraft Setup for Lightning.ai
# Quick installation script for Python 3.12 environment

set -e  # Exit on error

echo "=========================================="
echo "AudioCraft Setup for Lightning.ai"
echo "=========================================="

# Check Python version
echo -e "\n[1/8] Checking Python version..."
python --version
if ! python -c "import sys; exit(0 if sys.version_info >= (3, 8) and sys.version_info < (3, 13) else 1)"; then
    echo "ERROR: Python 3.8-3.12 required"
    exit 1
fi

# Check GPU availability
echo -e "\n[2/8] Checking GPU availability..."
if ! command -v nvidia-smi &> /dev/null; then
    echo "WARNING: nvidia-smi not found. GPU may not be available."
else
    nvidia-smi --query-gpu=name,memory.total --format=csv
    echo "✓ GPU detected"
fi

# Install system dependencies
echo -e "\n[3/8] Installing FFmpeg dependencies..."
sudo apt-get update -qq
sudo apt-get install -y -qq ffmpeg libavformat-dev libavcodec-dev libavdevice-dev libavutil-dev libswscale-dev || true

# Clone/update repository
AUDIOCRAFT_DIR="$HOME/audiocraft"
if [ -d "$AUDIOCRAFT_DIR" ]; then
    echo -e "\n[4/8] Updating existing AudioCraft repository..."
    cd "$AUDIOCRAFT_DIR"
    git fetch origin
    git checkout colab-python312-support
    git pull origin colab-python312-support
else
    echo -e "\n[4/8] Cloning AudioCraft repository..."
    git clone -b colab-python312-support https://github.com/loudmantrade/audiocraft.git "$AUDIOCRAFT_DIR"
    cd "$AUDIOCRAFT_DIR"
fi

# Copy Python 3.12 compatible setup
echo -e "\n[5/8] Setting up Python 3.12 compatible configuration..."
cp setup_py312.py setup.py
grep "REQUIRES_PYTHON" setup.py

# Install PyTorch with CUDA support
echo -e "\n[6/8] Installing PyTorch with CUDA 12.8..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128

# Verify PyTorch CUDA
echo -e "\nVerifying PyTorch CUDA support..."
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}'); print(f'CUDA version: {torch.version.cuda if torch.cuda.is_available() else \"N/A\"}'); print(f'GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"N/A\"}')"

# Install dependencies
echo -e "\n[7/8] Installing AudioCraft dependencies..."
pip install -q av einops transformers huggingface_hub sentencepiece num2words hydra-core omegaconf gradio julius encodec demucs torchmetrics librosa

# Install AudioCraft
echo -e "\n[8/8] Installing AudioCraft..."
pip install -e .

# Verify installation
echo -e "\n=========================================="
echo "Verifying installation..."
echo "=========================================="
python -c "import audiocraft; print('✓ AudioCraft:', audiocraft.__version__)"
python -c "from audiocraft.models import MusicGen; print('✓ MusicGen available')"
python -c "import torch; print('✓ GPU ready:', torch.cuda.is_available())"

echo -e "\n=========================================="
echo "✓ Installation Complete!"
echo "=========================================="
echo ""
echo "Quick start:"
echo "  cd $AUDIOCRAFT_DIR"
echo "  python demos/musicgen_app.py"
echo ""
echo "Or use Python:"
echo "  from audiocraft.models import MusicGen"
echo "  model = MusicGen.get_pretrained('facebook/musicgen-small')"
echo ""
