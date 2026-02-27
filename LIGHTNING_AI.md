# AudioCraft on Lightning.ai

Quick setup guide for running AudioCraft on Lightning.ai instances with Python 3.12 and GPU support.

## Quick Start

### 1. Connect to Lightning.ai

```bash
ssh s_01kjgghfgzrex7pbyr5kffsx2j@ssh.lightning.ai
```

### 2. Run Setup Script

```bash
# Download and run setup script
curl -O https://raw.githubusercontent.com/loudmantrade/audiocraft/colab-python312-support/setup_lightning_ai.sh
chmod +x setup_lightning_ai.sh
./setup_lightning_ai.sh
```

Or manually:

```bash
# Clone repository
git clone -b colab-python312-support https://github.com/loudmantrade/audiocraft.git
cd audiocraft

# Run setup
bash setup_lightning_ai.sh
```

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

## Features

✅ **Python 3.12 Support** - Fully compatible with latest Python  
✅ **GPU Acceleration** - Automatic CUDA 12.8 setup  
✅ **No xformers Required** - Uses PyTorch native attention  
✅ **Fast Installation** - ~5 minutes setup time  

## Models Available

- `facebook/musicgen-small` - Fast, 300M parameters
- `facebook/musicgen-medium` - Balanced, 1.5B parameters  
- `facebook/musicgen-large` - Best quality, 3.3B parameters
- `facebook/audiogen-medium` - Sound effects generation

## Web Interface

Launch Gradio interface:

```bash
cd ~/audiocraft
python demos/musicgen_app.py --share
```

## Troubleshooting

**GPU not detected:**
```bash
nvidia-smi  # Check GPU availability
```

**Import errors:**
```bash
cd ~/audiocraft
pip install -e .  # Reinstall AudioCraft
```

**CUDA errors:**
```bash
# Reinstall PyTorch with CUDA
pip uninstall torch torchvision torchaudio -y
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
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
