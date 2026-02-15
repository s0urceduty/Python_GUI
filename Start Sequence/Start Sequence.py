import tkinter as tk

def start_process():
    # Define steps: (Background Color, Label Text, Text Color)
    steps = [
        ("red", "Step 1: Active", "white"),
        ("orange", "Step 2: Active", "black"), # Requested black text
        ("yellow", "Step 3: Active", "black"), # Requested black text
        ("green", "Step 4: Active", "white"),
        ("blue", "Step 5: Done!", "white")
    ]
    
    start_btn.config(state="disabled")
    
    # Reset areas
    for area, label in indicator_widgets:
        area.config(bg="gray20")
        label.config(bg="gray20", fg="white", text="Inactive")

    def run_step(index):
        if index < len(steps):
            bg_color, text, fg_color = steps[index]
            area, label = indicator_widgets[index]
            
            # Light up with specific text color
            area.config(bg=bg_color)
            label.config(bg=bg_color, fg=fg_color, text=text)
            
            root.after(5000, lambda: run_step(index + 1))
        else:
            start_btn.config(state="normal")

    run_step(0)

root = tk.Tk()
root.title("Bordered Process GUI")

# 1. Main Frame (The border around all widgets)
main_container = tk.Frame(root, bd=2, relief="solid", padx=20, pady=20)
main_container.pack(padx=20, pady=20)

# 2. Start Button (Black with White Text)
# fill='x' makes it the same width as the container/indication areas
start_btn = tk.Button(main_container, text="START", bg="black", fg="white", 
                      font=("Arial", 12, "bold"), command=start_process, height=2)
start_btn.pack(fill='x', pady=(0, 20))

# 3. Indication Areas
indicator_widgets = []
for _ in range(5):
    frame = tk.Frame(main_container, height=50, width=300, bg="gray20", 
                     highlightbackground="black", highlightthickness=1)
    frame.pack(pady=5, fill='x')
    frame.pack_propagate(False)
    
    lbl = tk.Label(frame, text="Inactive", bg="gray20", fg="white", font=("Arial", 10))
    lbl.pack(expand=True, fill="both")
    
    indicator_widgets.append((frame, lbl))

root.mainloop()
