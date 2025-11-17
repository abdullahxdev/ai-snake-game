# 🐍 Snake AI Game - Complete Implementation

A **fully functional Snake game** with AI agents using **BFS** and **A*** search algorithms. Built for educational purposes with clean, modular code and comprehensive documentation.

## ✨ Features

### Game Features
- 🎮 **Playable Snake Game** with keyboard controls
- 🤖 **AI Autopilot** using search algorithms (BFS & A*)
- 🎨 **Dark & Light Themes** - Toggle with 'T' key
- 📊 **Visual Search Debugging** - See AI's thought process
- ⚡ **Adjustable Speed** - Control game FPS
- 🔄 **Dynamic Replanning** - AI recalculates path every move
- 🎯 **Smart Fallback** - Tail-chasing when food unreachable

### AI Features
- **BFS (Breadth-First Search)** - Guaranteed shortest path
- **A* Search** - Heuristic-guided optimal pathfinding
- **Manhattan Distance** heuristic (default)
- **Euclidean Distance** heuristic (alternative)
- **Collision Avoidance** - Simulates future body positions
- **Tail-Chasing Strategy** - Survives when food blocked

### Visualization
- 🟦 **Visited Nodes** - Cells explored by AI
- 🟨 **Frontier** - Cells being considered
- 🟡 **Planned Path** - Current route to food
- 📈 **Real-time Stats** - Score, moves, algorithm info

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)

### Installation
```bash
# 1. Clone the repository
git clone <your-repo-url>
cd snake-ai-project

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt
```

### Running the Game
```bash
# Run in human play mode
python -m snake_game.main

# Or use the run script (Unix/Mac)
chmod +x run.sh
./run.sh
```

## 🎮 Controls

| Key | Action |
|-----|--------|
| **Arrow Keys** | Move snake (Human mode) |
| **Space** | Pause/Resume |
| **R** | Restart game |
| **M** | Toggle Human/AI mode |
| **A** | Switch AI algorithm (BFS ↔ A*) |
| **T** | Toggle theme (Dark ↔ Light) |
| **V** | Toggle search visualization |
| **+/-** | Increase/Decrease speed |

## 📖 Usage Guide

### Human Play Mode
1. Launch the game
2. Use arrow keys to control the snake
3. Eat food (red circles) to grow and score points
4. Avoid walls and your own body

### AI Play Mode
1. Press **M** to switch to AI mode
2. Watch the AI play automatically
3. Press **A** to switch between BFS and A*
4. Press **V** to toggle visualization overlay
5. Observe the search process in real-time

### Configuration

Edit `snake_game/config.py` to customize:
```python
# Grid size
GRID_ROWS = 20
GRID_COLS = 20

# Game speed
DEFAULT_FPS = 10

# AI settings
AI_ALGORITHM = 'astar'  # or 'bfs'
AI_HEURISTIC = 'manhattan'  # or 'euclidean'
SHOW_SEARCH_VISUALIZATION = True
```

## 🧪 Testing

### Run Unit Tests
```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_search.py -v

# Run with coverage
pytest tests/ --cov=snake_game --cov-report=html
```

### Performance Evaluation
```bash
# Run performance comparison (50 games each)
python -m evaluation.performance_test
```

**Sample Output:**
```
PERFORMANCE COMPARISON: BFS vs A*
============================================================
Running 50 games with BFS...
  Completed 50/50 games...

BFS:
------------------------------------------------------------
  Average Score:     8.42 ± 3.15
  Max Score:         15
  Min Score:         3
  Average Moves:     156.3
  Success Rate:      94.0%

A* (Manhattan):
------------------------------------------------------------
  Average Score:     12.68 ± 4.22
  Max Score:         24
  Min Score:         5
  Average Moves:     198.7
  Success Rate:      98.0%

🏆 Best Average Score: A* (Manhattan)
```

## 📁 Project Structure
│   ├── main.py              # Game controller & main loop
│   ├── game.py              # Core game logic
│   ├── renderer.py          # Pygame rendering
│   ├── agent.py             # AI agent controller
│   ├── search.py            # BFS & A* algorithms
│   ├── heuristics.py        # Heuristic functions
│   ├── config.py            # Configuration constants
│   └── utils.py             # Helper functions
├── tests/
│   ├── __init__.py
│   ├── test_search.py       # Search algorithm tests
│   └── test_game.py         # Game logic tests
├── evaluation/
│   ├── __init__.py
│   └── performance_test.py  # Performance evaluation
├── logs/                     # AI run logs (auto-created)
├── requirements.txt          # Python dependencies
├── config.yaml              # Optional YAML config
├── README.md                # This file
└── run.sh                   # Quick start script