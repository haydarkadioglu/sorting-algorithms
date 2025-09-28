"""
Sorting Algorithms Visualization - Main GUI Application
This application provides a unified interface for visualizing different sorting algorithms.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import importlib
import os
from pathlib import Path

class SortingAlgorithmsGUI:
    def __init__(self, root):
        """
        Main GUI Application for Sorting Algorithm Visualizations
        """
        self.root = root
        self.root.title("Sorting Algorithms Visualization")
        self.root.geometry("1200x850")
        self.root.configure(bg='#f0f0f0')
        
        # Current algorithm instance
        self.current_algorithm = None
        self.algorithm_frame = None
        
        # Available algorithms
        self.algorithms = self.discover_algorithms()
        
        # Create main interface
        self.create_main_interface()
        
        # Load default algorithm if available
        if self.algorithms:
            first_algorithm = list(self.algorithms.keys())[0]
            self.algorithm_var.set(first_algorithm)
            self.load_algorithm()
    
    def discover_algorithms(self):
        """
        Discovers available algorithm classes from the algorithms directory
        """
        algorithms = {}
        algorithms_dir = Path(__file__).parent / 'algorithms'
        
        if not algorithms_dir.exists():
            return algorithms
        
        # Look for Python files in algorithms directory
        for file_path in algorithms_dir.glob('*.py'):
            if file_path.name.startswith('__'):
                continue
                
            module_name = file_path.stem
            try:
                # Import module dynamically
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Look for Algorithm classes
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if (isinstance(attr, type) and 
                        hasattr(attr, 'algorithm_name') and 
                        attr_name.endswith('Algorithm')):
                        
                        algorithms[attr.algorithm_name] = {
                            'class': attr,
                            'module': module_name,
                            'file': str(file_path)
                        }
                        
            except Exception as e:
                print(f"Error loading algorithm from {file_path}: {e}")
        
        return algorithms
    
    def create_main_interface(self):
        """Creates the main application interface"""
        
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Application title
        title_label = ttk.Label(main_frame, text="Sorting Algorithms Visualization", 
                               font=('Arial', 18, 'bold'))
        title_label.pack(pady=(0, 15))
        
        # Algorithm selection frame
        selection_frame = ttk.LabelFrame(main_frame, text="Algorithm Selection", padding=10)
        selection_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Algorithm selection
        ttk.Label(selection_frame, text="Choose Algorithm:", 
                 font=('Arial', 11, 'bold')).pack(side=tk.LEFT, padx=(0, 10))
        
        self.algorithm_var = tk.StringVar()
        algorithm_combo = ttk.Combobox(selection_frame, textvariable=self.algorithm_var,
                                     values=list(self.algorithms.keys()),
                                     state="readonly", width=20, font=('Arial', 10))
        algorithm_combo.pack(side=tk.LEFT, padx=(0, 10))
        algorithm_combo.bind('<<ComboboxSelected>>', self.on_algorithm_change)
        
        # Load algorithm button
        load_btn = ttk.Button(selection_frame, text="Load Algorithm", 
                            command=self.load_algorithm)
        load_btn.pack(side=tk.LEFT, padx=(5, 0))
        
        # Info button
        info_btn = ttk.Button(selection_frame, text="ℹ About", 
                            command=self.show_algorithm_info)
        info_btn.pack(side=tk.RIGHT)
        
        # Algorithm container frame
        self.container_frame = ttk.Frame(main_frame)
        self.container_frame.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_frame = ttk.Frame(main_frame)
        self.status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = ttk.Label(self.status_frame, text="Ready", 
                                    font=('Arial', 9))
        self.status_label.pack(side=tk.LEFT)
        
        # Algorithm count
        algorithm_count = len(self.algorithms)
        count_label = ttk.Label(self.status_frame, 
                               text=f"Available Algorithms: {algorithm_count}",
                               font=('Arial', 9))
        count_label.pack(side=tk.RIGHT)
    
    def on_algorithm_change(self, event=None):
        """Called when algorithm selection changes"""
        selected = self.algorithm_var.get()
        if selected:
            self.status_label.config(text=f"Selected: {selected}")
    
    def load_algorithm(self):
        """Loads the selected algorithm"""
        selected = self.algorithm_var.get()
        if not selected or selected not in self.algorithms:
            messagebox.showwarning("Warning", "Please select a valid algorithm!")
            return
        
        try:
            # Clear previous algorithm
            if self.algorithm_frame:
                self.algorithm_frame.destroy()
            
            # Create new frame for the algorithm
            self.algorithm_frame = ttk.Frame(self.container_frame)
            self.algorithm_frame.pack(fill=tk.BOTH, expand=True)
            
            # Get algorithm class
            algorithm_info = self.algorithms[selected]
            algorithm_class = algorithm_info['class']
            
            # Create algorithm instance
            self.current_algorithm = algorithm_class(self.algorithm_frame)
            
            # Update status
            self.status_label.config(text=f"Loaded: {selected}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load algorithm: {str(e)}")
            self.status_label.config(text="Error loading algorithm")
    
    def show_algorithm_info(self):
        """Shows information about the selected algorithm"""
        selected = self.algorithm_var.get()
        if not selected or selected not in self.algorithms:
            messagebox.showinfo("Info", "Please select an algorithm first!")
            return
        
        algorithm_info = self.algorithms[selected]
        algorithm_class = algorithm_info['class']
        
        # Collect algorithm information
        info_text = f"Algorithm: {selected}\n\n"
        
        if hasattr(algorithm_class, 'description'):
            info_text += f"Description:\n{algorithm_class.description}\n\n"
        
        if hasattr(algorithm_class, 'time_complexity'):
            info_text += f"Time Complexity: {algorithm_class.time_complexity}\n"
        
        if hasattr(algorithm_class, 'space_complexity'):
            info_text += f"Space Complexity: {algorithm_class.space_complexity}\n"
        
        if hasattr(algorithm_class, 'best_case'):
            info_text += f"Best Case: {algorithm_class.best_case}\n"
        
        if hasattr(algorithm_class, 'worst_case'):
            info_text += f"Worst Case: {algorithm_class.worst_case}\n"
        
        if hasattr(algorithm_class, 'stable'):
            stability = "Yes" if algorithm_class.stable else "No"
            info_text += f"Stable: {stability}\n"
        
        info_text += f"\nModule: {algorithm_info['module']}"
        
        # Show info dialog
        info_dialog = tk.Toplevel(self.root)
        info_dialog.title(f"Algorithm Info - {selected}")
        info_dialog.geometry("500x400")
        info_dialog.transient(self.root)
        info_dialog.grab_set()
        
        # Text widget with scrollbar
        text_frame = ttk.Frame(info_dialog)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text_widget = tk.Text(text_frame, wrap=tk.WORD, font=('Arial', 10))
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.insert('1.0', info_text)
        text_widget.config(state=tk.DISABLED)
        
        text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Close button
        ttk.Button(info_dialog, text="Close", 
                  command=info_dialog.destroy).pack(pady=10)
    
    def refresh_algorithms(self):
        """Refreshes the list of available algorithms"""
        self.algorithms = self.discover_algorithms()
        
        # Update combobox
        algorithm_combo = None
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Combobox):
                algorithm_combo = widget
                break
        
        if algorithm_combo:
            algorithm_combo['values'] = list(self.algorithms.keys())
        
        # Update status
        algorithm_count = len(self.algorithms)
        self.status_label.config(text=f"Refreshed - Available Algorithms: {algorithm_count}")


def main():
    """Main function"""
    root = tk.Tk()
    
    # Set window icon (if available)
    try:
        root.iconbitmap('icon.ico')
    except:
        pass
    
    # Create application instance
    app = SortingAlgorithmsGUI(root)
    
    # Start main loop
    root.mainloop()


if __name__ == "__main__":
    # Add the necessary import for importlib.util
    import importlib.util
    main()