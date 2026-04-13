# Fahrenheit 451 - Terminal Text Adventure

A modern terminal recreation of the classic MS-DOS text adventure game "Fahrenheit 451" by Telarium (1984), based on the novel by Ray Bradbury.

![Fahrenheit 451 Original Game](f451_original.jpg)

## About This Project

This project is a complete **Python** rewrite of the original Telarium adventure game, bringing Fahrenheit 451 to modern terminals. The original game files were analyzed and their data extracted to build a new engine that preserves the original game's spirit while running natively on today's systems.

**Built with Python** - A modern, clean implementation of the classic text adventure engine.

**Fully translated** - Available in both **English** and **Spanish** (Español) with a language selection menu at startup.

## Installation

```bash
pip install -e .
```

## Running the Game

```bash
fahrenheit-451
```

Or directly with Python:

```bash
python src/main.py
```

## Requirements

- Python 3.8+
- rich (for enhanced terminal display)

## Language Selection

The game starts with a language selection menu:
- Press `1` for **English**
- Press `2` for **Español**

## Controls

### English Commands
- `LOOK` or `L` - Examine your surroundings
- `GO <direction>` or just `NORTH/SOUTH/EAST/WEST` - Move
- `N, S, E, W` - Quick movement
- `EXAMINE <object>` - Look at something closely
- `TAKE <object>` - Pick up an object
- `DROP <object>` - Put down an object
- `INVENTORY` or `I` - See what you're carrying
- `SAY "text"` - Speak to someone
- `USE <object>` - Use an object
- `SAVE` - Save your game
- `LOAD` - Load saved game
- `RESTART` - Start over
- `QUIT` - Exit the game
- `HELP` - Show help

### Comandos en Español
- `MIRAR` o `M` - Examinar tu entorno
- `IR <dirección>` o `NORTE/SUR/ESTE/OESTE` - Moverse
- `N, S, E, O` - Movimiento rápido
- `EXAMINAR <objeto>` - Mirar algo de cerca
- `TOMAR <objeto>` - Coger un objeto
- `SOLTAR <objeto>` - Dejar un objeto
- `INVENTARIO` o `I` - Ver qué llevas
- `DECIR "texto"` - Hablar con alguien
- `USAR <objeto>` - Usar un objeto
- `GUARDAR` - Guardar partida
- `CARGAR` - Cargar partida guardada
- `REINICIAR` - Empezar de nuevo
- `SALIR` - Salir del juego
- `AYUDA` - Mostrar ayuda

## Game Overview

You are a firefighter in a dystopian future where books are burned. Based on Ray Bradbury's classic novel, you must navigate this oppressive world, make choices, and find your way to either escape or face the consequences.

## Project Structure

```
fahrenheit-451/
├── src/
│   ├── engine/          # Game engine
│   │   ├── engine.py    # Main game engine
│   │   ├── parser.py   # Command parser
│   │   ├── rooms.py    # Room management
│   │   ├── inventory.py # Inventory system
│   │   └── state.py     # Game state
│   ├── ui/             # Terminal UI
│   │   └── terminal.py
│   ├── i18n/           # Internationalization
│   │   ├── en.json     # English translations
│   │   └── es.json     # Spanish translations
│   └── data/           # Extracted game data
├── scripts/            # Data extraction scripts
└── tests/              # Test files
```

## Contributing

Contributions are welcome! This project is a work in progress and there's plenty to do.

### Ways to Contribute

- **Bug Reports**: Found a bug? Please open an issue with steps to reproduce.
- **Feature Requests**: Have ideas for new features? Open an issue to discuss.
- **Code Contributions**: Want to fix a bug or add a feature? Submit a pull request.
- **Translations**: Help translate the game into more languages.
- **Documentation**: Improve the docs, add examples, or write a walkthrough.
- **Game Content**: Help expand rooms, puzzles, and story elements.

### Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR-USERNAME/fahrenheit-451-terminal.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes and commit: `git commit -m 'Add some feature'`
5. Push to the branch: `git push origin feature/your-feature-name`
6. Open a Pull Request

### Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and small

### Testing

Before submitting a PR, ensure the game runs correctly:

```bash
python src/main.py
```

### Roadmap

Future improvements planned:
- [ ] Add more game puzzles and logic
- [ ] Expand the dialogue system with AI integration (Ollama)
- [ ] Add sound effects support
- [ ] More language translations
- [ ] Save/Load to custom file paths
- [ ] Add unit tests

## License

MIT License - Based on the original Telarium game (1984).
