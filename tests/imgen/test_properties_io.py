import os
import sys
import unittest

# Add the parent directory to sys.path to allow importing from the project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from imgen.properties_io import PropertiesIO

def test_properties_io():
    # Create a test directory
    test_dir = "test_output"
    os.makedirs(test_dir, exist_ok=True)

    # Create a test properties file
    test_file = os.path.join(test_dir, "test.properties")
    with open(test_file, 'w') as f:
        f.write("stability.ai.api.key=test_api_key\n")

    # Create an instance of PropertiesIO
    props = PropertiesIO(test_file)

    # Test get_property
    assert props.get_property('stability.ai.api.key') == 'test_api_key', "Failed to get property"

    # Test set_property
    props.set_property('new.key', 'new_value')
    assert props.get_property('new.key') == 'new_value', "Failed to set property"

    # Test write and read
    props.write()
    new_props = PropertiesIO(test_file)
    assert new_props.get_property('new.key') == 'new_value', "Failed to write and read property"

    # Test get_properties
    all_props = props.get_properties()
    assert 'stability.ai.api.key' in all_props, "Missing key in get_properties"
    assert 'new.key' in all_props, "Missing key in get_properties"

    print("All tests passed successfully!")

if __name__ == "__main__":
    test_properties_io()