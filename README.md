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

### Bubble Sort
- **Time Complexity**: O(n²)
- **Space Complexity**: O(1)
- **Best Case**: O(n) - when array is already sorted
- **Type**: Simple comparison-based algorithm
- **Stability**: Stable

### Selection Sort
- **Time Complexity**: O(n²)
- **Space Complexity**: O(1)
- **Best Case**: O(n²) - always the same performance
- **Type**: Simple selection-based algorithm
- **Stability**: Not stable

### Merge Sort
- **Time Complexity**: O(n log n)
- **Space Complexity**: O(n)
- **Best Case**: O(n log n) - always consistent performance
- **Type**: Divide and conquer algorithm
- **Stability**: Stable

### Insertion Sort
- **Time Complexity**: O(n²)
- **Space Complexity**: O(1)
- **Best Case**: O(n) - when array is already sorted
- **Type**: Incremental construction algorithm
- **Stability**: Stable

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/haydarkadioglu/sorting-algorithms
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

### Bubble Sort

Bubble Sort is a simple comparison-based sorting algorithm that:

1. **Compares Adjacent Elements**: Goes through the list comparing neighboring elements
2. **Swaps if Necessary**: Swaps elements if they are in the wrong order
3. **Bubbles Up**: Larger elements "bubble" to the end of the array
4. **Repeats Passes**: Continues until no more swaps are needed

**Visualization Features**:
- Color-coded elements (comparing, swapping, sorted)
- Step-by-step comparison process
- Pass-by-pass visualization
- Early termination when sorted

### Selection Sort

Selection Sort is a simple comparison-based sorting algorithm that:

1. **Divides Array**: Splits the array into sorted and unsorted parts
2. **Finds Minimum**: Finds the smallest element in the unsorted part
3. **Swaps Elements**: Swaps the minimum with the first unsorted element
4. **Moves Boundary**: Expands the sorted part by one element

**Visualization Features**:
- Color-coded elements (current position, minimum, comparing, sorted)
- Step-by-step minimum finding process
- Clear boundary between sorted and unsorted parts
- Detailed comparison explanations

### Merge Sort

Merge Sort is an efficient divide-and-conquer algorithm that:

1. **Divides**: Splits the array into two halves recursively
2. **Conquers**: Sorts each half independently
3. **Combines**: Merges the sorted halves back together
4. **Guarantees**: Consistent O(n log n) performance in all cases

**Visualization Features**:
- Color-coded subarrays (left, right, merged)
- Step-by-step divide and conquer process
- Clear merge operation visualization
- Recursive call tracking

### Insertion Sort

Insertion Sort is a simple and intuitive algorithm that:

1. **Starts Small**: Considers the first element as sorted
2. **Takes Next Element**: Picks the next unsorted element
3. **Finds Position**: Compares and finds the correct insertion position
4. **Shifts Elements**: Moves larger elements one position right
5. **Inserts**: Places the element in its correct position

**Visualization Features**:
- Color-coded elements (current, comparing, shifting, sorted)
- Step-by-step insertion process
- Clear boundary between sorted and unsorted parts
- Detailed shifting visualization

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

- [ ] Additional sorting algorithms (Heap Sort, Radix Sort, Shell Sort, etc.)
- [ ] Algorithm comparison mode
- [ ] Performance statistics
- [ ] Sound effects
- [ ] Custom themes
- [ ] Export animations
- [ ] Array generation patterns
- [ ] Educational content integration