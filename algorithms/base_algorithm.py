"""
Base Algorithm Class for Sorting Visualizations
This module provides the base class that all sorting algorithms should inherit from.
"""

from abc import ABC, abstractmethod
import tkinter as tk
from tkinter import ttk
from typing import List, Dict, Tuple, Any

class SortingAlgorithmBase(ABC):
    """
    Abstract base class for all sorting algorithm visualizations
    """
    
    # Algorithm metadata (to be defined in subclasses)
    algorithm_name = "Base Algorithm"
    description = "Base class for sorting algorithms"
    time_complexity = "N/A"
    space_complexity = "N/A"
    best_case = "N/A"
    worst_case = "N/A"
    stable = True
    
    def __init__(self, parent_frame):
        """
        Initialize the algorithm visualization
        
        Args:
            parent_frame: The tkinter frame where the algorithm GUI will be placed
        """
        self.parent_frame = parent_frame
        self.array = []
        self.original_array = []
        self.steps = []
        self.current_step = 0
        self.is_sorting = False
        self.is_playing = False
        self.animation_speed = 1000  # milliseconds
        
        # Create the algorithm-specific GUI
        self.create_gui()
    
    @abstractmethod
    def create_gui(self):
        """
        Create the GUI components specific to this algorithm
        Must be implemented by subclasses
        """
        pass
    
    @abstractmethod
    def sort_algorithm(self, arr: List[int]) -> None:
        """
        Implement the sorting algorithm logic
        This method should populate self.steps with sorting steps
        
        Args:
            arr: The array to sort
        """
        pass
    
    @abstractmethod
    def add_step(self, array: List[int], **kwargs):
        """
        Add a step to the visualization
        
        Args:
            array: Current state of the array
            **kwargs: Algorithm-specific visualization data
        """
        pass
    
    def generate_steps(self):
        """
        Generate all sorting steps
        """
        if not self.array:
            return
        
        self.steps = []
        temp_array = self.array.copy()
        self.sort_algorithm(temp_array)
        self.array = temp_array
    
    def start_sorting(self):
        """
        Start the sorting animation
        """
        if self.is_sorting:
            return
        
        if not self.steps:
            self.generate_steps()
        
        self.is_sorting = True
        self.is_playing = True
        self.animate_sorting()
    
    def fast_sort(self):
        """
        Perform fast sorting with quick animation steps
        """
        if self.is_sorting:
            return
        
        if not self.steps:
            self.generate_steps()
        
        self.is_sorting = True
        self.is_playing = True
        
        # Set fast animation speed (50ms per step)
        original_speed = self.animation_speed
        self.animation_speed = 50
        
        # Start fast animation and restore speed when done
        self.animate_sorting()
        
        # Note: Speed will be restored in the animation completion handler
    
    def pause_sorting(self):
        """
        Pause the sorting animation
        """
        self.is_playing = False
    
    def reset_sorting(self):
        """
        Reset the sorting to initial state
        """
        self.is_sorting = False
        self.is_playing = False
        self.current_step = 0
        self.steps = []
        self.array = self.original_array.copy()
    
    def step_forward(self):
        """
        Move to the next step
        """
        if not self.steps:
            self.generate_steps()
        
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.show_current_step()
    
    def step_backward(self):
        """
        Move to the previous step
        """
        if self.current_step > 0:
            self.current_step -= 1
            self.show_current_step()
    
    @abstractmethod
    def show_current_step(self):
        """
        Display the current step
        Must be implemented by subclasses
        """
        pass
    
    def animate_sorting(self):
        """
        Animate the sorting process
        """
        if not self.is_playing or self.current_step >= len(self.steps):
            if self.current_step >= len(self.steps):
                self.is_sorting = False
            return
        
        self.show_current_step()
        self.current_step += 1
        
        if self.is_playing:
            self.parent_frame.after(self.animation_speed, self.animate_sorting)
    
    def generate_random_array(self, size: int = 15, min_val: int = 1, max_val: int = 100):
        """
        Generate a random array for sorting
        
        Args:
            size: Size of the array
            min_val: Minimum value in array
            max_val: Maximum value in array
        """
        import random
        self.array = [random.randint(min_val, max_val) for _ in range(size)]
        self.original_array = self.array.copy()
        self.steps = []
        self.current_step = 0
    
    def set_manual_array(self, array: List[int]):
        """
        Set a manual array for sorting
        
        Args:
            array: The array to sort
        """
        self.array = array.copy()
        self.original_array = self.array.copy()
        self.steps = []
        self.current_step = 0
    
    def get_color_scheme(self):
        """
        Get the default color scheme for visualization
        
        Returns:
            Dict of color mappings
        """
        return {
            'default': '#3498db',
            'comparing': '#f39c12',
            'pivot': '#e74c3c',
            'sorted': '#2ecc71',
            'current': '#9b59b6',
            'left_part': '#27ae60',
            'right_part': '#8e44ad',
            'minimum': '#e67e22'
        }