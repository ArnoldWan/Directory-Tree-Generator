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

    contents = [item for item in os.listdir(dir_path) if item not in exclude_files and not item.endswith('.pyc')]
    contents = sorted(contents, key=lambda s: s.lower())  # Sort for consistent output

    if is_root:
        result_lines.append(os.path.abspath(dir_path))  # Add the top-level directory path
        prefix += '    '  # Increase the prefix for the next level

    for index, item in enumerate(contents):
        item_path = os.path.join(dir_path, item)
        connector = '├── ' if index < len(contents) - 1 else '└── '

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
        ".py": "🐍",
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

    def get_html_list(path, exclude_files, is_root=False):
        contents = [item for item in os.listdir(path) if item not in exclude_files and not item.endswith('.pyc')]
        contents = sorted(contents, key=lambda s: s.lower())
        folders = [item for item in contents if os.path.isdir(os.path.join(path, item))]
        files = [item for item in contents if not os.path.isdir(os.path.join(path, item))]

        html = '<ul class="nested">'
        for folder in folders:
            item_path = os.path.join(path, folder)
            html += f'<li class="folder"><span>{icon_mapping["folder"]} {folder}</span>{get_html_list(item_path, exclude_files, is_root=False)}</li>'

        for file in files:
            html += f'<li class="file"><span>{get_icon(file)} {file}</span></li>'
        html += '</ul>'
        return html

    top_level_dir = os.path.abspath(dir_path)
    html_structure = get_html_list(dir_path, exclude_files, is_root=True)
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Directory Structure</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
            }}
            ul {{
                list-style-type: none;
                padding-left: 20px;
                position: relative;
            }}
            ul ul {{
                margin-left: 20px;
            }}
            li {{
                position: relative;
                margin-left: -20px;
                cursor: pointer;
            }}
            span {{
                display: inline-block;
                margin-left: 5px;
            }}
            .top-level {{
                font-weight: bold;
                font-size: 1.2em;
            }}
            .folder > span {{
                cursor: pointer;
            }}
            .nested {{
                display: none;
            }}
            .active > .nested {{
                display: block;
            }}
            .buttons {{
                margin: 10px 0;
            }}
            .buttons button {{
                margin-right: 10px;
            }}
        </style>
    </head>
    <body>
        <h1>Directory Structure of {os.path.basename(dir_path)}</h1>
        <div class="top-level"><span>{icon_mapping["folder"]} {top_level_dir}</span></div>
        <div class="buttons">
            <button onclick="expandAll()">Expand All</button>
            <button onclick="collapseAll()">Collapse All</button>
        </div>
        <div>{html_structure}</div>
        <script>
            document.querySelectorAll('.folder > span').forEach(span => {{
                span.addEventListener('click', function() {{
                    this.parentElement.classList.toggle('active');
                }});
            }});

            function expandAll() {{
                document.querySelectorAll('.folder').forEach(folder => {{
                    folder.classList.add('active');
                }});
            }}

            function collapseAll() {{
                document.querySelectorAll('.folder').forEach(folder => {{
                    folder.classList.remove('active');
                }});
            }}
        </script>
    </body>
    </html>
    """

def get_unique_folder_name(path, base_name):
    counter = 1
    unique_name = base_name
    while os.path.exists(os.path.join(path, unique_name)):
        unique_name = f"{base_name}_{counter}"
        counter += 1
    return unique_name

def get_unique_filename(path, base_name, extension):
    counter = 1
    unique_name = f"{base_name}{extension}"
    while os.path.exists(os.path.join(path, unique_name)):
        unique_name = f"{base_name}_{counter}{extension}"
        counter += 1
    return unique_name

if __name__ == "__main__":
    # Ask the user for the folder path
    dir_path = input("Enter the directory path: ").strip()
    if not os.path.isdir(dir_path):
        print("Invalid directory path.")
        sys.exit(1)
    
    # Get the top-level directory name for output folder naming
    top_level_dir_name = os.path.basename(os.path.abspath(dir_path))
    
    # Determine the directory of the executable or script
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        script_dir = os.path.dirname(sys.executable)
    else:
        # Running as script
        script_dir = os.path.dirname(os.path.realpath(__file__))
    
    # Create output folder
    output_folder_name = get_unique_folder_name(script_dir, f"{top_level_dir_name}_output")
    output_folder = os.path.join(script_dir, output_folder_name)
    os.makedirs(output_folder, exist_ok=True)

    # Generate unique file names
    txt_file_name = get_unique_filename(output_folder, 'directory_structure', '.txt')
    html_file_name = get_unique_filename(output_folder, 'directory_structure', '.html')

    # Generate tree and write to TXT file
    txt_file_path = os.path.join(output_folder, txt_file_name)
    with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
        result_lines = generate_tree(dir_path, exclude_files=[], is_root=True)
        txt_file.write('\n'.join(result_lines))

    # Automatically open the TXT file
    if sys.platform == "win32":
        os.startfile(txt_file_path)
    else:
        webbrowser.open('file://' + os.path.realpath(txt_file_path))
    
    # Generate HTML file
    html_file_path = os.path.join(output_folder, html_file_name)
    with open(html_file_path, 'w', encoding='utf-8') as html_file:
        html_content = generate_html_tree(dir_path, exclude_files=[])
        html_file.write(html_content)

    # Automatically open the HTML file in the default web browser
    webbrowser.open('file://' + os.path.realpath(html_file_path))
