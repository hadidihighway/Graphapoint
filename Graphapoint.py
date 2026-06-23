import tkinter as tk

root = tk.Tk()
import tkinter as tk

# Default canvas settings (used by both GUI and web API)
DEFAULT_WIDTH = 600
DEFAULT_HEIGHT = 600
DEFAULT_SPACING = 25


def to_canvas(x, y, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT, spacing=DEFAULT_SPACING):
    cx = width // 2
    cy = height // 2
    canvas_x = cx + x * spacing
    canvas_y = cy - y * spacing
    return canvas_x, canvas_y


def calculate_b(point):
    x, y = point
    return y - x


def line_endpoints(point, width=DEFAULT_WIDTH, spacing=DEFAULT_SPACING):
    x, y = point
    b = calculate_b(point)
    units = (width // spacing)
    x_back = -1 * (units // 2)
    y_back = -1 * (units // 2)
    x_front = units // 2
    y_front = units // 2

    if y > 0:
        y1 = x_back + b
        x1 = x_back
        y2 = x_front + b
        x2 = x_front
    elif y < 0:
        x1 = y_back - b
        y1 = y_back
        y2 = x_front - b
        x2 = x_front
    else:  # y == 0 and x == 0 or general fallback
        x1 = -12
        y1 = -12
        x2 = 12
        y2 = 12

    return (x1, y1, x2, y2)


# --- GUI code (only run when executed directly) ---


def clear_screen(root):
    for widget in root.winfo_children():
        widget.destroy()


def build_start_screen(root):
    global label, entry, button, start_button

    label = tk.Label(root, text="Welcome to Graphapoint! Choose a point to graph: x,y")
    label.pack(pady=15)

    entry = tk.Entry(root)
    entry.pack(pady=10)

    button = tk.Button(root, text="Submit", command=input_point)
    button.pack(pady=10)

    start_button = tk.Button(root, text="Start Graphapoint", command=start)


def start():
    global root, start_button
    print("Graphapoint started!")

    start_button.destroy()
    width = DEFAULT_WIDTH
    height = DEFAULT_HEIGHT
    spacing = DEFAULT_SPACING

    canvas = tk.Canvas(root, width=width, height=height, bg="white")
    canvas.pack()

    cx = width // 2
    cy = height // 2

    for x in range(0, width, spacing):
        canvas.create_line(x, 0, x, height, fill="lightgray")

    for y in range(0, height, spacing):
        canvas.create_line(0, y, width, y, fill="lightgray")

    canvas.create_line(cx, 0, cx, height, fill="black", width=2)
    canvas.create_line(0, cy, width, cy, fill="black", width=2)

    def draw_point(point):
        x, y = point
        canvas_x, canvas_y = to_canvas(x, y, width, height, spacing)
        canvas.create_oval(canvas_x - 6, canvas_y - 6, canvas_x + 6, canvas_y + 6, fill="red")

    def draw_line(point):
        x1, y1, x2, y2 = line_endpoints(point, width=width, spacing=spacing)
        canvas_x1, canvas_y1 = to_canvas(x1, y1, width, height, spacing)
        canvas_x2, canvas_y2 = to_canvas(x2, y2, width, height, spacing)
        canvas.create_line(canvas_x1, canvas_y1, canvas_x2, canvas_y2, fill="blue", width=2)

    draw_point(point)
    draw_line(point)

    root.after(3000, show_restart_button)


def show_restart_button():
    clear_screen(root)
    restart_btn = tk.Button(root, text="Restart", command=restart)
    restart_btn.pack(pady=200)


def restart():
    clear_screen(root)
    build_start_screen(root)


def input_point():
    global point
    point = tuple(int(x) for x in entry.get().split(','))
    print("Input Value:", point)
    root.after(1000, swap_widget)
    label.config(text=f"You entered: {point}")


def swap_widget():
    button.destroy()
    label.destroy()
    entry.destroy()
    start_button.pack(pady=75)


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Graphapoint")
    root.geometry(f"{DEFAULT_WIDTH}x{DEFAULT_HEIGHT}")
    build_start_screen(root)
    root.mainloop()
