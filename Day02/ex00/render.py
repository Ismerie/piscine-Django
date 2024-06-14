import sys
import os

def verifie_file(template_file):
    settings_file = "settings.py"
    if not os.path.isfile(settings_file):
        print(f"Settings file {settings_file} not found")
        return 0
    
    if not os.path.isfile(template_file):
        print(f"Template file {template_file} not found")
        return 0
    
    _, file_extension = os.path.splitext(settings_file)
    if file_extension != ".py":
        print (f"Settings file {settings_file} doesn´t have a .py extension")
        return 0
    
    _, file_extension = os.path.splitext(template_file)
    if file_extension != ".template":
        print (f"Template file {template_file} doesn´t have a .template extension")
        return 0
    
    return 1
    
def tranform_into_dict(settings_file):
    settings = {}
    try:
        with open(settings_file, 'r') as f:
            exec(f.read(), {}, settings)
    except Exception as e:
        print(f"Error: An error occurred while reading the settings file '{settings_file}': {e}")
    return settings


def render_template(template_file, settings):
    try:
        with open(template_file, 'r') as f:
            template_content = f.read()
    except Exception as e:
        print(f"Error: An error occurred while reading the template file '{template_file}': {e}")
    return template_content.format(**settings)
    

def main(template):
    if not verifie_file(template):
        return

    settings = tranform_into_dict("settings.py")
    rendered_template = render_template(template, settings)
    
    output_file = os.path.splitext(template)[0] + '.html'
    try:
        with open(output_file, 'w') as f:
            f.write(rendered_template)
    except Exception as e:
        print(f"Error: An error occurred while writing the output file '{output_file}': {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 render.py <template_file>")
        sys.exit(1)
    template = sys.argv[1]
    main(template)
