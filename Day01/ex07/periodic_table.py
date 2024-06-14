import sys

def parse_file(lines):
    element = []
    elements = []

    for line in lines:
        infos = line.split("=")
        name = infos[0].strip()
        parts = infos[1].split(',')
        for part in parts:
            attributes = part.split(':')
            element.append(attributes[1].strip())
        element_tuple = (name, element[0], element[1], element[2], element[3])
        element.clear()
        elements.append(element_tuple)
    return elements

def add_element_inHTML(html_content, elements):
    before_pos = 18
    for infos in elements:
        if int(infos[1]) > before_pos:
            while int(infos[1]) != before_pos + 1:
                html_content += """
                        <td class="no-border"></td>"""
                before_pos += 1
        if infos[1] == '0':
            html_content += """
            <tr>"""
        html_content += f"""
                <td>
                    <h4>{infos[0]}</h4>
                    <ul>
                        <li>{infos[2]}</li>
                        <li>{infos[3]}</li>
                        <li>{infos[4]}</li>
                    </ul>
                </td>"""
        if infos[1] == '17':
            html_content += """
            </tr>"""
        before_pos = int(infos[1])
    return html_content

def main():
    with open("periodic_table.txt", "r") as file:
        lines = file.readlines()
    file.close()
    elements = []
    elements = parse_file(lines)
    # print(elements)
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tableau des Atomes</title>
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        td {
            border: 1px solid black;
        }
        th, td {
            padding: 8px;
            text-align: center;
        }
        th {
            background-color: #f2f2f2;
        }
        .no-border {
            border: 0px;
        }
    </style>
</head>
<body>
    <h2> Tableau Periodiques des elements</h2>
    <table>"""

    html_content = add_element_inHTML(html_content, elements)

    html_content += """
    </table>
</body>
</html>"""

    with open("periodic_table.html", "w") as file:
        file.write(html_content)


if __name__ == '__main__':
    main()