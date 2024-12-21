import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk, FigureCanvasTkAgg
import tkinter as tk

class CustomToolbar(NavigationToolbar2Tk):
    toolitems = [
        ('Home', 'Reset original view', 'home', 'home'),
        ('Pan', 'Pan axes with left mouse, zoom with right', 'move', 'pan'),
        ('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'),
        ('Save', 'Save the figure', 'filesave', 'save_figure'),
    ]

class CellularAutomata:
    def __init__(self, rows, cols):
        self.grid = np.random.choice([0, 1], size=(rows, cols))
        
    def game_of_life_step(self):
        rows, cols = self.grid.shape
        new_grid = self.grid.copy()
        
        for i in range(rows):
            for j in range(cols):
                neighbors = np.sum(self.grid[max(0, i-1):min(i+2, rows), 
                                           max(0, j-1):min(j+2, cols)]) - self.grid[i, j]
                
                if self.grid[i, j] == 1 and (neighbors < 2 or neighbors > 3):
                    new_grid[i, j] = 0
                elif self.grid[i, j] == 0 and neighbors == 3:
                    new_grid[i, j] = 1
        
        self.grid = new_grid

def animate(frame_num, img, automata):
    automata.game_of_life_step()
    img.set_array(automata.grid)
    return [img]

class Application:
    def __init__(self, master):
        self.master = master
        master.title("Conway's Game of Life")
        
        # Get user input
        rows = int(input("Enter the number of rows (recommended 50): "))
        cols = int(input("Enter the number of columns (recommended 50): "))
        self.steps = int(input("Enter the number of steps (recommended 100): "))
        
        # Create automata
        self.automata = CellularAutomata(rows, cols)
        
        # Create figure and canvas
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.draw()
        
        # Configure plot
        self.img = self.ax.imshow(self.automata.grid, interpolation='nearest', cmap='viridis')
        self.ax.grid(True)
        self.ax.set_title("Conway's Game of Life")
        self.ax.set_xlabel("Columns")
        self.ax.set_ylabel("Rows")
        
        # Add colorbar
        plt.colorbar(self.img)
        
        # Add toolbar
        self.toolbar = CustomToolbar(self.canvas, master)
        self.toolbar.update()
        
        # Pack canvas
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        # Create animation
        self.ani = animation.FuncAnimation(self.fig, animate, 
                                         fargs=(self.img, self.automata),
                                         frames=self.steps, interval=200, blit=True)
        
        # Set up closing protocol
        master.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def on_closing(self):
        self.ani.event_source.stop()
        plt.close(self.fig)
        self.master.quit()
        self.master.destroy()

def main():
    root = tk.Tk()
    app = Application(root)
    root.mainloop()

if __name__ == "__main__":
    main()