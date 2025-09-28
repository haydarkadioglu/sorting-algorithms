# Sorting Algorithms Visualization

A comprehensive Python application for visualizing multiple sorting algorithms with a unified interface.

## Features

- **Unified GUI**: Single application with algorithm selection
- **Modular Architecture**: Easy to add new algorithms  
- **Step-by-step Visualization**: Watch algorithms work with detailed animations
- **Multiple Control Options**: Play, pause, step forward/backward through the sorting process
- **Customizable Arrays**: Generate random arrays or input your own data
- **Speed Control**: Adjust animation speed from very slow to very fast
- **Save Functionality**: Export visualizations as PNG, PDF, or SVG files
- **Detailed Algorithm Information**: View complexity and characteristics of each algorithm

## Available Algorithms

### Quick Sort
- **Time Complexity**: Average O(n log n), Worst O(n²)
- **Space Complexity**: O(log n)
- **Type**: Divide and conquer algorithm
- **Stability**: Not stable

## Installation

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd sorting-algorithms
   ```

2. **Install Required Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

```bash
python main_gui.py
```

### How to Use

1. **Select Algorithm**: Choose from the dropdown menu
2. **Load Algorithm**: Click "Load Algorithm" to initialize the selected algorithm
3. **Configure Array**: Set size, generate random array, or input manual values
4. **Control Animation**: Use play, pause, step controls
5. **View Information**: Click "ℹ About" for algorithm details

### Controls (Algorithm-Specific)

- **Generate New Array**: Creates a new random array of specified size
- **Manual Array**: Input your own array values
- **▶ Start**: Begin the sorting animation
- **⏸ Pause**: Pause the current animation
- **↻ Reset**: Reset to the original unsorted state
- **⏮ Previous / ⏭ Next**: Step through the algorithm manually
- **Speed Control**: Adjust animation speed (Very Slow to Very Fast)
- **📊 Save**: Export the current visualization

## Project Structure

```
sorting-algorithms/
├── main_gui.py                    # Main application entry point
├── algorithms/                    # Algorithm implementations
│   ├── __init__.py               # Package initialization
│   ├── base_algorithm.py         # Base class for all algorithms
│   └── quicksort.py              # Quick Sort implementation
├── requirements.txt              # Dependencies
└── README.md                    # Documentation
```

## Architecture

### Modular Design

The application uses a modular architecture where:

- **main_gui.py**: Main application that discovers and loads algorithms
- **base_algorithm.py**: Abstract base class defining the algorithm interface
- **Algorithm files**: Individual implementations inheriting from the base class

### Adding New Algorithms

To add a new sorting algorithm:

1. Create a new file in the `algorithms/` directory
2. Inherit from `SortingAlgorithmBase`
3. Implement required methods:
   - `create_gui()`: Create algorithm-specific GUI
   - `sort_algorithm()`: Implement the sorting logic
   - `add_step()`: Define visualization steps
   - `show_current_step()`: Display current algorithm state
4. Set algorithm metadata (name, complexity, etc.)

The main GUI will automatically discover and load the new algorithm.

## Technical Details

### Dependencies

- **Python 3.x**: Core language
- **tkinter**: GUI framework (usually comes with Python)
- **matplotlib**: Visualization and plotting
- **numpy**: Numerical operations and array handling

### Base Algorithm Interface

All algorithms inherit from `SortingAlgorithmBase` which provides:

- Common array operations
- Animation control methods
- Step management
- Color scheme definitions
- GUI component standards

## Algorithm Details

### Quick Sort

Quick Sort is a highly efficient divide-and-conquer algorithm that:

1. **Chooses a Pivot**: Selects an element as the pivot (typically the last element)
2. **Partitions**: Rearranges the array so elements smaller than pivot go left, larger go right
3. **Recursively Sorts**: Applies the same process to the left and right subarrays
4. **Combines**: The sorted subarrays naturally combine to form the final sorted array

**Visualization Features**:
- Color-coded elements (pivot, comparing, partitions)
- Step-by-step partition process
- Recursive call visualization
- Detailed status information

## Contributing

Contributions are welcome! The modular architecture makes it easy to add new algorithms:

### Adding Algorithms
1. Follow the base class interface
2. Implement visualization steps
3. Set algorithm metadata
4. Test with the main GUI

### Other Contributions
- Bug fixes
- UI improvements
- Documentation enhancements
- Performance optimizations

## License

This project is open source and available under the MIT License.

## Future Enhancements

- [ ] Additional sorting algorithms (Merge Sort, Heap Sort, Bubble Sort, etc.)
- [ ] Algorithm comparison mode
- [ ] Performance statistics
- [ ] Sound effects
- [ ] Custom themes
- [ ] Export animations
- [ ] Array generation patterns
- [ ] Educational content integration