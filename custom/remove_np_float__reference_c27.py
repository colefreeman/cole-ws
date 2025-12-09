import os
import re


@custom
def fix_numpy_float_reference(*args, **kwargs):
    """
    Search for all instances of np.float_ in the codebase and replace with np.float64
    to ensure compatibility with NumPy 2.0.
    """

    # Define the directory to search; assuming current directory or specify as needed
    root_dir = os.path.abspath(os.path.dirname(__file__))

    # Pattern to match lines with np.float_ in the code
    pattern = re.compile(r"np\.float_")

    # Walk through the directory to find Python files
    for subdir, _, files in os.walk(root_dir):
        for filename in files:
            if filename.endswith(".py"):
                file_path = os.path.join(subdir, filename)
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()

                # Check if np.float_ exists in the file
                if "np.float_" in content:
                    # Replace np.float_ with np.float64
                    new_content = pattern.sub("np.float64", content)

                    # Write back the modified content
                    with open(file_path, "w", encoding="utf-8") as file:
                        file.write(new_content)

    # Additionally, handle specific lines in known files if needed
    # For example, in 'mage_ai/shared/parsers.py' at line 61
    target_file = os.path.join(root_dir, "mage_ai", "shared", "parsers.py")
    if os.path.exists(target_file):
        with open(target_file, "r", encoding="utf-8") as f:
            content = f.read()

        if "np.float_" in content:
            new_content = re.sub(r"np\.float_", "np.float64", content)
            with open(target_file, "w", encoding="utf-8") as f:
                f.write(new_content)

    # No return value needed
    return None
