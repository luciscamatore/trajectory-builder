import tkinter as tk

# Create the main application window
root = tk.Tk()
root.title("Point and Connect")

# Create a Canvas widget
canvas = tk.Canvas(root, width=800, height=600)
canvas.pack()
points = []  # List to store points
current_line = None  # To store the ID of the currently drawn line
last_points = []

def draw_point(x, y):
    canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="black")

def draw_line(start_x, start_y, end_x, end_y):
    return canvas.create_line(start_x, start_y, end_x, end_y, fill="blue")

def on_canvas_click(event):
    global current_line
    x, y = event.x, event.y
    draw_point(x, y)
    points.append((x, y))
    if current_line:
        canvas.delete(current_line)
    current_line = draw_line(points[-1][0], points[-1][1], x, y)
    last_points.extend([x, y])

def on_canvas_motion(event):
    global current_line
    if current_line:
        canvas.delete(current_line)
        current_line = draw_line(points[-1][0], points[-1][1], event.x, event.y)

def on_canvas_release(event):
    global current_line
    if current_line:
        canvas.delete(current_line)
        last_points.extend([event.x, event.y])
        canvas.create_line(last_points, fill="blue")
        current_line = draw_line(last_points[-2], last_points[-1], event.x, event.y)

canvas.bind("<Button-1>", on_canvas_click)
canvas.bind("<B1-Motion>", on_canvas_motion)
canvas.bind("<ButtonRelease-1>", on_canvas_release)
root.mainloop()
