"""Build lambda common layer"""

import os
import shutil
import subprocess

def package_lambda_layer():
    """
    Packages a Lambda layer by creating the necessary directory,
    installing dependencies, and zipping the contents.
    """
    layer_dir = os.environ.get("LAYER_DIR")

    # Create the layer directory if it doesn't exist
    if os.path.exists(layer_dir):
        shutil.rmtree(layer_dir)
    os.makedirs(layer_dir)

    # Install dependencies into the layer directory
    subprocess.run(
        [
            "pip",
            "install",
            "-r",
            "../requirements.txt",
            "--target",
            f"{layer_dir}/python"
        ],
        check=True
    )

    # Zip the layer directory
    shutil.make_archive(f"{layer_dir}/common_layer", 'zip', layer_dir)

    # Clean up the python directory
    shutil.rmtree(f"{layer_dir}/python")

if __name__ == "__main__":
    package_lambda_layer()