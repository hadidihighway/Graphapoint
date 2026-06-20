import tkinter as tk

root = tk.Tk()
root.title("Graphapoint")
root.geometry("600x600")

label = tk.Label(root, text="Welcome to Graphapoint! Choose a point to graph: x,y")
label.pack(pady=15)

def start():
    
    print("Graphapoint started!")


    start_button.destroy()
    width = 600
    height = 600
    spacing = 25

    canvas = tk.Canvas(root, width=width, height=height, bg="white")
    canvas.pack()

    cx = width//2
    cy = height//2

    for x in range(0, width, spacing):
        canvas.create_line(x, 0, x, height, fill="lightgray")

    for y in range(0, height, spacing):
        canvas.create_line(0, y, width, y, fill="lightgray")

    canvas.create_line(cx, 0, cx, height, fill="black", width=2)
    canvas.create_line(0, cy, width, cy, fill="black", width=2)


    
    def to_canvas(x, y, scale=spacing):
        return cx + x * scale, cy - y * scale

    def draw_point(point):
        x, y = point
        canvas_x, canvas_y = to_canvas(x, y)
        canvas.create_oval(canvas_x-6, canvas_y-6, canvas_x+6, canvas_y+6, fill="red")
    # draw the point and the line only if a point has been submitted
    if 'point' in globals():
        draw_point(point)
        # line y = x + b that passes through the point: b = y - x
        b = point[1] - point[0]
        draw_y_equals_x_plus_b(canvas, b=b, scale=spacing, color="blue", width=2)
    else:
        label.config(text="No point provided — please Submit a point first")

def draw_y_equals_x_plus_b(canvas, b, scale=25, color="blue", width=2):
    # canvas pixel size and Cartesian center
    W = int(canvas["width"])
    H = int(canvas["height"])
    cx = W / 2
    cy = H / 2

    m = 1  # slope for y = x + b

    # math x at canvas left and right edges
    x_left = (0 - cx) / scale
    x_right = (W - cx) / scale

    # compute corresponding math y using y = m*x + b
    y_left = m * x_left + b
    y_right = m * x_right + b

    # convert math coords to canvas pixels
    px_left = cx + x_left * scale
    py_left = cy - y_left * scale
    px_right = cx + x_right * scale
    py_right = cy - y_right * scale

    canvas.create_line(px_left, py_left, px_right, py_right, fill=color, width=width)

start_button = tk.Button(root, text="Start Graphapoint", command=start)

def input_point():
    global point
    point = tuple(int(x) for x in entry.get().split(','))
    print("Input Value:", point)
    root.after(5000,swap_widget)
    label.config(text=f"You entered: {point}")

entry = tk.Entry(root)
entry.pack(pady=10)

button = tk.Button(root, text="Submit", command=input_point)
button.pack(pady=10)

def swap_widget():
    button.destroy()
    label.destroy()
    entry.destroy()
    start_button.pack(pady=75)










root.mainloop()
