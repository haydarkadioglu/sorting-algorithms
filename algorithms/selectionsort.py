"""
Selection Sort Algorithm Implementation
Complete visualization of the Selection Sort algorithm with step-by-step animation.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import random
import time
from typing import List, Dict, Tuple
from algorithms.base_algorithm import SortingAlgorithmBase

class SelectionSortAlgorithm(SortingAlgorithmBase):
    """
    Selection Sort algorithm visualization implementation
    """
    
    # Algorithm metadata
    algorithm_name = "Selection Sort"
    description = """Selection Sort is a simple comparison-based sorting algorithm. It divides the input 
    list into two parts: a sorted sublist of items which is built up from left to right, and a 
    sublist of the remaining unsorted items. The algorithm finds the smallest (or largest) 
    element in the unsorted sublist, swaps it with the leftmost unsorted element, and moves 
    the sublist boundaries one element to the right."""
    time_complexity = "O(n²)"
    space_complexity = "O(1)"
    best_case = "O(n²)"
    worst_case = "O(n²)"
    stable = False
    
    def __init__(self, parent_frame):
        """Initialize Selection Sort visualization"""
        self.colors = self.get_color_scheme()
        self.start_time = None
        super().__init__(parent_frame)
    
    def create_gui(self):
        """Create the Selection Sort specific GUI components"""
        
        # Main container
        main_frame = ttk.Frame(self.parent_frame)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Algorithm title
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = ttk.Label(title_frame, text="Selection Sort Algorithm Visualization", 
                               font=('Arial', 16, 'bold'))
        title_label.pack()
        
        # Control panel
        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding=10)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # First row controls
        row1_frame = ttk.Frame(control_frame)
        row1_frame.pack(fill=tk.X, pady=(0, 5))
        
        # Array size control
        ttk.Label(row1_frame, text="Array Size:").pack(side=tk.LEFT)
        self.size_var = tk.StringVar(value="15")
        size_spinbox = ttk.Spinbox(row1_frame, from_=5, to=30, width=5, 
                                  textvariable=self.size_var)
        size_spinbox.pack(side=tk.LEFT, padx=(5, 15))
        
        # Speed control
        ttk.Label(row1_frame, text="Animation Speed:").pack(side=tk.LEFT)
        self.speed_var = tk.StringVar(value="Medium")
        speed_combo = ttk.Combobox(row1_frame, textvariable=self.speed_var, 
                                  values=["Very Slow", "Slow", "Medium", "Fast", "Very Fast"],
                                  state="readonly", width=10)
        speed_combo.pack(side=tk.LEFT, padx=(5, 15))
        speed_combo.bind('<<ComboboxSelected>>', self.on_speed_change)
        
        # Array generation buttons
        new_array_btn = ttk.Button(row1_frame, text="Generate New Array", 
                                  command=self.generate_new_array)
        new_array_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        manual_array_btn = ttk.Button(row1_frame, text="Manual Array", 
                                     command=self.manual_array_input)
        manual_array_btn.pack(side=tk.LEFT)
        
        # Second row controls - Sorting buttons
        row2_frame = ttk.Frame(control_frame)
        row2_frame.pack(fill=tk.X, pady=(5, 0))
        
        # Sorting control buttons
        self.start_btn = ttk.Button(row2_frame, text="▶ Start", 
                                   command=self.start_sorting)
        self.start_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.fast_btn = ttk.Button(row2_frame, text="⚡ Fast Sort", 
                                  command=self.fast_sort, 
                                  style="Fast.TButton")
        self.fast_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.pause_btn = ttk.Button(row2_frame, text="⏸ Pause", 
                                   command=self.pause_sorting, state=tk.DISABLED)
        self.pause_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.reset_btn = ttk.Button(row2_frame, text="↻ Reset", 
                                   command=self.reset_sorting)
        self.reset_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        # Step control buttons
        self.step_backward_btn = ttk.Button(row2_frame, text="⏮ Previous", 
                                           command=self.step_backward)
        self.step_backward_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.step_forward_btn = ttk.Button(row2_frame, text="⏭ Next", 
                                          command=self.step_forward)
        self.step_forward_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        # Progress information
        progress_frame = ttk.Frame(control_frame)
        progress_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.progress_label = ttk.Label(progress_frame, text="Step: 0/0")
        self.progress_label.pack(side=tk.LEFT)
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 10))
        
        self.time_label = ttk.Label(progress_frame, text="Time: 0s")
        self.time_label.pack(side=tk.RIGHT)
        
        # Save button
        save_btn = ttk.Button(progress_frame, text="📊 Save", 
                             command=self.save_visualization)
        save_btn.pack(side=tk.RIGHT, padx=(0, 10))
        
        # Status panel
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding=10)
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.status_text = tk.Text(status_frame, height=4, wrap=tk.WORD, 
                                  font=('Courier', 10), state=tk.DISABLED)
        status_scrollbar = ttk.Scrollbar(status_frame, orient=tk.VERTICAL, 
                                        command=self.status_text.yview)
        self.status_text.configure(yscrollcommand=status_scrollbar.set)
        
        self.status_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        status_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Visualization panel
        self.graph_frame = ttk.LabelFrame(main_frame, text="Visualization", padding=5)
        self.graph_frame.pack(fill=tk.BOTH, expand=True)
        
        # Style configuration
        style = ttk.Style()
        style.configure("Fast.TButton", foreground="#e74c3c", font=('Arial', 9, 'bold'))
        
        # Create matplotlib components
        self.create_matplotlib_frame()
        
        # Generate initial array
        self.generate_new_array()
    
    def create_matplotlib_frame(self):
        """Create matplotlib visualization frame"""
        
        # Create matplotlib figure
        self.fig = Figure(figsize=(10, 6), facecolor='white')
        self.ax = self.fig.add_subplot(111)
        
        # Create tkinter canvas
        self.canvas = FigureCanvasTkAgg(self.fig, self.graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Draw initial empty state
        self.draw_array()
    
    def log_message(self, message: str):
        """Add message to status panel"""
        self.status_text.config(state=tk.NORMAL)
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)
        self.status_text.config(state=tk.DISABLED)
        self.parent_frame.update()
    
    def generate_new_array(self):
        """Generate new random array"""
        try:
            size = int(self.size_var.get())
            if size < 5 or size > 30:
                messagebox.showwarning("Warning", "Array size must be between 5-30!")
                return
            
            self.generate_random_array(size)
            self.log_message(f"New array generated: {self.array}")
            self.draw_array()
            self.update_progress()
            
        except ValueError:
            messagebox.showerror("Error", "Invalid array size!")
    
    def on_speed_change(self, event=None):
        """Handle animation speed change"""
        speed_map = {
            "Very Slow": 2000,
            "Slow": 1500,
            "Medium": 1000,
            "Fast": 500,
            "Very Fast": 200
        }
        self.animation_speed = speed_map.get(self.speed_var.get(), 1000)
    
    def add_step(self, array: List[int], current_position: int = -1, 
                 minimum_index: int = -1, comparing_index: int = -1,
                 sorted_indices: List[int] = None, description: str = ""):
        """Add a step to the Selection Sort visualization"""
        step_data = {
            'array': array.copy(),
            'current_position': current_position,
            'minimum_index': minimum_index,
            'comparing_index': comparing_index,
            'sorted_indices': sorted_indices if sorted_indices else [],
            'description': description
        }
        self.steps.append(step_data)
    
    def sort_algorithm(self, arr: List[int]):
        """Selection Sort algorithm implementation"""
        n = len(arr)
        
        # Add initial step
        self.add_step(arr, description="Initial state - Selection Sort algorithm starting")
        
        sorted_indices = []
        
        # Selection sort main loop
        for i in range(n):
            # Find minimum element in remaining unsorted array
            min_idx = i
            
            self.add_step(
                arr,
                current_position=i,
                minimum_index=min_idx,
                sorted_indices=sorted_indices.copy(),
                description=f"Round {i + 1}: Looking for minimum in unsorted part [position {i} to {n-1}]"
            )
            
            self.add_step(
                arr,
                current_position=i,
                minimum_index=min_idx,
                sorted_indices=sorted_indices.copy(),
                description=f"Assume element at position {i} ({arr[i]}) is minimum"
            )
            
            # Check remaining elements
            for j in range(i + 1, n):
                self.add_step(
                    arr,
                    current_position=i,
                    minimum_index=min_idx,
                    comparing_index=j,
                    sorted_indices=sorted_indices.copy(),
                    description=f"Comparing: {arr[j]} (position {j}) with current minimum {arr[min_idx]}"
                )
                
                # Update minimum if found smaller element
                if arr[j] < arr[min_idx]:
                    min_idx = j
                    self.add_step(
                        arr,
                        current_position=i,
                        minimum_index=min_idx,
                        comparing_index=j,
                        sorted_indices=sorted_indices.copy(),
                        description=f"New minimum found! {arr[j]} at position {j}"
                    )
            
            # Swap the found minimum element with the first element
            if min_idx != i:
                self.add_step(
                    arr,
                    current_position=i,
                    minimum_index=min_idx,
                    sorted_indices=sorted_indices.copy(),
                    description=f"Swapping: {arr[i]} (position {i}) with {arr[min_idx]} (position {min_idx})"
                )
                
                arr[i], arr[min_idx] = arr[min_idx], arr[i]
                
                self.add_step(
                    arr,
                    current_position=i,
                    sorted_indices=sorted_indices.copy(),
                    description=f"Swap completed: {arr[i]} is now in position {i}"
                )
            else:
                self.add_step(
                    arr,
                    current_position=i,
                    sorted_indices=sorted_indices.copy(),
                    description=f"No swap needed: {arr[i]} is already the minimum"
                )
            
            # Mark current position as sorted
            sorted_indices.append(i)
            
            self.add_step(
                arr,
                sorted_indices=sorted_indices.copy(),
                description=f"Position {i} is now sorted. Element {arr[i]} is in correct place"
            )
        
        # Add final step
        self.add_step(
            arr,
            sorted_indices=list(range(n)),
            description="Selection Sort completed! All elements are now sorted"
        )
    
    def draw_array(self, step_data: Dict = None):
        """Draw the current array state"""
        self.ax.clear()
        
        if not self.array:
            return
        
        # Determine colors for each element
        colors = [self.colors['default']] * len(self.array)
        
        if step_data:
            # Color sorted elements (green)
            for idx in step_data.get('sorted_indices', []):
                if 0 <= idx < len(colors):
                    colors[idx] = self.colors['sorted']
            
            # Color current position (blue)
            current_pos = step_data.get('current_position', -1)
            if 0 <= current_pos < len(colors) and colors[current_pos] != self.colors['sorted']:
                colors[current_pos] = self.colors['current']
            
            # Color minimum element (red)
            min_idx = step_data.get('minimum_index', -1)
            if 0 <= min_idx < len(colors) and colors[min_idx] != self.colors['sorted']:
                colors[min_idx] = self.colors['minimum']
            
            # Color comparing element (orange)
            comp_idx = step_data.get('comparing_index', -1)
            if 0 <= comp_idx < len(colors) and colors[comp_idx] != self.colors['sorted']:
                colors[comp_idx] = self.colors['comparing']
        
        # Create bar chart
        bars = self.ax.bar(range(len(self.array)), self.array, color=colors, alpha=0.8)
        
        # Add value labels on bars
        for i, (bar, value) in enumerate(zip(bars, self.array)):
            self.ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                        str(value), ha='center', va='bottom', fontweight='bold')
        
        # Set graph properties
        self.ax.set_ylim(0, max(self.array) * 1.2)
        self.ax.set_xlabel('Index')
        self.ax.set_ylabel('Value')
        
        title = "Selection Sort Visualization"
        if step_data and step_data.get('description'):
            title += f"\n{step_data['description']}"
        self.ax.set_title(title)
        
        self.ax.grid(True, alpha=0.3)
        
        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor=self.colors['default'], label='Unsorted'),
            Patch(facecolor=self.colors['current'], label='Current Position'),
            Patch(facecolor=self.colors['minimum'], label='Current Minimum'),
            Patch(facecolor=self.colors['comparing'], label='Comparing'),
            Patch(facecolor=self.colors['sorted'], label='Sorted'),
        ]
        self.ax.legend(handles=legend_elements, loc='upper right', fontsize=8)
        
        self.canvas.draw()
    
    def show_current_step(self):
        """Display the current step"""
        if self.steps and 0 <= self.current_step < len(self.steps):
            step_data = self.steps[self.current_step]
            self.array = step_data['array'].copy()
            self.draw_array(step_data)
            self.update_progress()
            
            if step_data['description']:
                self.log_message(f"Step {self.current_step + 1}: {step_data['description']}")
    
    def start_sorting(self):
        """Start the Selection Sort animation"""
        if self.is_sorting:
            return
        
        if not self.steps:
            self.generate_steps()
        
        self.is_sorting = True
        self.is_playing = True
        
        # Update button states
        self.start_btn.config(state=tk.DISABLED)
        self.fast_btn.config(state=tk.DISABLED)
        self.pause_btn.config(state=tk.NORMAL)
        
        self.log_message("Selection Sort started...")
        self.start_time = time.time()
        
        # Start animation
        self.animate_sorting()
    
    def fast_sort(self):
        """Perform fast Selection Sort with quick animation steps"""
        if self.is_sorting:
            return
        
        if not self.array:
            return
        
        self.log_message("Fast Sort initiated...")
        self.start_time = time.time()
        
        # Generate steps if not already done
        if not self.steps:
            self.generate_steps()
        
        self.is_sorting = True
        self.is_playing = True
        
        # Update button states
        self.start_btn.config(state=tk.DISABLED)
        self.fast_btn.config(state=tk.DISABLED)
        self.pause_btn.config(state=tk.NORMAL)
        
        # Store original speed and set fast speed
        self.original_speed = self.animation_speed
        self.animation_speed = 50  # 50ms per step for fast animation
        
        # Start fast animation
        self.animate_sorting()
    
    def pause_sorting(self):
        """Pause the Selection Sort animation"""
        self.is_playing = False
        
        # Restore original speed if it was changed for fast sort
        if hasattr(self, 'original_speed'):
            self.animation_speed = self.original_speed
            delattr(self, 'original_speed')
        
        # Update button states
        self.start_btn.config(state=tk.NORMAL, text="▶ Resume")
        self.fast_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)
        
        self.log_message("Selection Sort paused.")
    
    def reset_sorting(self):
        """Reset the Selection Sort animation"""
        super().reset_sorting()
        
        # Restore original speed if it was changed for fast sort
        if hasattr(self, 'original_speed'):
            self.animation_speed = self.original_speed
            delattr(self, 'original_speed')
        
        # Update button states
        self.start_btn.config(state=tk.NORMAL, text="▶ Start")
        self.fast_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)
        
        self.log_message("Selection Sort reset.")
        
        # Update visualization
        self.draw_array()
        self.update_progress()
    
    def animate_sorting(self):
        """Animate the Selection Sort process"""
        if not self.is_playing or self.current_step >= len(self.steps):
            if self.current_step >= len(self.steps):
                self.is_sorting = False
                
                # Restore original speed if it was changed for fast sort
                if hasattr(self, 'original_speed'):
                    self.animation_speed = self.original_speed
                    delattr(self, 'original_speed')
                    self.log_message("Fast Sort completed!")
                else:
                    self.log_message("Selection Sort completed!")
                
                self.start_btn.config(state=tk.NORMAL, text="▶ Start")
                self.fast_btn.config(state=tk.NORMAL)
                self.pause_btn.config(state=tk.DISABLED)
                
                # Calculate elapsed time
                if self.start_time:
                    elapsed_time = time.time() - self.start_time
                    self.time_label.config(text=f"Time: {elapsed_time:.1f}s")
            return
        
        # Show current step
        self.show_current_step()
        self.current_step += 1
        
        # Update elapsed time
        if self.start_time:
            elapsed_time = time.time() - self.start_time
            self.time_label.config(text=f"Time: {elapsed_time:.1f}s")
        
        # Schedule next step
        if self.is_playing:
            self.parent_frame.after(self.animation_speed, self.animate_sorting)
    
    def update_progress(self):
        """Update progress information"""
        total_steps = len(self.steps) if self.steps else 0
        current = min(self.current_step + 1, total_steps)
        
        self.progress_label.config(text=f"Step: {current}/{total_steps}")
        
        if total_steps > 0:
            progress_percent = (current / total_steps) * 100
            self.progress_bar.config(value=progress_percent)
    
    def manual_array_input(self):
        """Open dialog for manual array input"""
        dialog = tk.Toplevel(self.parent_frame)
        dialog.title("Manual Array Input")
        dialog.geometry("400x200")
        dialog.transient(self.parent_frame)
        dialog.grab_set()
        
        # Instructions
        ttk.Label(dialog, text="Enter numbers separated by commas (e.g., 5,2,8,1,9):").pack(pady=10)
        
        # Input field
        entry_var = tk.StringVar()
        entry = ttk.Entry(dialog, textvariable=entry_var, width=40)
        entry.pack(pady=10)
        entry.focus()
        
        # Button frame
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)
        
        def apply_array():
            try:
                input_text = entry_var.get().strip()
                if not input_text:
                    messagebox.showwarning("Warning", "Please enter an array!")
                    return
                
                # Parse comma-separated values
                array_values = [int(x.strip()) for x in input_text.split(',')]
                
                if len(array_values) < 3:
                    messagebox.showwarning("Warning", "You must enter at least 3 elements!")
                    return
                
                if len(array_values) > 30:
                    messagebox.showwarning("Warning", "You can enter at most 30 elements!")
                    return
                
                # Set the array
                self.set_manual_array(array_values)
                
                self.log_message(f"Manual array entered: {self.array}")
                self.draw_array()
                self.update_progress()
                dialog.destroy()
                
            except ValueError:
                messagebox.showerror("Error", "Invalid number format! Use only integers and commas.")
        
        ttk.Button(button_frame, text="Apply", command=apply_array).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
        # Allow Enter key to apply
        entry.bind('<Return>', lambda e: apply_array())
    
    def save_visualization(self):
        """Save the current visualization"""
        try:
            from tkinter import filedialog
            filename = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("PDF files", "*.pdf"), ("SVG files", "*.svg")],
                title="Save Visualization"
            )
            
            if filename:
                self.fig.savefig(filename, dpi=300, bbox_inches='tight')
                messagebox.showinfo("Success", f"Visualization saved: {filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Save error: {str(e)}")