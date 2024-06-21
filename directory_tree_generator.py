import os
import sys

def generate_tree(dir_path, prefix='', exclude_files=None, is_root=True):
    if not os.path.isdir(dir_path):
        print(f"{dir_path} is not a valid directory.")
        return

    if exclude_files is None:
        exclude_files = []

    contents = [item for item in os.listdir(dir_path) if item not in exclude_files]
    contents = sorted(contents, key=lambda s: s.lower())  # Sort for consistent output

    for index, item in enumerate(contents):
        item_path = os.path.join(dir_path, item)
        connector = '├── ' if index < len(contents) - 1 else '└── '

        if is_root:
            # Print the top-level directory without prefix
            print(item)
            if os.path.isdir(item_path):
                generate_tree(item_path, '    ', exclude_files, is_root=False)
        else:
            print(prefix + connector + item)
            if os.path.isdir(item_path):
                next_prefix = prefix + ('│   ' if index < len(contents) - 1 else '    ')
                generate_tree(item_path, next_prefix, exclude_files, is_root=False)

if __name__ == "__main__":
    # Determine the directory of the executable or script
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        script_dir = os.path.dirname(sys.executable)
    else:
        # Running as script
        script_dir = os.path.dirname(os.path.realpath(__file__))
    
    # Get the script file name to exclude it from the tree
    script_name = os.path.basename(__file__)
    # Get the top-level directory name
    top_level_dir = os.path.basename(script_dir)
    # Print the top-level directory name
    print(top_level_dir)
    # Generate the tree for the contents of the script directory
    generate_tree(script_dir, exclude_files=[script_name], is_root=True)
    # Pause to keep the console window open
    input("Press Enter to exit...")
