# COLMAP Gradio Interface

This project provides a **Gradio-based UI** for running **COLMAP** without using the command line.  
It works on **macOS (M1/M2/Intel)** and has been tested with the specified package versions.

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

### **Pull the Project and Install Dependencies**
```bash
git clone https://github.com/jonstephens85/colmap-gradio.git
cd colmap-gradio
pip install -r requirements.txt
```
This ensures that all packages (Gradio, Pandas, NumPy, etc.) are installed with the correct versions.
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
<br><br>
## 🔧 Troubleshooting

Issue: "botocore 1.20.112 requires urllib3<1.27, but you have urllib3 2.3.0"
Solution:
```bash
pip install "urllib3<1.27" --force-reinstall
```

Issue: "No module named gradio_client"
Solution:
```bash
pip install gradio_client
```

