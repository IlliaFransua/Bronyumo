import os
from bs4 import BeautifulSoup

def parse_style(style_str):
    rules = {}
    for rule in style_str.split(';'):
        rule = rule.strip()
        if rule and ':' in rule:
            prop, value = rule.split(':', 1)
            rules[prop.strip()] = value.strip()
    return rules

def style_dict_to_string(style_dict):
    return '; '.join(f"{prop}: {value}" for prop, value in style_dict.items()) + ';'

script_dir = os.path.dirname(os.path.realpath(__file__))

input_file_path = os.path.join(script_dir, "input.html")
output_html_path = os.path.join(script_dir, "output.html")
output_file_path = os.path.join(script_dir, "output.css")

main_tag = input("Введите общий тег для классов: ").strip()

with open(input_file_path, "r", encoding="utf-8", errors="ignore") as file:
    html = file.read()

soup = BeautifulSoup(html, 'html.parser')

styles_dict = {}

def normalize_class_name(class_name):
    return class_name[0].lower() + class_name[1:] if class_name else class_name

def add_prefix(class_name, prefix):
    return f"{prefix}-{class_name}" if prefix else class_name

for element in soup.find_all(True):
    if element.has_attr('style'):
        style_value = ' '.join(element['style'].split())
        new_rules = parse_style(style_value)
        if element.has_attr('class'):
            new_classes = []
            for cls in element['class']:
                normalized = normalize_class_name(cls)
                prefixed = add_prefix(normalized, main_tag)
                new_classes.append(prefixed)
                if prefixed in styles_dict:
                    existing_rules = parse_style(styles_dict[prefixed])
                    existing_rules.update(new_rules)
                    styles_dict[prefixed] = style_dict_to_string(existing_rules)
                else:
                    styles_dict[prefixed] = style_dict_to_string(new_rules)
            element['class'] = new_classes
        else:
            new_cls = add_prefix("generatedClass", main_tag)
            element['class'] = [new_cls]
            styles_dict[new_cls] = style_dict_to_string(new_rules)
        del element['style']
    else:
        if element.has_attr('class'):
            new_classes = [add_prefix(normalize_class_name(cls), main_tag) for cls in element['class']]
            element['class'] = new_classes

if soup.head is None:
    head_tag = soup.new_tag('head')
    soup.insert(0, head_tag)
else:
    head_tag = soup.head

link_tag = soup.new_tag('link', rel='stylesheet', href='styles.css')
head_tag.append(link_tag)

with open(output_html_path, 'w', encoding='utf-8', errors='ignore') as file:
    file.write(soup.prettify())

css_lines = []
for class_name, style in styles_dict.items():
    css_lines.append(f".{class_name} {{")
    rules = [rule.strip() for rule in style.split(';') if rule.strip()]
    for rule in rules:
        css_lines.append(f"    {rule};")
    css_lines.append("}")
    css_lines.append("")

css_content = "\n".join(css_lines)

with open(output_file_path, 'w', encoding='utf-8', errors='ignore') as file:
    file.write(css_content)

print("HTML и CSS файлы успешно сгенерированы!")
