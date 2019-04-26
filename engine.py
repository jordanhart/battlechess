#!/usr/bin/env python3
import sys
import time
import random
import numpy as np
import time
import chess

def piece_score(symbol):
  symbol = symbol.upper()
  if symbol == "P":
    return 1
  if symbol == "N":
    return 3
  if symbol == "B":
    return 3.5
  if symbol == "R":
    return 5
  if symbol == "Q":
    return 9
  return 0

# def game_over

large_number = 999


def pieces_score(board, turn):
  score = 0
  pieces = board.piece_map().values()
  for piece in pieces:
    symbol = piece.symbol()
    if turn and symbol.isupper() or not turn and symbol.islower():
      score += piece_score(symbol)
  return score



def utility(board, turn, move=None):
   score = 0
   score += pieces_score(board, turn)
   score -= pieces_score(board, not turn)

   if board.is_game_over():
    result = board.result()
    if turn and result == "1-0":
      return large_number
    if not turn and result == "0-1":
      return -large_number
    elif result == "1/2-1/2":
      if score > 0:
        return large_number // 10
      else:
        return -large_number // 10

   if move:
    if board.board.is_capture(move):
      score += .1
    if board.is_into_check(move):
      score += .1

   return score



def get_move(board, limit=100):
  # TODO: Fill this in with an actual chess engine

  start = time.time() * 1000


  random_move = random.choice(list(board.legal_moves))

  turn = board.turn

  
  i = 2
  max_move = None
  while time.time() * 1000 - start < limit - 30:
      score, move = tree(board=board, time_start=start, maximize=turn, turn=turn, turns_left=i, limit=limit)
      if move != None:
        max_move = move
      i += 1
  if max_move != None:
    return max_move
  return random_move



def tree(board, time_start, maximize, turn, turns_left, limit, alpha=float('-inf'), beta=float('inf')):
  if time.time() * 1000 - time_start > limit - 30 or turns_left <= 0:
    return utility(board, turn), None
  moves = list(board.legal_moves)
  np.random.shuffle(moves)
  sorted_moves = sorted(moves, key=lambda m: board.is_into_check(m) or board.is_capture(m), reverse=True)


  if maximize:
    max_score = float('-inf')
  else:
    max_score = float('inf')


  max_move = None
  for move in sorted_moves:
    new_board = board.copy()
    new_board.push(move)
    score, new_move = tree(new_board, time_start, not maximize, turn,  turns_left - 1, limit, alpha, beta)
    if maximize:
      if score != None and score > max_score:
        max_score = score
        max_move = new_move
      alpha = max( alpha, max_score)
      if beta <= alpha:
          break
    if not maximize:
      if score != None and score < max_score:
        max_score = score
        max_move = new_move
      beta = min(beta, max_score)
      if beta <= alpha:
        break
  return max_score, max_move






if __name__ == "__main__":
  while 1:
    cmd = input().split(" ")
    #print(cmd, file=sys.stderr)

    if cmd[0] == "uci":
      # print("uciok")
    elif cmd[0] == "ucinewgame":
      pass
    elif cmd[0] == "isready":
      # print("readyok")
    elif cmd[0] == "position":
      if cmd[1] == "startpos":
        board = chess.Board()
        if len(cmd) > 2 and cmd[2] == "moves":
          for m in cmd[3:]:
            board.push(chess.Move.from_uci(m))
    elif cmd[0] == "go":
      if len(cmd) > 1 and cmd[1] == "movetime":
        move = get_move(board, limit=int(cmd[2]))
      else:
        move = get_move(board)
      # print("bestmove %s" % move)
    elif cmd[0] == "quit":
      exit(0)
      
