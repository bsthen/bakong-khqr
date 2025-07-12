from setuptools import setup, find_packages

# Read the contents of your README file
from pathlib import Path
readme = Path(__file__).parent / "README.md"
long_description = readme.read_text(encoding="utf-8")

setup(
    name="bakong-khqr",
    version="0.4.7",
    author="BAN Sothen",
    author_email="bansokthen@gmail.com",
    description="A Python package for generating payment transactions compliant with the Bakong KHQR standard. (Unofficial NBC)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bsthen/bakong-khqr",
    packages=find_packages(exclude=["tests*"]),
    install_requires=[],
    extras_require={
        "image": ["pillow", "qrcode"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    include_package_data=True,
    project_urls={
        'Documentation': 'https://github.com/bsthen/bakong-khqr#readme',  # Replace with your documentation URL
        'Source': 'https://github.com/bsthen/bakong-khqr',  # Replace with your GitHub URL
        'Tracker': 'https://github.com/bsthen/bakong-khqr/issues',  # Replace with your issue tracker URL
    },
)
