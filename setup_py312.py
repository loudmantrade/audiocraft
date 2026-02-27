# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

"""
Setup script with Python 3.12 compatibility fixes
"""

from pathlib import Path
from setuptools import setup, find_packages


NAME = 'audiocraft'
DESCRIPTION = 'Audio generation research library for PyTorch'

URL = 'https://github.com/facebookresearch/audiocraft'
AUTHOR = 'FAIR Speech & Audio'
EMAIL = 'defossez@meta.com, jadecopet@meta.com'
REQUIRES_PYTHON = '>=3.8.0,<3.13'

for line in open('audiocraft/__init__.py'):
    line = line.strip()
    if '__version__' in line:
        context = {}
        exec(line, context)
        VERSION = context['__version__']

HERE = Path(__file__).parent

try:
    with open(HERE / "README.md", encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Updated requirements for Python 3.12 compatibility
REQUIRED = [
    'av',
    'einops',
    'flashy>=0.0.2',
    'hydra-core>=1.3',
    'hydra_colorlog',
    'julius',
    'num2words',
    'numpy<2.0',  # numpy 2.0 has breaking changes
    'sentencepiece',
    'spacy>=3.7.0',
    'torch>=2.1.0',
    'torchaudio>=2.1.0',
    'huggingface_hub',
    'tqdm',
    'transformers>=4.35.0',
    'xformers>=0.0.23; python_version<"3.12"',  # xformers may not be available for 3.12
    'demucs',
    'librosa',
    'gradio>=4.0.0',
    'torchmetrics',
    'encodec>=0.1.1',
    'protobuf',
    'omegaconf',
]

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author_email=EMAIL,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    url=URL,
    python_requires=REQUIRES_PYTHON,
    install_requires=REQUIRED,
    extras_require={
        'dev': ['coverage', 'flake8', 'mypy', 'pdoc3', 'pytest'],
    },
    packages=find_packages(),
    package_data={'audiocraft': ['py.typed']},
    include_package_data=True,
    license='MIT License',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)
