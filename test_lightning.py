#!/usr/bin/env python3
"""
Quick test script for AudioCraft on Lightning.ai
Generates a short music sample to verify installation
Requires: Python 3.9
"""

import sys
import torch
import torchaudio
from audiocraft.models import MusicGen
import time

def main():
    print("=" * 60)
    print("AudioCraft Quick Test")
    print("=" * 60)
    
    # Check Python version
    python_version = sys.version_info
    print(f"\n✓ Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    if python_version.major != 3 or python_version.minor != 9:
        print(f"⚠️  Warning: Recommended Python 3.9, you have {python_version.major}.{python_version.minor}")
    
    # Check GPU
    print(f"✓ PyTorch version: {torch.__version__}")
    print(f"✓ CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"✓ GPU: {torch.cuda.get_device_name(0)}")
        print(f"✓ CUDA version: {torch.version.cuda}")
    else:
        print("⚠️  Warning: GPU not available, generation will be slow")
    
    # Load model
    print("\n" + "=" * 60)
    print("Loading MusicGen model...")
    print("=" * 60)
    start = time.time()
    model = MusicGen.get_pretrained('facebook/musicgen-small')
    load_time = time.time() - start
    print(f"✓ Model loaded in {load_time:.1f}s")
    
    if torch.cuda.is_available():
        device = next(model.lm.parameters()).device
        print(f"✓ Model device: {device}")
        print(f"✓ GPU memory: {torch.cuda.memory_allocated(0) / 1024**2:.1f} MB")
    
    # Generate music
    print("\n" + "=" * 60)
    print("Generating music (10 seconds)...")
    print("=" * 60)
    
    model.set_generation_params(duration=10)
    description = 'upbeat electronic dance music with synthesizers'
    print(f"Prompt: {description}")
    
    start = time.time()
    wav = model.generate([description])
    gen_time = time.time() - start
    
    print(f"\n✓ Generated in {gen_time:.1f}s")
    if torch.cuda.is_available():
        print(f"✓ GPU memory peak: {torch.cuda.max_memory_allocated(0) / 1024**2:.1f} MB")
    
    # Save output
    output_path = 'test_output.wav'
    torchaudio.save(output_path, wav[0].cpu(), model.sample_rate)
    print(f"✓ Saved to: {output_path}")
    
    # File info
    import os
    file_size = os.path.getsize(output_path) / 1024
    print(f"✓ File size: {file_size:.1f} KB")
    
    print("\n" + "=" * 60)
    print("✓ Test completed successfully!")
    print("=" * 60)
    print(f"\nTo play the file:")
    print(f"  Download {output_path} or use audio player")

if __name__ == '__main__':
    main()
