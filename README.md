# Battleship-Simulation-in-Python
This project simulates a turn-based Battleship game using Python, built for a software development course. The program reads user-provided files to place ships and process guesses, handling hits, misses, and win conditions with clear console output.

# Project Overview
- Reads input files for ship placements and player guesses
- Tracks a 10x10 game board using custom object classes
- Determines hits, misses, and when ships are sunk
- Ends the game when all ships are destroyed

# Object-Oriented Concepts
- Encapsulation:
  - Each class (Ship, Board, GridPos) manages its own state and behavior
- Composition:
  - The Board is composed of a grid of GridPos objects that hold ships and track guesses
 
# Features
- Input validation (out-of-bounds, overlapping, diagonal ships)
- Turn-based guess evaluation with clear hit/miss/sunk output
- Clean object-oriented structure for extensibility

-----------------------

Note: This project was tested using instructor-given JUnit tests.
