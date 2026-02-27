# AudioCraft on Lightning.ai

Quick setup guide for running AudioCraft on Lightning.ai instances with Python 3.9 and GPU support.

## Quick Start

### 1. Connect to Lightning.ai

```bash
ssh s_01kjgghfgzrex7pbyr5kffsx2j@ssh.lightning.ai
```

### 2. Run Setup Script

The setup script will automatically:
- Install Python 3.9 using pyenv
- Install PyTorch with CUDA support
- Install AudioCraft from Meta's official repository
- Configure everything for GPU acceleration

```bash
# Download and run setup script
curl -O https://raw.githubusercontent.com/loudmantrade/audiocraft/colab-python312-support/setup_lightning_ai.sh
chmod +x setup_lightning_ai.sh
./setup_lightning_ai.sh
```

**Note:** Setup takes ~10-15 minutes (includes Python 3.9 compilation)

### 3. Generate Music

```python
from audiocraft.models import MusicGen
import torchaudio

# Load model
model = MusicGen.get_pretrained('facebook/musicgen-small')

# Generate
model.set_generation_params(duration=10)
wav = model.generate(['upbeat electronic dance music'])

# Save
torchaudio.save('output.wav', wav[0].cpu(), model.sample_rate)
```

## Why Python 3.9?

AudioCraft was developed and tested with Python 3.9. While newer versions may work, Python 3.9 ensures:
- ✅ Full compatibility with all dependencies
- ✅ Stable xformers support for faster generation
- ✅ No compatibility issues with Meta's pretrained models
- ✅ Tested and supported configuration

## Features

✅ **Python 3.9 via pyenv** - Automatic version management  
✅ **GPU Acceleration** - CUDA support configured  
✅ **xformers Support** - Faster transformer operations  
✅ **Original Meta Version** - Official stable release  

## Models Available

- `facebook/musicgen-small` - Fast, 300M parameters
- `facebook/musicgen-medium` - Balanced, 1.5B parameters  
- `facebook/musicgen-large` - Best quality, 3.3B parameters
- `facebook/audiogen-medium` - Sound effects generation

## Web Interface

Launch Gradio interface:

```bash
cd ~/audiocraft
python -m demos.musicgen_app --share
```

## Using Python 3.9 in New Sessions

Python 3.9 is set as the local version in the audiocraft directory:

```bash
cd ~/audiocraft  # Automatically activates Python 3.9
python --version  # Should show Python 3.9.18
```

To use Python 3.9 globally:
```bash
pyenv global 3.9.18
```

## Troubleshooting

**Python 3.9 not found:**
```bash
# Reinstall Python 3.9
pyenv install 3.9.18
cd ~/audiocraft
pyenv local 3.9.18
```

**GPU not detected:**
```bash
nvidia-smi  # Check GPU availability
python -c "import torch; print(torch.cuda.is_available())"
```

**Import errors:**
```bash
cd ~/audiocraft
pip install -U audiocraft  # Reinstall AudioCraft
```

**CUDA errors:**
```bash
# Reinstall PyTorch with CUDA
pip uninstall torch torchvision torchaudio -y
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**pyenv command not found:**
```bash
# Source bashrc to load pyenv
source ~/.bashrc
# Or add to current session:
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
```

## Performance Tips

- Use `musicgen-small` for faster generation (2-3x speed)
- Set `duration` to 10-30 seconds for best results
- Batch generation: pass list of descriptions to `model.generate()`
- Monitor GPU memory: `torch.cuda.memory_allocated()`

## Links

- Repository: https://github.com/loudmantrade/audiocraft
- Original AudioCraft: https://github.com/facebookresearch/audiocraft
- Lightning.ai Docs: https://lightning.ai/docs
