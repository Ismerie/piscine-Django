from django.shortcuts import render

def color(request):
    step = 255 / 50
    colors = ['black', 'red', 'blue', 'green']
    color_steps = {
        'black': [(i * step, i * step, i * step) for i in range(50)],
        'red': [(i * step, 0, 0) for i in range(50)],
        'blue': [(0, 0, i * step) for i in range(50)],
        'green': [(0, i * step, 0) for i in range(50)],
    }

    # Convert the RGB tuples to hex
    hex_colors = {color: ["#{:02X}{:02X}{:02X}".format(int(r), int(g), int(b)) for r, g, b in steps]
                  for color, steps in color_steps.items()}

    context = {
        'colors': colors,
        'hex_colors': hex_colors,
        'range': range(50),
        }
    return render(request, 'color.html', context)

# Create your views here.
