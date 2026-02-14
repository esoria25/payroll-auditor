from setuptools import setup, find_packages

setup(
    name="universal-payroll-auditor",
    version="1.0.0",
    description="Universal tool for auditing payroll data files",
    author="Your Name",
    py_modules=["universal_payroll_auditor"],
    install_requires=[
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "openpyxl>=3.1.0",
    ],
    extras_require={
        "pdf": ["pdfplumber>=0.9.0"],
        "api": ["flask>=2.0.0"],
    },
    entry_points={
        "console_scripts": [
            "payroll-audit=universal_payroll_auditor:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
