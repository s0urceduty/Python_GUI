import tkinter as tk

class PercentageNestedSlider:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg="#121212")
        self.canvas = tk.Canvas(root, width=600, height=350, bg="#121212", highlightthickness=0)
        self.canvas.pack(pady=20)

        # Dimensions
        self.t_x1, self.t_x2 = 50, 550  
        self.b_w, self.b_h = 120, 80   
        self.r_w, self.r_h = 30, 40    
        self.max_travel = (self.t_x2 - self.t_x1) - self.b_w
        self.is_unlocked = False

        # Status text with Percentage placeholder
        self.status_text = self.canvas.create_text(300, 50, text="LOCKED 0%", fill="#FF5252", font=("Arial", 16, "bold"))

        # 1. Expanded Grey Background Container
        self.outer_track = self.canvas.create_rectangle(self.t_x1, 110, self.t_x2, 190, fill="#222222", outline="#444444", width=2)

        # 2. Numbered positions
        for i in range(0, 101, 20):
            x_pos = self.t_x1 + (i / 100) * (self.t_x2 - self.t_x1)
            self.canvas.create_text(x_pos, 210, text=str(i), fill="#888888", font=("Arial", 10))

        # 3. Outer Slider (Blue Handle)
        self.outer_h = self.canvas.create_rectangle(self.t_x1, 110, self.t_x1 + self.b_w, 190, fill="#1E88E5", outline="#BBDEFB")
        
        # 4. Inner Slider components
        self.inner_t = self.canvas.create_rectangle(self.t_x1 + 10, 145, self.t_x1 + self.b_w - 10, 155, fill="#0D47A1", outline="")
        self.inner_h = self.canvas.create_rectangle(self.t_x1 + 10, 130, self.t_x1 + 10 + self.r_w, 170, fill="#FF5252", outline="#FFCDD2")

        self.canvas.tag_bind(self.inner_h, "<B1-Motion>", self.move_inner)
        self.canvas.tag_bind(self.outer_h, "<B1-Motion>", self.move_outer)

    def update_status_label(self, pct=None):
        # Determine percentage based on blue handle position if not provided
        if pct is None:
            bx1 = self.canvas.coords(self.outer_h)[0]
            pct = int(((bx1 - self.t_x1) / self.max_travel) * 100)
        
        state = "UNLOCKED" if self.is_unlocked else "LOCKED"
        color = "#4CAF50" if self.is_unlocked else "#FF5252"
        self.canvas.itemconfig(self.status_text, text=f"{state} {pct}%", fill=color)

    def move_inner(self, event):
        bx1, _, bx2, _ = self.canvas.coords(self.outer_h)
        ix1 = max(bx1 + 10, min(event.x - self.r_w/2, bx2 - 10 - self.r_w))
        self.canvas.coords(self.inner_h, ix1, 130, ix1 + self.r_w, 170)

        # Check Unlock Condition
        self.is_unlocked = (ix1 + self.r_w >= bx2 - 11)
        self.canvas.itemconfig(self.outer_h, fill="#42A5F5" if self.is_unlocked else "#1E88E5")
        self.update_status_label()

    def move_outer(self, event):
        if not self.is_unlocked: return
        
        nx1 = max(self.t_x1, min(event.x - self.b_w/2, self.t_x2 - self.b_w))
        dx = nx1 - self.canvas.coords(self.outer_h)[0]
        
        for obj in [self.outer_h, self.inner_t, self.inner_h]:
            self.canvas.move(obj, dx, 0)
        
        self.update_status_label()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sourceduty Nested Slider")
    app = PercentageNestedSlider(root)
    root.mainloop()
