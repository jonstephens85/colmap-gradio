# COLMAP Gradio Interface

This project provides a **Gradio-based UI** for running **COLMAP** without using the command line.  
It works on **macOS** and has been tested with the specified package versions.

Watch the [video guide](https://youtu.be/VM6trBcPlaU) to make it easier to follow along!!! 

---

## ⚙️ Installation

### **Install Conda (If You Don't Have It)**
[Download Miniconda](https://docs.conda.io/en/latest/miniconda.html) and install it.

### **Install COLMAP**
This is done easiest through [Brew](https://brew.sh/):
```bash
brew install colmap
```

### **Install ImageMagick**
This is done easiest through [Brew](https://brew.sh/):
```bash
brew install imagemagick
```

### **Create and Activate the Conda Environment**
Run the following in a terminal:

```bash
conda create --name colmap_env python=3.9 --no-default-packages -y
conda activate colmap_env
```

### **Pull the Project and Install Gradio**
```bash
git clone https://github.com/jonstephens85/colmap-gradio.git
cd colmap-gradio
pip install gradio==4.43.0
```
<br><br>

## 🚀 Usage

Start the UI by running
```bash
python colmap_gradio.py
```
Open the UI via your web browser by navigating to `http://127.0.0.1:7860/`

1. Input your workspace directory. This should include a subsfolder called `images`
2. Select downscale factor.
2. Select your feature matching type. Spatial is for imagery that is geotagged.
3. The processing log will display once complete

