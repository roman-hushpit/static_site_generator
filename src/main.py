import os
import shutil

from src.block import markdown_to_html_node
from src.markdown import extract_title


def copy_files_and_folders(source_dir, target_dir):
    if os.path.exists(target_dir):
        os.removedirs(target_dir)

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        target_path = os.path.join(target_dir, item)

        if os.path.isdir(source_path):
            shutil.copytree(source_path, target_path)
            print(f"Copied directory {source_path} to {target_path}")
        elif os.path.isfile(source_path):
            shutil.copy2(source_path, target_path)
            print(f"Copied file {source_path} to {target_path}")


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # Ensure the destination directory exists
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)

    # Load template content
    with open(template_path, 'r', encoding='utf-8') as template_file:
        template_content = template_file.read()

    # Iterate over all entries in the content directory
    for entry_name in os.listdir(dir_path_content):
        entry_path = os.path.join(dir_path_content, entry_name)

        # If the entry is a directory, recursively generate pages
        if os.path.isdir(entry_path):
            generate_pages_recursive(entry_path, template_path, os.path.join(dest_dir_path, entry_name))

        # If the entry is a Markdown file, generate HTML page
        elif entry_name.endswith('.md'):
            with open(entry_path, 'r', encoding='utf-8') as md_file:
                md_content = md_file.read()

            # Convert Markdown content to HTML
            html_text = markdown_to_html_node(md_content).to_html()
            title = extract_title(md_content)
            template_content = template_content.replace("{{ Title }}", title)
            template_content = template_content.replace("{{ Content }}", html_text)
            # Create file name for the HTML page
            html_file_name = os.path.splitext(entry_name)[0] + '.html'
            html_file_path = os.path.join(dest_dir_path, html_file_name)

            # Write HTML content to the destination directory
            with open(html_file_path, 'w', encoding='utf-8') as html_file:
                html_file.write(template_content)




def main():
    source_directory = '../static'
    target_directory = '../public'
    copy_files_and_folders(source_directory, target_directory)
    from_path = '../content'
    dest_path = '../public/y'
    template_path = '../template.html'
    generate_pages_recursive(from_path, template_path, dest_path)


if __name__ == "__main__":
    main()
