import tkinter as tk
from tkinter import ttk
import roomba_algos
from roomba_node import randomize_map
import time

class RoombaGUI:
    def __init__(self):
        self.current_room = None
        self.room_size = 5
        
        self.window = tk.Tk()
        self.window.title("Modern Roomba Simulator")
        self.window.geometry("1050x650")
        self.window.state("zoomed")
        
        self.style = ttk.Style()
        self.style.theme_use("clam") 
        
        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=2)
        self.window.columnconfigure(2, weight=1)
        self.window.rowconfigure(0, weight=1)

        self.frm_algo_options = ttk.Frame(self.window, padding=15, relief="flat")
        self.frm_algo_options.grid(column=0, row=0, sticky="nsew")
        self.frm_algo_options.columnconfigure(0, weight=1)

        self.frm_map_container = ttk.LabelFrame(self.window, text=" Simulation Map ", padding=10)
        self.frm_map_container.grid(column=1, row=0, sticky="nsew", padx=10, pady=10)
        self.frm_map_container.columnconfigure(0, weight=1)
        self.frm_map_container.rowconfigure(0, weight=1)

        self.map_canvas = tk.Canvas(master=self.frm_map_container, bg="#EAEAEA", highlightthickness=0)
        self.map_canvas.grid(column=0, row=0, sticky="nsew")

        self.frm_state_log = ttk.LabelFrame(self.window, text=" Execution Logs ", padding=10)
        self.frm_state_log.grid(column=2, row=0, sticky="nsew", padx=10, pady=10)
        self.frm_state_log.columnconfigure(0, weight=1)
        self.frm_state_log.rowconfigure(0, weight=1)

        self.log_text = tk.Text(self.frm_state_log, bg="white", wrap=tk.WORD, font=("Consolas", 10), relief="flat")
        self.log_scroll = ttk.Scrollbar(self.frm_state_log, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=self.log_scroll.set)
        
        self.log_text.grid(column=0, row=0, sticky="nsew")
        self.log_scroll.grid(column=1, row=0, sticky="ns")

        self.algo_dict = {
            "BREADTH FIRST SEARCH 1": roomba_algos.bfs1,
            "BREADTH FIRST SEARCH 2": roomba_algos.bfs2,
            "DEPTH FIRST SEARCH 1": roomba_algos.dfs1,
            "DEPTH FIRST SEARCH 2": roomba_algos.dfs2,
            "ITERATIVE DEEPENING SEARCH": roomba_algos.ids,
            "UNIFORM COST SEARCH": roomba_algos.ucs,
            "GREEDY SEARCH": roomba_algos.greedy,
            "A* SEARCH": roomba_algos.a_star,
            "ITERATIVE DEEPENING A* SEARCH": roomba_algos.ida_star,
            "SIMPLE HILL CLIMBING": roomba_algos.simple_hc,
            "STEEPEST ASCENT HILL CLIMBING": roomba_algos.steepest_ahc,
            "STOCHASTIC HILL CLIMBING": roomba_algos.stochastic_hc,
            "RANDOM RESTART HC": roomba_algos.random_restart_hc,
            "LOCAL BEAM SEARCH": roomba_algos.local_beam_search,
            "SIMULATED ANNEALING": roomba_algos.simulated_annealing
        }

        lbl_select = ttk.Label(self.frm_algo_options, text="Select Algorithm:", font=("Helvetica", 10, "bold"))
        lbl_select.grid(column=0, row=0, sticky="w", pady=(0, 5))

        self.selected_algo = tk.StringVar()
        self.algo_cb = ttk.Combobox(self.frm_algo_options, textvariable=self.selected_algo, values=list(self.algo_dict.keys()), state="readonly")
        self.algo_cb.grid(column=0, row=1, sticky="ew", pady=(0, 20))
        self.algo_cb.current(0)

        self.style.configure("Run.TButton", font=("Helvetica", 11, "bold"), foreground="white", background="#4A90E2")
        self.style.map("Run.TButton", background=[("active", "#357ABD")])

        btn_run = ttk.Button(self.frm_algo_options, text="Run Algorithm", style="Run.TButton", command=self.run_selected)
        btn_run.grid(column=0, row=2, sticky="ew", pady=5)

        btn_random = ttk.Button(self.frm_algo_options, text="Randomize Map", command=self.generate_new_random_map)
        btn_random.grid(column=0, row=3, sticky="ew", pady=5)

        btn_redraw = ttk.Button(self.frm_algo_options, text="Redraw Room", command=lambda: self.draw_matrix_on_map(self.current_room))
        btn_redraw.grid(column=0, row=4, sticky="ew", pady=5)

        lbl_speed = ttk.Label(self.frm_algo_options, text="Animation Speed:", font=("Helvetica", 10, "bold"))
        lbl_speed.grid(column=0, row=5, sticky="w", pady=(15, 2))

        self.speed_value = tk.IntVar(value=50)
        self.speed_slider = ttk.Scale(self.frm_algo_options, from_=5, to=200, variable=self.speed_value, orient=tk.HORIZONTAL)
        self.speed_slider.grid(column=0, row=6, sticky="ew", pady=5)

        self.speed_display = ttk.Label(self.frm_algo_options, text="50 ms delay", font=("Helvetica", 9))
        self.speed_display.grid(column=0, row=7, sticky="w", pady=(0, 10))
        self.speed_value.trace_add("write", self.update_speed_display)

        lbl_room_size = ttk.Label(self.frm_algo_options, text="Random Room Size:", font=("Helvetica", 10, "bold"))
        lbl_room_size.grid(column=0, row=8, sticky="w", pady=(10, 2))

        self.room_size_display = ttk.Label(self.frm_algo_options, text="5x5", font=("Helvetica", 9))
        self.room_size_display.grid(column=0, row=9, sticky="w", pady=(0, 4))

        room_size_controls = ttk.Frame(self.frm_algo_options)
        room_size_controls.grid(column=0, row=10, sticky="ew")
        ttk.Button(room_size_controls, text="-", width=3, command=self.decrease_room_size).grid(column=0, row=0, padx=(0, 4))
        ttk.Button(room_size_controls, text="+", width=3, command=self.increase_room_size).grid(column=1, row=0)

        self.frm_algo_options.rowconfigure(11, weight=1)

        btn_clr_log = ttk.Button(self.frm_algo_options, text="Clear Log", command=lambda: self.update_log(clear=True))
        btn_clr_log.grid(column=0, row=12, sticky="ew", pady=(5, 0))

    def update_log(self, message="", clear=False):
        if clear:
            self.log_text.delete("1.0", tk.END)
        if message != "":
            self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def generate_new_random_map(self):
        self.current_room = randomize_map(self.room_size)
        self.draw_matrix_on_map(self.current_room)

    def increase_room_size(self):
        if self.room_size < 10:
            self.room_size += 1
            self.room_size_display.configure(text=f"{self.room_size}x{self.room_size}")

    def decrease_room_size(self):
        if self.room_size > 3:
            self.room_size -= 1
            self.room_size_display.configure(text=f"{self.room_size}x{self.room_size}")

    def draw_matrix_on_map(self, matrix):
        if matrix is None: return
        self.window.update_idletasks()
        
        self.map_canvas.delete("all")
        rows, cols = len(matrix), len(matrix[0])
        
        c_width = self.map_canvas.winfo_width()
        c_height = self.map_canvas.winfo_height()
        
        cell_size = min(c_width // cols, c_height // rows)
        
        if cell_size <= 0:
            cell_size = 40
            
        x_offset = (c_width - (cols * cell_size)) // 2
        y_offset = (c_height - (rows * cell_size)) // 2
        
        colors = {0: "#F5F5F5", 1: "#A07855", 2: "#333333", 3: "#2ECC71"}
        
        for r in range(rows):
            for c in range(cols):
                val = matrix[r][c]
                color = colors.get(val, "white")
                
                x1 = x_offset + (c * cell_size)
                y1 = y_offset + (r * cell_size)
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                
                self.map_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#D0D0D0", width=1)
                if val == 3:
                    padding = max(2, cell_size // 8)
                    self.map_canvas.create_oval(x1 + padding, y1 + padding, x2 - padding, y2 - padding, fill="#7F8C8D", outline="white", width=2)

    def run_selected(self):
        if self.current_room is None:
            self.update_log("Please generate a map first using Randomize!")
            return

        algo_name = self.selected_algo.get()
        algo_func = self.algo_dict[algo_name]
        message = None

        start_time = time.perf_counter()
        result = algo_func(self.current_room)
        end_time = time.perf_counter()

        if isinstance(result, tuple):
            result, message = result
        
        if result is None:
            self.update_log("No solution found to clean the room!\n")
            return
            
        path_timeline = []
        if isinstance(result, list):
            path_timeline = result
        else:
            parent_list = result.get_parent_list()
            for node in parent_list:
                if node.action is not None:
                    path_timeline.append((node.state, str("Roomba moved " + node.action)))
                else:
                    path_timeline.append((node.state, "Initial Position"))
        
        self.update_log(f"{algo_name} : {(end_time - start_time) * 1000:.1f}ms")
        if message:
            self.update_log(message)

        self.animate_steps(path_timeline, 0)

    def animate_steps(self, path_timeline, step_index):
        if step_index >= len(path_timeline):
            self.update_log("Animation complete!\n")
            return

        room_state, action_text = path_timeline[step_index]
        self.draw_matrix_on_map(room_state)
        self.update_log(action_text)

        delay = max(5, min(200, self.speed_value.get()))
        self.window.after(delay, lambda: self.animate_steps(path_timeline, step_index + 1))

    def update_speed_display(self, *args):
        delay = max(5, min(200, self.speed_value.get()))
        self.speed_display.configure(text=f"{delay} ms delay")

    def start(self):
        self.window.mainloop()