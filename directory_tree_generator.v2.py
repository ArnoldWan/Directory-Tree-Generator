import os
import sys
import webbrowser

def generate_tree(dir_path, prefix='', exclude_files=None, is_root=True, result_lines=None):
    if result_lines is None:
        result_lines = []

    if not os.path.isdir(dir_path):
        result_lines.append(f"{dir_path} is not a valid directory.")
        return result_lines

    if exclude_files is None:
        exclude_files = []

    contents = [item for item in os.listdir(dir_path) if item not in exclude_files]
    contents = sorted(contents, key=lambda s: s.lower())  # Sort for consistent output

    for index, item in enumerate(contents):
        item_path = os.path.join(dir_path, item)
        connector = '├── ' if index < len(contents) - 1 else '└── '

        if is_root:
            # Add the top-level directory without prefix
            result_lines.append(item)
            if os.path.isdir(item_path):
                generate_tree(item_path, '    ', exclude_files, is_root=False, result_lines=result_lines)
        else:
            result_lines.append(prefix + connector + item)
            if os.path.isdir(item_path):
                next_prefix = prefix + ('│   ' if index < len(contents) - 1 else '    ')
                generate_tree(item_path, next_prefix, exclude_files, is_root=False, result_lines=result_lines)
    return result_lines

def generate_html_tree(dir_path, exclude_files=None):
    if not os.path.isdir(dir_path):
        return "<p>Invalid directory.</p>"

    if exclude_files is None:
        exclude_files = []

    icon_mapping = {
        "folder": "📁",
        ".py": "🐍",  # Professional icon for Python files
        ".cs": "💻",
        ".html": "🌐",
        ".css": "🎨",
        ".js": "📜",
        ".json": "🔧",
        ".md": "📄",
        ".txt": "📄",
        "default": "📄"
    }

    def get_icon(file_name):
        _, ext = os.path.splitext(file_name)
        return icon_mapping.get(ext, icon_mapping["default"])

    def get_html_list(path, exclude_files):
        contents = [item for item in os.listdir(path) if item not in exclude_files]
        contents = sorted(contents, key=lambda s: s.lower())
        html = '<ul>'
        for item in contents:
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                html += f'<li><span class="folder">{icon_mapping["folder"]} {item}</span>{get_html_list(item_path, exclude_files)}</li>'
            else:
                html += f'<li><span class="file">{get_icon(item)} {item}</span></li>'
        html += "</ul>"
        return html

    html_structure = get_html_list(dir_path, exclude_files)
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Directory Structure</title>
        <style>
            ul {{ list-style-type: none; padding-left: 1em; }}
            .folder-structure {{ display: flex; flex-wrap: wrap; }}
            .folder-structure ul {{ margin: 0 1em 0 0; }}
            .folder::before {{ content: ""; }}
            .file::before {{ content: ""; }}
            .folder, .file {{ white-space: nowrap; }}
        </style>
    </head>
    <body>
        <h1>Directory Structure of {os.path.basename(dir_path)}</h1>
        <div class="folder-structure">{html_structure}</div>
    </body>
    </html>
    """

def get_unique_filename(path, base_name, extension):
    counter = 1
    unique_name = f"{base_name}{extension}"
    while os.path.exists(os.path.join(path, unique_name)):
        unique_name = f"{base_name}_{counter}{extension}"
        counter += 1
    return unique_name

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
    
    # Create output folder
    output_folder = os.path.join(script_dir, 'directory_tree_output')
    os.makedirs(output_folder, exist_ok=True)

    # Generate unique file names
    txt_file_name = get_unique_filename(output_folder, 'directory_structure', '.txt')
    html_file_name = get_unique_filename(output_folder, 'directory_structure', '.html')

    # Generate tree and write to TXT file
    txt_file_path = os.path.join(output_folder, txt_file_name)
    with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
        result_lines = generate_tree(script_dir, exclude_files=[script_name], is_root=True)
        txt_file.write('\n'.join(result_lines))

    # Automatically open the TXT file
    if sys.platform == "win32":
        os.startfile(txt_file_path)
    else:
        webbrowser.open('file://' + os.path.realpath(txt_file_path))
    
    # Generate HTML file
    html_file_path = os.path.join(output_folder, html_file_name)
    with open(html_file_path, 'w', encoding='utf-8') as html_file:
        html_content = generate_html_tree(script_dir, exclude_files=[script_name])
        html_file.write(html_content)

    # Automatically open the HTML file in the default web browser
    webbrowser.open('file://' + os.path.realpath(html_file_path))
