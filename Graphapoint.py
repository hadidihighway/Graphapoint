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
    

    def draw_point(point):
        x, y = point
        canvas_x, canvas_y = to_canvas(x, y)
        canvas.create_oval(canvas_x-6, canvas_y-6, canvas_x+6, canvas_y+6, fill="red")
    
    def to_canvas(x, y):
        canvas_x = cx + x * spacing
        canvas_y = cy - y * spacing
        return canvas_x, canvas_y

    def draw_line(point):
        x,y = point
        b = calculate_b(point)
        x_back = -1 * ((width//spacing)//2)
        y_back = -1 * ((width//spacing)//2)
        x_front = (width//spacing)//2
        y_front = (width//spacing)//2
        if y > 0:
            y1 = x_back + b
            x1 = x_back
            y2 = x_front + b
            x2 = x_front

        if y < 0:
            x1 = y_back - b
            y1 = y_back
            y2 = x_front - b
            x2 = x_front

        if y == 0 and x == 0:
            x1 = -12
            y1 = -12
            y2 = 12
            x2 = 12
        
        canvas_x1, canvas_y1 = to_canvas(x1,y1)
        canvas_x2, canvas_y2 = to_canvas(x2,y2)
        canvas.create_line(canvas_x1,canvas_y1,canvas_x2,canvas_y2,fill="blue",width=2)

    def calculate_b(point):
        x,y = point
        b = y - x
        return b
    



 
    draw_point(point)
    draw_line(point)



start_button = tk.Button(root, text="Start Graphapoint", command=start)

def input_point():
    global point
    point = tuple(int(x) for x in entry.get().split(','))
    print("Input Value:", point)
    root.after(2000,swap_widget)
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
