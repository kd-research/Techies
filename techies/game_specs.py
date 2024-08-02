def game_specs(key):
    return " ".join(specs[key].split())


specs = dict(

NumSeq_game_specifications = """
NumSeq Scramble is a strategic board game where players aim to form the longest
sequences of the same digit on a 15x15 grid to score points. Each player starts
with 7 number tiles, drawing from a bag, and takes turns placing tiles to build
or extend sequences horizontally or vertically. Valid moves must connect to
existing sequences, and players draw new tiles to maintain 7 in hand. Points
are awarded based on sequence length, with bonuses for special tiles and
multiple sequences in one turn. The game includes wild tiles, combo bonuses,
and blocking strategies. It ends when no more valid moves are possible, and the
player with the highest score wins. Variations include timed turns, team play,
and advanced modes. The game promotes numerical recognition, strategic
thinking, and problem-solving skills, blending the familiar Scrabble format
with numerical challenges.
""",

Wordsum_game_specifications = """
Players start with a 9x9 blank grid similar to Sudoku, where each square can
hold a letter or number tile. The objective is to fill the grid with valid
words horizontally and vertically, while each row and column must also satisfy
numerical constraints like in Sudoku or Calcudoku. Players strategically place
tiles (letters A-Z and numbers 1-9) to form words and meet numerical
requirements without repetition. Points are awarded for word complexity and
meeting numerical constraints, advancing players to more challenging levels.
Special tiles and numerical modifiers, along with time-based or limited-move
challenges, add strategic depth to the game.
""",

Boggle_game_specifications = """
Players start with a 9x9 grid, where each square has a letter.
Player could choose a square and a direction (up, down, left, right) to form a word.
The word must be at least 3 letters long.
There will be one solution that every letter in the grid is used exactly once.
""",

LexiMath_game_specifications = """
Game Title: LexiMath Concept: LexiMath combines the word-building mechanics of
popular word games with the numerical challenge of mathematical puzzles.
Players strategically place tiles on a grid to form words horizontally and
vertically while ensuring numbers in the grid satisfy mathematical equations.
Mechanics: Grid Formation: Players work on a grid divided into squares where
each square can hold either a letter tile (A-Z) or a number tile (1-9).
Objective: Form words across the grid horizontally and vertically, similar to
word games like Scrabble. Ensure numbers in the grid contribute to solving
mathematical equations presented in the puzzle. Tile Placement: Players have
tiles containing both letters and numbers. Place these tiles strategically to
form words and satisfy mathematical equations simultaneously. Mathematical
Equations: Solve equations (e.g., addition, subtraction, multiplication,
division) using numbers placed in the grid. Numbers must satisfy both row and
column numerical constraints, similar to Sudoku. Why Play LexiMath? LexiMath
offers a unique blend of linguistic creativity and mathematical logic. It
challenges players to think strategically about both forming words and solving
mathematical equations within a single grid-based puzzle format.
""",

Word2048_game_specifications = """
Word2048 merges the sliding tile mechanics of 2048 with the word-building
creativity of Scrabble. Players slide letter tiles on a grid to form words,
combining identical letters to create higher-value words. The grid consists of
cells containing letter tiles (A-Z), which can be slid in four directions to
merge identical letters and form longer words. The objective is to create words
horizontally or vertically, earning points based on word length and complexity.
Merging two identical letter tiles advances the tile to the next alphabetical
letter. Points are awarded as players form words, and new tiles appear to
challenge them further. Strategic tile movements maximize word formation while
avoiding a full grid. Special word lengths or themes yield bonus points or
unlock special tiles for strategic advantages. Word2048 offers a dynamic
gameplay experience, blending linguistic skills and spatial reasoning for fans
of both word and puzzle games.
""",

)
