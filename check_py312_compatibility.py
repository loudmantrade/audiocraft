#!/usr/bin/env python3
"""
Скрипт для проверки совместимости AudioCraft с Python 3.12
и автоматического применения патчей.
"""

import sys
import subprocess
from pathlib import Path

# Используем importlib.metadata для Python 3.8+
try:
    from importlib.metadata import version, PackageNotFoundError
except ImportError:
    # Fallback для старых версий Python
    try:
        import pkg_resources
        def version(package):
            return pkg_resources.get_distribution(package).version
        PackageNotFoundError = pkg_resources.DistributionNotFound
    except ImportError:
        print("⚠️  Warning: Cannot import package version checking utilities")
        def version(package):
            raise PackageNotFoundError(package)
        class PackageNotFoundError(Exception):
            pass


def check_python_version():
    """Проверка версии Python"""
    version = sys.version_info
    print(f"🐍 Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor == 12:
        print("✓ Python 3.12 detected")
        return True
    elif version.major == 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor} (compatible)")
        return True
    else:
        print(f"⚠️  Python {version.major}.{version.minor} may not be compatible")
        return False


def check_package(package_name, min_version=None):
    """Проверка наличия и версии пакета"""
    try:
        pkg_version = version(package_name)
        
        if min_version:
            # Простое сравнение версий
            def parse_version(v):
                return tuple(map(int, v.split('.')[:3]))
            
            try:
                if parse_version(pkg_version) >= parse_version(min_version):
                    print(f"  ✓ {package_name}=={pkg_version} (>= {min_version})")
                    return True
                else:
                    print(f"  ✗ {package_name}=={pkg_version} (required >= {min_version})")
                    return False
            except (ValueError, AttributeError):
                # Если не можем сравнить версии, просто показываем что установлено
                print(f"  ✓ {package_name}=={pkg_version}")
                return True
        else:
            print(f"  ✓ {package_name}=={pkg_version}")
            return True
    except PackageNotFoundError:
        print(f"  ✗ {package_name} not installed")
        return False


def check_dependencies():
    """Проверка всех важных зависимостей"""
    print("\n📦 Checking dependencies:")
    
    dependencies = {
        'torch': '2.1.0',
        'torchaudio': '2.1.0',
        'transformers': '4.35.0',
        'gradio': '4.0.0',
        'hydra-core': '1.3',
        'numpy': None,
        'einops': None,
        'flashy': '0.0.2',
        'encodec': '0.1.1',
    }
    
    all_ok = True
    for package, min_version in dependencies.items():
        if not check_package(package, min_version):
            all_ok = False
    
    # Проверка xformers (опционально для Python 3.12)
    if sys.version_info >= (3, 12):
        print("\n  ℹ️  xformers may not be available for Python 3.12 (optional)")
        check_package('xformers')
    else:
        if not check_package('xformers', '0.0.23'):
            all_ok = False
    
    return all_ok


def check_numpy_version():
    """Специальная проверка NumPy (должна быть < 2.0)"""
    print("\n🔢 Checking NumPy version:")
    try:
        import numpy as np
        version = np.__version__
        major = int(version.split('.')[0])
        
        if major < 2:
            print(f"  ✓ NumPy {version} (< 2.0, compatible)")
            return True
        else:
            print(f"  ⚠️  NumPy {version} (>= 2.0, may have compatibility issues)")
            print("     Recommendation: pip install 'numpy<2.0'")
            return False
    except ImportError:
        print("  ✗ NumPy not installed")
        return False


def check_torch_cuda():
    """Проверка CUDA support в PyTorch"""
    print("\n🎮 Checking CUDA support:")
    try:
        import torch
        
        print(f"  PyTorch version: {torch.__version__}")
        print(f"  CUDA available: {torch.cuda.is_available()}")
        
        if torch.cuda.is_available():
            print(f"  CUDA version: {torch.version.cuda}")
            print(f"  GPU count: {torch.cuda.device_count()}")
            for i in range(torch.cuda.device_count()):
                print(f"    GPU {i}: {torch.cuda.get_device_name(i)}")
            return True
        else:
            print("  ⚠️  CUDA not available (CPU only)")
            return False
    except ImportError:
        print("  ✗ PyTorch not installed")
        return False


def check_audiocraft():
    """Проверка установки AudioCraft"""
    print("\n🎵 Checking AudioCraft:")
    try:
        import audiocraft
        print(f"  ✓ AudioCraft version: {audiocraft.__version__}")
        
        # Попытка импорта основных моделей
        try:
            from audiocraft.models import MusicGen
            print("  ✓ MusicGen imported")
        except ImportError as e:
            print(f"  ✗ MusicGen import failed: {e}")
            return False
        
        try:
            from audiocraft.models import AudioGen
            print("  ✓ AudioGen imported")
        except ImportError as e:
            print(f"  ✗ AudioGen import failed: {e}")
            return False
        
        return True
    except ImportError:
        print("  ✗ AudioCraft not installed")
        return False


def apply_python312_patches():
    """Применить патчи для Python 3.12"""
    print("\n🔧 Applying Python 3.12 compatibility patches:")
    
    # Проверяем наличие патчей
    setup_patch = Path("setup_py312.py")
    requirements_patch = Path("requirements_py312.txt")
    
    if setup_patch.exists() and requirements_patch.exists():
        print("  ✓ Compatibility patch files found")
        
        response = input("  Apply patches? (y/n): ")
        if response.lower() == 'y':
            # Копируем патчи
            import shutil
            shutil.copy(setup_patch, "setup.py")
            shutil.copy(requirements_patch, "requirements.txt")
            print("  ✓ Patches applied")
            print("  Run: pip install -e . to reinstall")
            return True
    else:
        print("  ⚠️  Patch files not found")
        print("     Expected: setup_py312.py, requirements_py312.txt")
    
    return False


def install_missing_dependencies():
    """Установка недостающих зависимостей"""
    print("\n📥 Install missing dependencies:")
    
    response = input("  Install/upgrade dependencies for Python 3.12? (y/n): ")
    if response.lower() != 'y':
        return False
    
    packages = [
        'torch>=2.1.0',
        'torchaudio>=2.1.0',
        'transformers>=4.35.0',
        'gradio>=4.0.0',
        'hydra-core>=1.3',
        'flashy>=0.0.2',
        "'numpy<2.0'",
        'encodec>=0.1.1',
        'einops',
        'julius',
        'librosa',
        'torchmetrics',
    ]
    
    print(f"  Installing {len(packages)} packages...")
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", package])
            print(f"    ✓ {package}")
        except subprocess.CalledProcessError:
            print(f"    ✗ {package} (failed)")
    
    print("  ✓ Installation complete")
    return True


def generate_report():
    """Генерация отчета о совместимости"""
    print("\n" + "="*60)
    print("COMPATIBILITY REPORT")
    print("="*60)
    
    results = {
        'python': check_python_version(),
        'numpy': check_numpy_version(),
        'dependencies': check_dependencies(),
        'cuda': check_torch_cuda(),
        'audiocraft': check_audiocraft(),
    }
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    for check, status in results.items():
        status_icon = "✓" if status else "✗"
        print(f"{status_icon} {check.upper()}")
    
    all_ok = all(results.values())
    
    if all_ok:
        print("\n✅ All checks passed! AudioCraft is ready to use.")
    else:
        print("\n⚠️  Some checks failed. See recommendations above.")
        
        if sys.version_info >= (3, 12):
            print("\n💡 For Python 3.12, you may need to:")
            print("   1. Apply compatibility patches")
            print("   2. Install updated dependencies")
            print("   3. Use torch attention instead of xformers")
    
    return all_ok


def main():
    """Главная функция"""
    print("AudioCraft Python 3.12 Compatibility Checker")
    print("="*60)
    
    # Генерируем отчет
    all_ok = generate_report()
    
    # Предлагаем действия если есть проблемы
    if not all_ok and sys.version_info >= (3, 12):
        print("\n" + "="*60)
        print("RECOMMENDED ACTIONS")
        print("="*60)
        
        print("\n1. Apply Python 3.12 patches")
        apply_python312_patches()
        
        print("\n2. Install/upgrade dependencies")
        install_missing_dependencies()
        
        print("\n3. Reinstall AudioCraft")
        response = input("  Reinstall AudioCraft? (y/n): ")
        if response.lower() == 'y':
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", "."])
                print("  ✓ AudioCraft reinstalled")
            except subprocess.CalledProcessError:
                print("  ✗ Reinstallation failed")


if __name__ == "__main__":
    main()
