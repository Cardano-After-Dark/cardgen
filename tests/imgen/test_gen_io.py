import os
import sys
import unittest
from PIL import Image

# Add the parent directory to sys.path to allow importing from imgen
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from imgen.gen_io import GenIO


def test_gen_io():
    # Create a test directory
    test_dir = "test_output"
    os.makedirs(test_dir, exist_ok=True)

    # Create a dummy image
    dummy_image = Image.new('RGB', (100, 100), color = 'red')

    # Create an instance of GenIO
    gen_io = GenIO(
        prompt="Test prompt",
        negative_prompt="Test negative prompt",
        aspect_ratio="1:1",
        seed=42,
        output_format="png",
        gen_result="Test result",
        gen_image=dummy_image
    )

    # Save the instance
    gen_io.save(test_dir, "test")

    # Load the instance back
    loaded_gen_io = GenIO.load(test_dir, "test")

    # Verify if the loaded instance matches the original
    assert loaded_gen_io.prompt == gen_io.prompt
    assert loaded_gen_io.negative_prompt == gen_io.negative_prompt
    assert loaded_gen_io.aspect_ratio == gen_io.aspect_ratio
    assert loaded_gen_io.seed == gen_io.seed
    assert loaded_gen_io.output_format == gen_io.output_format
    assert loaded_gen_io.gen_result == gen_io.gen_result
    assert loaded_gen_io.gen_image.size == gen_io.gen_image.size

    print("Test passed successfully!")

if __name__ == "__main__":
    test_gen_io()
