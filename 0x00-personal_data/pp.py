#!/usr/bin/env python3

import sys

def is_safe(board, row, col, N):
    # Check if there's a queen in the same column up to the current row
    for i in range(row):
        if board[i] == col:
            return False
    
    # Check diagonals
    for i, j in enumerate(board):
        if abs(j - col) == row - i:
            return False
    
    return True

def solve_nqueens(N):
    if not isinstance(N, int):
        print("N must be a number")
        sys.exit(1)
    
    if N < 4:
        print("N must be at least 4")
        sys.exit(1)
    
    def backtrack(row, board):
        if row == N:
            solutions.append(board[:])
            return
        
        for col in range(N):
            if is_safe(board, row, col, N):
                board.append(col)
                backtrack(row + 1, board)
                board.pop()
    
    solutions = []
    backtrack(0, [])
    
    for solution in solutions:
        print([[i, solution[i]] for i in range(N)])

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: nqueens N")
        sys.exit(1)
    
    try:
        N = int(sys.argv[1])
    except ValueError:
        print("N must be a number")
        sys.exit(1)
    
    solve_nqueens(N)

