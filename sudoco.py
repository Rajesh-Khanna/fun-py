import os
import copy
def print_board(b):
    k=0
    for i in b:
        print(' '.join((i[:3]))+'  '+' '.join(i[3:6])+'  '+' '.join(i[6:9]))
        k+=1
        if(k%3==0):
            print(' ')
    return

def check_row(board,r,e):
	for i in board[r]:
		if(e==i):
			return False
	return True

def check_col(board,c,e):
	for i in range(9):
		if(board[i][c] == e):
			return False
	return True

def check_sq(board,r,c,e):
	for i in range(int(r/3)*3,int(r/3)*3 + 3):
		for j in range(int(c/3)*3,int(c/3)*3 + 3):
			if(board[i][j] == e):
				return  False
	return True
def fill_board(board):
	count = 81
	pc = 0
	check = 0
	test = [['0']*9]*9
	temp = [[[]]*9 for _ in range(9)]
	while(count != 0):
		count = 81
		for i in range(9):
			for j in range(9):
				if(board[i][j] == '0'):
					for x in range(1,10):
						if(check_row(board,i,str(x)) and check_col(board,j,str(x)) and check_sq(board,i,j,str(x))):
							temp[i][j].append(x)
					if(len(temp[i][j]) == 0):
						return None
					elif(len(temp[i][j]) == 1):
						board[i][j] = str(temp[i][j][0])
						count -= 1
					elif(len(temp[i][j]) >= 2  and check == 1):
						for el in temp[i][j]:
							test = copy.deepcopy(board)
							test[i][j] = str(el)
							test = fill_board(test)
							if(test != None):
								return test
						return None
				else:
					count -= 1
				temp[i][j][:] = []
		if(pc == count):
			check = 1
		pc = count
	return board
board = []
for i in range(9) :
	board.append(input().split(' '))	
print(board)
print('question board')
print_board(board)
print('Completed Board')
print_board(fill_board(board))