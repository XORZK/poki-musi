# poki-musi
Our `poki-musi` console has a physical 16x12 RGB screen, keyboard input, and a three channel 1-bit audio system used for sound effects and background music.

The game console can effectively play Tetris, Snake and Sokoban.

<p align="center" width="100%">
    <img width="100%" src="https://raw.githubusercontent.com/XORZK/poki-musi/refs/heads/main/img/tetris.jpg">
	the <i> poki-musi </i> running Tetris.
</p>


<p align="center">
    <img width="100%" src="https://raw.githubusercontent.com/XORZK/poki-musi/refs/heads/main/img/snake.gif">
  <br>
  the <i> poki-musi </i> running Snake
</p>

## the screen
- The game console's screen was built using WS2812B individually addressable LED strips.
- These LED strips use a serial communication protocol to control an arbitrary number of RGB LEDs, w/ a single GPIO pin.
