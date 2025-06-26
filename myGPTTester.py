import customtkinter as ctk
import tkinter as tk

ctk.set_appearance_mode("light")

class DraggableOpgave:
    def __init__(self, canvas, x, y, width, height, label, snap_interval=50):
        self.canvas = canvas
        self.snap_interval = snap_interval
        self.tag = f"opgave_{label}"

        # Draw rectangle and text
        self.rect = canvas.create_rectangle(x, y, x + width, y + height, fill="lightblue", outline="black", tags=self.tag)
        self.text = canvas.create_text(x + width / 2, y + height / 2, text=label, tags=self.tag)

        self._drag_data = {"x": 0, "y": 0}

        # Bind to tag (both rect and text)
        canvas.tag_bind(self.tag, "<ButtonPress-1>", self.on_press)
        canvas.tag_bind(self.tag, "<B1-Motion>", self.on_drag)
        canvas.tag_bind(self.tag, "<ButtonRelease-1>", self.on_release)

    def on_press(self, event):
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def on_drag(self, event):
        dx = event.x - self._drag_data["x"]
        self.canvas.move(self.tag, dx, 0)
        self._drag_data["x"] = event.x

    def on_release(self, event):
        x1, _, x2, _ = self.canvas.coords(self.rect)
        width = x2 - x1
        snapped_x = round(x1 / self.snap_interval) * self.snap_interval
        dx_snap = snapped_x - x1
        self.canvas.move(self.tag, dx_snap, 0)

class GanttChart(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Renovation Gantt Chart")
        self.geometry("1000x400")

        self.canvas = tk.Canvas(self, bg="white", height=300)
        self.canvas.pack(fill="both", expand=True)

        self.draw_timeline()
        self.draw_renovation_blocks()

    def draw_timeline(self):
        y = 50
        for i in range(20):
            x = i * 50
            self.canvas.create_line(x, y - 5, x, y + 5, fill="black")
            self.canvas.create_text(x, y + 20, text=f"Day {i+1}", font=("Arial", 8))
        self.canvas.create_line(0, y, 1000, y, fill="black")

    def draw_renovation_blocks(self):
        self.canvas.create_text(10, 100, anchor="w", text="Renovation 1", font=("Arial", 10, "bold"))
        DraggableOpgave(self.canvas, 100, 130, 100, 30, "Maling")
        DraggableOpgave(self.canvas, 200, 170, 100, 30, "Gulv")
        DraggableOpgave(self.canvas, 300, 210, 100, 30, "El")

if __name__ == "__main__":
    app = GanttChart()
    app.mainloop()
