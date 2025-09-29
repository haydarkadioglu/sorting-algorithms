"""
Merge Sort Algorithm Implementation
Complete visualization of the Merge Sort algorithm with step-by-step animation.
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

class MergeSortAlgorithm(SortingAlgorithmBase):
    """
    Merge Sort algorithm visualization implementation
    """
    
    # Algorithm metadata
    algorithm_name = "Merge Sort"
    description = """Merge Sort is a divide-and-conquer algorithm that divides the input array into two 
    halves, recursively sorts both halves, and then merges the sorted halves back together. 
    It is one of the most efficient sorting algorithms with guaranteed O(n log n) time complexity 
    in all cases. The algorithm is stable and works by repeatedly splitting the array until 
    each subarray has only one element, then merging them back in sorted order."""
    time_complexity = "O(n log n)"
    space_complexity = "O(n)"
    best_case = "O(n log n)"
    worst_case = "O(n log n)"
    stable = True
    
    def __init__(self, parent_frame):
        """Initialize Merge Sort visualization"""
        self.colors = self.get_color_scheme()
        self.start_time = None
        super().__init__(parent_frame)
    
    def create_gui(self):
        """Create the Merge Sort specific GUI components"""
        
        # Main container
        main_frame = ttk.Frame(self.parent_frame)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Algorithm title
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = ttk.Label(title_frame, text="Merge Sort Algorithm Visualization", 
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
    
    def add_step(self, array: List[int], left_subarray: Tuple[int, int] = None, 
                 right_subarray: Tuple[int, int] = None, merging_range: Tuple[int, int] = None,
                 comparing_indices: List[int] = None, description: str = ""):
        """Add a step to the Merge Sort visualization"""
        step_data = {
            'array': array.copy(),
            'left_subarray': left_subarray,
            'right_subarray': right_subarray,
            'merging_range': merging_range,
            'comparing_indices': comparing_indices if comparing_indices else [],
            'description': description
        }
        self.steps.append(step_data)
    
    def sort_algorithm(self, arr: List[int]):
        """Merge Sort algorithm implementation"""
        # Add initial step
        self.add_step(arr, description="Initial state - Merge Sort algorithm starting")
        
        # Perform merge sort
        self.merge_sort_recursive(arr, 0, len(arr) - 1)
        
        # Add final step
        self.add_step(arr, description="Merge Sort completed! Array is now fully sorted")
    
    def merge_sort_recursive(self, arr: List[int], left: int, right: int):
        """Recursive merge sort function"""
        if left < right:
            # Find the middle point
            mid = (left + right) // 2
            
            self.add_step(
                arr,
                left_subarray=(left, mid),
                right_subarray=(mid + 1, right),
                description=f"Dividing array: Left[{left}:{mid}], Right[{mid+1}:{right}]"
            )
            
            # Recursively sort both halves
            self.add_step(
                arr,
                left_subarray=(left, mid),
                description=f"Sorting left subarray: [{left}:{mid}]"
            )
            self.merge_sort_recursive(arr, left, mid)
            
            self.add_step(
                arr,
                right_subarray=(mid + 1, right),
                description=f"Sorting right subarray: [{mid+1}:{right}]"
            )
            self.merge_sort_recursive(arr, mid + 1, right)
            
            # Merge the sorted halves
            self.add_step(
                arr,
                left_subarray=(left, mid),
                right_subarray=(mid + 1, right),
                description=f"Merging sorted subarrays: [{left}:{mid}] and [{mid+1}:{right}]"
            )
            self.merge(arr, left, mid, right)
    
    def merge(self, arr: List[int], left: int, mid: int, right: int):
        """Merge two sorted subarrays"""
        # Create temporary arrays for left and right subarrays
        left_arr = arr[left:mid + 1]
        right_arr = arr[mid + 1:right + 1]
        
        self.add_step(
            arr,
            left_subarray=(left, mid),
            right_subarray=(mid + 1, right),
            description=f"Created temp arrays: Left{left_arr}, Right{right_arr}"
        )
        
        # Merge the temporary arrays back into arr[left..right]
        i = j = 0  # Initial indices for left_arr and right_arr
        k = left   # Initial index for merged array
        
        while i < len(left_arr) and j < len(right_arr):
            self.add_step(
                arr,
                merging_range=(left, right),
                comparing_indices=[left + i, mid + 1 + j],
                description=f"Comparing: {left_arr[i]} vs {right_arr[j]} at positions {left + i} and {mid + 1 + j}"
            )
            
            if left_arr[i] <= right_arr[j]:
                arr[k] = left_arr[i]
                self.add_step(
                    arr,
                    merging_range=(left, right),
                    description=f"Placed {left_arr[i]} at position {k}"
                )
                i += 1
            else:
                arr[k] = right_arr[j]
                self.add_step(
                    arr,
                    merging_range=(left, right),
                    description=f"Placed {right_arr[j]} at position {k}"
                )
                j += 1
            k += 1
        
        # Copy remaining elements of left_arr, if any
        while i < len(left_arr):
            arr[k] = left_arr[i]
            self.add_step(
                arr,
                merging_range=(left, right),
                description=f"Copying remaining left element: {left_arr[i]} to position {k}"
            )
            i += 1
            k += 1
        
        # Copy remaining elements of right_arr, if any
        while j < len(right_arr):
            arr[k] = right_arr[j]
            self.add_step(
                arr,
                merging_range=(left, right),
                description=f"Copying remaining right element: {right_arr[j]} to position {k}"
            )
            j += 1
            k += 1
        
        self.add_step(
            arr,
            merging_range=(left, right),
            description=f"Merge completed for range [{left}:{right}]"
        )
    
    def draw_array(self, step_data: Dict = None):
        """Draw the current array state"""
        self.ax.clear()
        
        if not self.array:
            return
        
        # Determine colors for each element
        colors = [self.colors['default']] * len(self.array)
        
        if step_data:
            # Color left subarray
            left_sub = step_data.get('left_subarray')
            if left_sub:
                start, end = left_sub
                for i in range(start, min(end + 1, len(colors))):
                    colors[i] = self.colors['left_part']
            
            # Color right subarray
            right_sub = step_data.get('right_subarray')
            if right_sub:
                start, end = right_sub
                for i in range(start, min(end + 1, len(colors))):
                    colors[i] = self.colors['right_part']
            
            # Color merging range
            merging_range = step_data.get('merging_range')
            if merging_range:
                start, end = merging_range
                for i in range(start, min(end + 1, len(colors))):
                    colors[i] = self.colors['sorted']
            
            # Color comparing elements
            for idx in step_data.get('comparing_indices', []):
                if 0 <= idx < len(colors):
                    colors[idx] = self.colors['comparing']
        
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
        
        title = "Merge Sort Visualization"
        if step_data and step_data.get('description'):
            title += f"\n{step_data['description']}"
        self.ax.set_title(title)
        
        self.ax.grid(True, alpha=0.3)
        
        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor=self.colors['default'], label='Unsorted'),
            Patch(facecolor=self.colors['left_part'], label='Left Subarray'),
            Patch(facecolor=self.colors['right_part'], label='Right Subarray'),
            Patch(facecolor=self.colors['comparing'], label='Comparing'),
            Patch(facecolor=self.colors['sorted'], label='Merged'),
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
        """Start the Merge Sort animation"""
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
        
        self.log_message("Merge Sort started...")
        self.start_time = time.time()
        
        # Start animation
        self.animate_sorting()
    
    def fast_sort(self):
        """Perform fast Merge Sort with quick animation steps"""
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
        """Pause the Merge Sort animation"""
        self.is_playing = False
        
        # Restore original speed if it was changed for fast sort
        if hasattr(self, 'original_speed'):
            self.animation_speed = self.original_speed
            delattr(self, 'original_speed')
        
        # Update button states
        self.start_btn.config(state=tk.NORMAL, text="▶ Resume")
        self.fast_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)
        
        self.log_message("Merge Sort paused.")
    
    def reset_sorting(self):
        """Reset the Merge Sort animation"""
        super().reset_sorting()
        
        # Restore original speed if it was changed for fast sort
        if hasattr(self, 'original_speed'):
            self.animation_speed = self.original_speed
            delattr(self, 'original_speed')
        
        # Update button states
        self.start_btn.config(state=tk.NORMAL, text="▶ Start")
        self.fast_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)
        
        self.log_message("Merge Sort reset.")
        
        # Update visualization
        self.draw_array()
        self.update_progress()
    
    def animate_sorting(self):
        """Animate the Merge Sort process"""
        if not self.is_playing or self.current_step >= len(self.steps):
            if self.current_step >= len(self.steps):
                self.is_sorting = False
                
                # Restore original speed if it was changed for fast sort
                if hasattr(self, 'original_speed'):
                    self.animation_speed = self.original_speed
                    delattr(self, 'original_speed')
                    self.log_message("Fast Sort completed!")
                else:
                    self.log_message("Merge Sort completed!")
                
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