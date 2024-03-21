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
      <i>For the Mini_Max algorithms, this is the amount of ply/moves that it explores in its adversial search</i></br>
      <b>This MUST be an interger value; recommmended values are 2-4, (higher depth plays 'better', but takes longer to process)</b>
  <li>Endgame_Transition</li>
      <i>For the utility heuristic, two sets of peice square values are used; representing both the midgame and endgamee, to provide some recognition of 'perfered' locations for peices<i></br>
      <b>This is a int value, between - which is the total percent of the Endgame table utilise per each additional turn. (Recommended: 1-10) </b></br>
      A higher value will encourage more aggressive play, as it favours taking more late-game positions.</br>
      The tables are taken from the PeSTO's evaluation function, <a href=https://www.chessprogramming.org/PeSTO%27s_Evaluation_Function">See Here</a>
        
  <li>Restlessness</li>
  <i> The total amount of moves without 'progress' (any pawn move or capture), to introduce a random factor in utility of 1. </i></br>
  <b> This MUST be an integer value, (recommended values are 5-20) </b></br>
  A lower value will introduce more variety into the AI play, and reduces the likelyhood of repeated positions/systems - although, this does mean unoptimal moves are more likely to be played.
  <li>Queen_Value</li>
  The utility value associated with the Queen Peice
  <li>Rook_Value</li>
  The utility value assciated with the Rook Peice
  <li>Bishop_Value</li>
  The utility value asscoiated with the Bishop Peice
  <LI>Knight_Value</LI>
  The utility value associated with the Knight Peice
  <li>Pawn_Value</li>
  The utility value associated with the Pawn Peice
</ul>

<ul><h2>Additional options</h2></ul>

Some additional options are availible for use. 

<ul><h2>Credits</h2></ul>

Created by CodeAvali for the OCR A Level Computer Science NEA, 2023-2024
