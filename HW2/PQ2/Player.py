from Board import BoardUtility
import random
import copy
import numpy as np

ROWS = 6
COLS = 6

class Player:
    def __init__(self, player_piece):
        self.piece = player_piece

    def play(self, board):
        return 0


class RandomPlayer(Player):
    def play(self, board):
        return [random.choice(BoardUtility.get_valid_locations(board)), random.choice([1, 2, 3, 4]), random.choice(["skip", "clockwise", "anticlockwise"])]


class HumanPlayer(Player):
    def play(self, board):
        move = input("row, col, region, rotation\n")
        move = move.split()
        print(move)
        return [[int(move[0]), int(move[1])], int(move[2]), move[3]]


class MiniMaxPlayer(Player):
    def __init__(self, player_piece, depth=5):
        super().__init__(player_piece)
        self.depth = depth

    def horiz_score(self, board, piece, n):
        count = 0
        op_piece = 1 if piece==2 else 2
        for c in range(COLS - n + 1):
            for r in range(ROWS):
                if np.array_equal(np.array(board[r,c:c+n]).reshape(-1),np.array([piece for _ in range(n)]).reshape(-1)):
                    count += 2
                elif np.array_equal(np.array(board[r,c:c+n]).reshape(-1),np.array([op_piece for _ in range(n)]).reshape(-1)):
                    count -= 1
        return count

    def vert_score(self, board, piece, n):
        count = 0
        op_piece = 1 if piece==2 else 2
        for c in range(COLS):
            for r in range(ROWS - n + 1):
                if np.array_equal(np.array(board[r:r+n,c]).reshape(-1),np.array([piece for _ in range(n)]).reshape(-1)):
                    count += 2
                elif np.array_equal(np.array(board[r:r+n,c]).reshape(-1),np.array([op_piece for _ in range(n)]).reshape(-1)):
                    count -= 1

        return count

    def diag_score(self, board, piece, n):
        count = 0
        op_piece = 1 if piece==2 else 2
        for c in range(COLS - n+1):
            for r in range(n-1, ROWS):
                board_game_status = np.array([board[r-i,c+i] for i in range(n)]).reshape(-1)
                if(np.array_equal(board_game_status ,np.array([piece for _ in range(n)]).reshape(-1))):
                    count += 2
                elif(np.array_equal(board_game_status ,np.array([op_piece for _ in range(n)]).reshape(-1))):
                    count -= 1

        for c in range(n-1, COLS):
            for r in range(n-1, ROWS):
                board_game_status = np.array([board[r-i,c-i] for i in range(n)]).reshape(-1)
                if(np.array_equal(board_game_status, np.array([piece for _ in range(n)]).reshape(-1))):
                    count += 2
                elif(np.array_equal(board_game_status, np.array([op_piece for _ in range(n)]).reshape(-1))):
                    count -= 1


        return count
    
    def utility(self, board):
        #return random.randint(-1000,1000)
        piece = self.piece
        vertical_score_piece = self.vert_score(board, piece, 4)*1000 + self.vert_score(board, piece, 3)*100 
        horizental_score_piece = self.horiz_score(board, piece, 4)*1000+self.horiz_score(board, piece, 3)*100 
        diagonal_score_piece = self.diag_score(board, piece, 4)*1000 + self.diag_score(board, piece, 3)*100 

        return vertical_score_piece + horizental_score_piece + diagonal_score_piece 
    
    def max_player(self, board, depth, alpha, beta):
        utility = -100000
        piece=2 if self.piece==1 else 1
        if BoardUtility.has_player_won(board, self.piece) : return 10000
        if BoardUtility.has_player_won(board, piece) : return -10000
        if BoardUtility.is_draw(board) : return -1000
        choice = ["skip", "clockwise", "anticlockwise"]
        valid_action = BoardUtility.get_valid_locations(board)
        
        for action in valid_action:
            for region in range(0, 9):
                    copy_board = copy.deepcopy(board)
                    if region == 8:
                        BoardUtility.make_move(copy_board, action[0], action[1], 1, choice[0], self.piece)
                    else:
                        BoardUtility.make_move(copy_board, action[0], action[1], region%4+1, choice[int(region/4)+1], self.piece)
                    if depth!=1:
                        new_utility = self.min_player(copy_board, depth-1)
                    else:
                        new_utility = self.utility(copy_board)

                    if(new_utility > utility):
                        utility = new_utility
                        alpha = new_utility
                    if(new_utility >= beta):
                        return utility
                    
        return utility
    

    def min_player(self, board, depth, alpha, beta):
        utility = 100000
        piece=2 if self.piece==1 else 1
        if BoardUtility.has_player_won(board, self.piece) : return 10000
        if BoardUtility.has_player_won(board, piece) : return -10000
        if BoardUtility.is_draw(board) : return -1000
        choice = ["skip", "clockwise", "anticlockwise"]
        valid_action = BoardUtility.get_valid_locations(board)

        for action in valid_action:
            for region in range(0, 9):
                    copy_board = copy.deepcopy(board)
                    if region == 8:
                        BoardUtility.make_move(copy_board, action[0], action[1], 1, choice[0], piece)
                    else:
                        BoardUtility.make_move(copy_board, action[0], action[1], region%4+1, choice[int(region/4)+1], piece)
                    if depth!=1:
                        new_utility = self.max_player(copy_board, depth-1, alpha, beta)
                    else:
                        new_utility = self.utility(copy_board)

                    if(new_utility < utility):
                        utility = new_utility
                        beta = new_utility
                    if(new_utility <= alpha):
                        return utility

        return utility


    def play(self, board):
        utility = -100000
        best_row = -1
        best_col = -1
        best_region = -1
        best_rotation = -1

        choice = ["skip", "clockwise", "anticlockwise"]
        
        valid_action = BoardUtility.get_valid_locations(board)

        alpha = -100000
        beta = 100000
        
        for action in valid_action:
            for region in range(0, 9):
                    copy_board = copy.deepcopy(board)
                    if region == 8:
                        BoardUtility.make_move(copy_board, action[0], action[1], 1, choice[0], self.piece)
                    else:
                        BoardUtility.make_move(copy_board, action[0], action[1], region%4+1, choice[int(region/4)+1], self.piece)
                    if self.depth==1:
                        new_utility = self.utility(copy_board)
                    else:
                        new_utility = self.min_player(copy_board, self.depth-1, alpha, beta)
                    if(new_utility > utility):
                        utility = new_utility
                        best_row = action[0]
                        best_col = action[1]
                        best_region = region%4+1
                        best_rotation = choice[0] if region==8 else choice[int(region/4)+1]
                        alpha = new_utility
                        
        return [[best_row, best_col], best_region, best_rotation]


class MiniMaxProbPlayer(Player):
    def __init__(self, player_piece, depth=5, prob_stochastic=0.1):
        super().__init__(player_piece)
        self.depth = depth
        self.prob_stochastic = prob_stochastic

    def horiz_score(self, board, piece, n):
        count = 0
        for c in range(COLS - n + 1):
            for r in range(ROWS):
                if (np.array_equal(np.array(board[r,c:c+n]).reshape(-1), np.array([piece for _ in range(n)]).reshape(-1))):
                    count += 1
        return count

    def vert_score(self, board, piece, n):
        count = 0
        for c in range(COLS):
            for r in range(ROWS - n + 1):
                if (np.array_equal(np.array(board[r:r+n,c]).reshape(-1),np.array([piece for _ in range(n)]).reshape(-1))):
                    count += 1

        return count

    def diag_score(self, board, piece, n):
        count = 0
        for c in range(COLS - n+1):
            for r in range(n-1, ROWS):
                board_game_status = np.array(
                    [board[r-i,c+i] for i in range(n)]).reshape(-1)
                if(np.array_equal(board_game_status ,np.array([piece for _ in range(n)]).reshape(-1))):
                    count += 1

        for c in range(n-1, COLS):
            for r in range(n-1, ROWS):
                board_game_status = np.array(
                    [board[r-i,c-i] for i in range(n)]).reshape(-1)
                if(np.array_equal(board_game_status, np.array([piece for _ in range(n)]).reshape(-1))):
                    count += 1

        return count
    
    def utility(self, board):
        piece = self.piece
        vertical_score_piece = self.vert_score(board, piece, 5)*5000 + self.vert_score(board, piece, 4)*100 + self.vert_score(board, piece, 3)*50 + self.vert_score(board, piece, 2)*10
        horizental_score_piece = self.horiz_score(board, piece, 5)*5000+self.horiz_score(board, piece, 4)*100 + self.horiz_score(board, piece, 3)*50 + self.horiz_score(board, piece, 2)*10
        diagonal_score_piece = self.diag_score(board, piece, 5)*5000 + self.diag_score(board, piece, 4)*100 + self.diag_score(board, piece, 3)*50 + self.diag_score(board, piece, 2)*10
        piece_total_score = vertical_score_piece + horizental_score_piece + diagonal_score_piece

        opponent = 1 if piece == 2 else 2

        vertical_score_opponent = self.vert_score(board, opponent, 5)*5000 + self.vert_score(board, opponent, 4)*100 + self.vert_score(board, opponent, 3)*50 + self.vert_score(board, piece, 2)*10
        horizental_score_opponent = self.horiz_score(board, opponent, 5)*5000 + self.horiz_score(board, opponent, 4)*100 + self.horiz_score(board, opponent, 3)*50 + self.horiz_score(board, piece, 2)*10
        diagonal_score_opponent = self.diag_score(board, opponent, 5)*5000 + self.diag_score(board, opponent, 4)*100 + self.diag_score(board, opponent, 3)*50 + self.diag_score(board, piece, 2)*10
        opponent_score = vertical_score_opponent + horizental_score_opponent + diagonal_score_opponent

        return piece_total_score - opponent_score
    
    def max_player(self, board, depth, alpha, beta):
        utility = -100000
        if BoardUtility.is_terminal_state(board) : return self.utility(board)
        choice = ["skip", "clockwise", "anticlockwise"]
        valid_action = BoardUtility.get_valid_locations(board)
        
        for action in valid_action:
            for region in range(0, 9):
                    copy_board = copy.deepcopy(board)
                    if region == 8:
                        BoardUtility.make_move(copy_board, action[0], action[1], 1, choice[0], self.piece)
                    else:
                        BoardUtility.make_move(copy_board, action[0], action[1], region%4+1, choice[int(region/4)+1], self.piece)
                    if depth!=1:
                        new_utility = self.min_player(copy_board, depth-1)
                    else:
                        new_utility = self.utility(copy_board)

                    if(new_utility > utility):
                        utility = new_utility
                        alpha = new_utility
                    if(new_utility >= beta):
                        return utility
                    
        return utility
    

    def min_player(self, board, depth, alpha, beta):
        utility = 100000
        if BoardUtility.is_terminal_state(board) : return self.utility(board)
        choice = ["skip", "clockwise", "anticlockwise"]
        valid_action = BoardUtility.get_valid_locations(board)

        for action in valid_action:
            for region in range(0, 9):
                    copy_board = copy.deepcopy(board)
                    if self.piece==1 : piece=2
                    else : piece = 1
                    if region == 8:
                        BoardUtility.make_move(copy_board, action[0], action[1], 1, choice[0], piece)
                    else:
                        BoardUtility.make_move(copy_board, action[0], action[1], region%4+1, choice[int(region/4)+1], piece)
                    if depth!=1:
                        new_utility = self.max_player(copy_board, depth-1, alpha, beta)
                    else:
                        new_utility = self.utility(copy_board)

                    if(new_utility < utility):
                        utility = new_utility
                        beta = new_utility
                    if(new_utility <= alpha):
                        return utility

        return utility


    def play(self, board):
        utility = -100000
        best_row = -1
        best_col = -1
        best_region = -1
        best_rotation = -1

        if(random.random() < self.prob_stochastic):
            return [random.choice(BoardUtility.get_valid_locations(board)), random.choice([1, 2, 3, 4]), random.choice(["skip", "clockwise", "anticlockwise"])]

        choice = ["skip", "clockwise", "anticlockwise"]
        
        valid_action = BoardUtility.get_valid_locations(board)

        alpha = -100000
        beta = 100000
        
        for action in valid_action:
            for region in range(0, 9):
                    copy_board = copy.deepcopy(board)
                    if region == 8:
                        BoardUtility.make_move(copy_board, action[0], action[1], 1, choice[0], self.piece)
                    else:
                        BoardUtility.make_move(copy_board, action[0], action[1], region%4+1, choice[int(region/4)+1], self.piece)
                    if self.depth==1:
                        new_utility = self.utility(copy_board)
                    else:
                        new_utility = self.min_player(copy_board, self.depth-1, alpha, beta)
                    if(new_utility > utility):
                        utility = new_utility
                        best_row = action[0]
                        best_col = action[1]
                        best_region = region%4+1
                        best_rotation = choice[0] if region==8 else choice[int(region/4)+1]
                        alpha = new_utility
                        
        return [[best_row, best_col], best_region, best_rotation]
