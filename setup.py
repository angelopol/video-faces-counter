from setuptools import setup

setup(
    name="video-faces-counter",
    version="1.0.0",
    description="Library to count faces in a video using aws rekognition.",
    author="angelopol",
    url="https://github.com/angelopol/video-faces-counter",
    py_modules=["VideoFacesCounter"],
    install_requires=[
        "tabulate",
        "boto3",
        "opencv-python",
        "numpy"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)