from setuptools import setup, find_packages

setup(
    name='deepfoundry',
    version='0.1.0',
    description='Modular DL image classifier with Streamlit UI and custom CLI',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'streamlit>=1.32',
        'tensorflow>=2.10',
        'pandas',
        'numpy',
        'matplotlib',
        'Pillow',
        'scikit-learn'
    ],
    entry_points={
        'console_scripts': [
            'deepfoundry = deepfoundry.cli:main',
        ],
    },
    python_requires='>=3.9',
)
