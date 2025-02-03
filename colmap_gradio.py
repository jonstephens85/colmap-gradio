import gradio as gr
import os
import subprocess

def run_colmap(workspace, matching_type):
    # The workspace directory should contain a subdirectory called "images"
    log = []  # a list to accumulate log messages

    def add_log(msg):
        print(msg)  # also print to console for debugging
        log.append(msg)
    
    # Ensure the workspace path is absolute
    workspace = os.path.abspath(workspace)
    images_folder = os.path.join(workspace, "images")
    db_path = os.path.join(workspace, "database.db")
    sparse_path = os.path.join(workspace, "sparse")

    add_log(f"Using workspace: {workspace}")

    # Check that the images folder exists
    if not os.path.exists(images_folder):
        add_log("Error: The workspace does not contain an 'images' folder.")
        return "\n".join(log)

    # Create the sparse folder if it doesn't exist.
    os.makedirs(sparse_path, exist_ok=True)

    # Run each COLMAP step and capture its output.
    def run_command(cmd, description):
        add_log(f"=== {description} ===")
        add_log(f"Running: {cmd}")
        # Run command and capture output
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.stdout:
            add_log("STDOUT:")
            add_log(result.stdout)
        if result.stderr:
            add_log("STDERR:")
            add_log(result.stderr)
        return result.returncode

    # Step 1: Create the database
    ret = run_command(f"colmap database_creator --database_path {db_path}", "Creating database")
    if ret != 0:
        add_log("Error during database creation.")
        return "\n".join(log)

    # Step 2: Feature extraction
    ret = run_command(f"colmap feature_extractor --database_path {db_path} --image_path {images_folder}", "Extracting features")
    if ret != 0:
        add_log("Error during feature extraction.")
        return "\n".join(log)

    # Step 3: Feature matching
    matcher_cmd = {
        "Exhaustive": f"colmap exhaustive_matcher --database_path {db_path}",
        "Sequential": f"colmap sequential_matcher --database_path {db_path}",
        "Spatial": f"colmap spatial_matcher --database_path {db_path}"
    }
    ret = run_command(matcher_cmd[matching_type], f"Running {matching_type} matching")
    if ret != 0:
        add_log("Error during feature matching.")
        return "\n".join(log)

    # Step 4: Sparse reconstruction (Mapper)
    ret = run_command(f"colmap mapper --database_path {db_path} --image_path {images_folder} --output_path {sparse_path}", "Running sparse reconstruction")
    if ret != 0:
        add_log("Error during sparse reconstruction.")
        return "\n".join(log)

    # COLMAP will normally create a subdirectory (often called "0") under sparse.
    result_dir = os.path.join(sparse_path, "0")
    expected_files = [os.path.join(result_dir, fname) for fname in ["cameras.bin", "images.bin", "points3D.bin"]]

    if all(os.path.exists(f) for f in expected_files):
        add_log("COLMAP reconstruction completed successfully!")
        add_log(f"Results are in: {result_dir}")
    else:
        add_log("Error: COLMAP did not generate the expected output files.")
        for f in expected_files:
            add_log(f"  {f}: {'Found' if os.path.exists(f) else 'Not found'}")

    return "\n".join(log)

# Define a simple Gradio interface:
# - The first input is a Textbox where you paste the path to your workspace directory.
# - The second input is a Radio button to choose the matching type.
# - The output is a Textbox that shows the log.
iface = gr.Interface(
    fn=run_colmap,
    inputs=[
        gr.Textbox(label="Workspace Directory (must contain an 'images' subfolder)"),
        gr.Radio(["Exhaustive", "Sequential", "Spatial"], label="Feature Matching Type", value="Exhaustive")
    ],
    outputs=gr.Textbox(label="Processing Log"),
    title="COLMAP Reconstruction Interface",
    description=(
        "Enter the absolute path of a directory that has a subfolder called 'images'.\n"
        "COLMAP will run using that directory as its workspace and produce the COLMAP outputs "
        "inside a 'sparse/0' subfolder. The log below will indicate success or any errors."
    ),
    allow_flagging="never",
)

iface.launch()
