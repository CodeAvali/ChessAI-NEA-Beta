<h1>ChessAI Beta</h1>

This is a A Level Computer Science NEA focused on building a chess engine and using it as a medium to allow users to interact with/against a implementation of a chessbot, 
which can be varied depending on choosable weights. 

<ul><h2>Weightings</h2></ul>

These are the values that can be changed in the chessAI engine to change the playstyle/movement logic of the AI.

<ul>
  <li><h3>Personality</h3></li>
  <ul>
    <li>Human - <i>This personality allows the user to play; performing a move before enabling the AI will cause personality to be set as human</i></li>
    <li>Random_Pick - <i>Randomly picks a legal move<i></li>
    <li>Ideal_Pick - <i>According to the utility heuristic, picks the immediately 'best' move, (acts like minimax with depth=1)<i></li>
    <li>Mini_Max - <i>Performs an adversal state search, over the course of n (n=depth) moves, picking the 'best' move for that tree, according to the utility heuristic</i></li>
    <li>Mini_Max_Optimised - <i>Same as the Mini_Max algorithm, but performs alpha beta prunning to reduce the number of possible states it needs to expand, and hence returns a move in a shorter amount of time</li>
  </ul>
  <li>Depth</li>
  <li>Endgame_Transition</li>
  <li>Restlessness</li>
  <li>Queen_Value</li>
  <li>Rook_Value</li>
  <li>Bishop_Value</li>
  <LI>Knight_Value</LI>
  <li>Pawn_Value</li>
</ul>

<ul><h2>Additional options</h2></ul>

Some additional options are availible for use. 

<ul><h2>Credits</h2></ul>

Created by CodeAvali for the OCR A Level Computer Science NEA, 2023-2024
