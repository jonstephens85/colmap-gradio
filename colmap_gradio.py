import gradio as gr
import os
import subprocess
import shutil
import time
from tqdm import tqdm

# Function to run COLMAP with real-time status updates
def run_colmap(images, matching_type):
    # Create a temporary workspace
    workspace = "colmap_workspace"
    image_folder = os.path.join(workspace, "images")
    db_path = os.path.join(workspace, "database.db")
    sparse_path = os.path.join(workspace, "sparse")

    # Ensure workspace exists
    os.makedirs(workspace, exist_ok=True)
    os.makedirs(image_folder, exist_ok=True)
    os.makedirs(sparse_path, exist_ok=True)

    # Save uploaded images
    for img in images:
        shutil.copy(img, image_folder)

    # Progress update list
    progress = []
    def update_progress(step):
        progress.append(step)
        return "\n".join(progress)

    # Step 1: Create COLMAP database
    update_progress("Creating database...")
    subprocess.run(f"colmap database_creator --database_path {db_path}", shell=True)

    # Step 2: Feature extraction
    update_progress("Extracting features...")
    subprocess.run(f"colmap feature_extractor --database_path {db_path} --image_path {image_folder}", shell=True)

    # Step 3: Feature matching
    update_progress(f"Running {matching_type} matching...")
    matching_cmd = {
        "Exhaustive": f"colmap exhaustive_matcher --database_path {db_path}",
        "Sequential": f"colmap sequential_matcher --database_path {db_path}",
        "Spatial": f"colmap spatial_matcher --database_path {db_path}"
    }
    subprocess.run(matching_cmd[matching_type], shell=True)

    # Step 4: Sparse reconstruction (SfM)
    update_progress("Running sparse reconstruction...")
    subprocess.run(f"colmap mapper --database_path {db_path} --image_path {image_folder} --output_path {sparse_path}", shell=True)

    # Step 5: Check for output files
    bin_files = [os.path.join(sparse_path, f) for f in ["cameras.bin", "images.bin", "points3D.bin"]]
    
    if all(os.path.exists(f) for f in bin_files):
        update_progress("COLMAP reconstruction completed!")
        return progress, bin_files
    else:
        return "Error: COLMAP did not generate the expected files.", []

# Define Gradio UI
iface = gr.Interface(
    fn=run_colmap,
    inputs=[
    gr.File(label="Upload Images", file_types=["image"], interactive=True),
    gr.Radio(["Exhaustive", "Sequential", "Spatial"], label="Feature Matching Type", value="Exhaustive")
    ],
    outputs=[gr.Textbox(label="Processing Log"), gr.File(label="Download COLMAP Files", file_types=[".bin"], interactive=True)],
    title="COLMAP Reconstruction Interface",
    description="Upload images and select a matching type. The tool will run COLMAP and generate cameras.bin, images.bin, and points3D.bin."
)

# Launch Gradio app
iface.launch()