
from collections import defaultdict

def PIECE(N, P,Q):

  Px,Py,Pz = P
  Qx,Qy,Qz = Q

  Vx,Vy = Qx-Px,Qy-Py
  Wx,Wy = Py-Qy,Qx-Px
    
  assert((Px == Qx or Py == Qy) and Pz == Qz)
  assert(abs(Px-Qx) <= 1 and abs(Py-Qy) <= 1)

  if N == 5: return ((Px,Py,Pz),(Qx,Qy,Qz),(Px,Py,-Pz),(Qx,Qy,-Qz))
  if N == 4: return ((Px,Py,Pz),(Qx,Qy,Qz),(Px,Py,-Pz),(Qx,Qy,-Qz),
                     (Qx+Vx,Qy+Vy,-Qz)) 
  if N == 3: return ((Px,Py,Pz),(Qx,Qy,Qz),(Qx,Qy,-Qz),(Px,Py,-Pz),
                     (Px+Wx,Py+Wy,-Pz))
  if N == 2: return ((Px,Py,Pz),(Qx,Qy,Qz),(Px,Py,-Pz),(Qx,Qy,-Qz),
                     (Qx+Wx,Qy+Wy,-Qz))
  if N == 1: return ((Px,Py,Pz),(Qx,Qy,Qz),(Px,Py,-Pz),(Px+Wx,Py+Wy,-Pz),
                     (Qx+Wx,Qy+Wy,-Qz),(Qx,Qy,-Qz))
  if N == 0: return ((Px,Py,Pz),(Qx,Qy,Qz),(Px,Py,-Pz),(Qx,Qy,-Qz),
                     (Qx+Vx,Qy+Vy,-Qz),(Qx+Vx+Wx,Qy+Vy+Wy,-Qz))
  return None
  
def DRAW(PIECES):
    
  BOARD = [[[None for z in range(3)] for j in range(4)] for i in range(4)]
  T = [list("┌───────────────┐   ┌───────────────┐"),
       list("│   │   │   │   │   │   │   │   │   │"),
       list("│─── ─── ─── ───│   │─── ─── ─── ───│"),
       list("│   │   │   │   │   │   │ █ │   │   │"),
       list("│─── ─── ─── ───│   │─── ─── ─── ───│"),
       list("│   │   │   │   │   │   │   │   │   │"),
       list("│─── ─── ─── ───│   │─── ─── ─── ───│"),
       list("│   │   │   │   │   │   │   │   │   │"),
       list("└───────────────┘   └───────────────┘")]
  
  for n,piece in enumerate(PIECES):
    for x,y,z in piece: BOARD[x][y][z] = n
  
  for x,y,z in PIECES[0][:2]:
    T[2*y+1][4*x+10*z+12] = "●"

  for piece in PIECES[1:6]:
    for x,y,z in piece[:2]:
      T[2*y+1][4*x+10*z+12] = "O"

  for piece in PIECES:
    for i,j in ((0,1),(2,3),(3,4),(4,5)):
      if j < len(piece): 
        x,y,z = piece[i]
        X,Y,Z = piece[j]                
        if x == X:
          T[2*min(y,Y)+2][4*x+11+10*z] = " "
          T[2*min(y,Y)+2][4*x+12+10*z] = " "
          T[2*min(y,Y)+2][4*x+13+10*z] = " "
        if y == Y:
           T[2*y+1][4*min(x,X)+14+10*z] = " "
        
  for row in T: print("".join(row))
  print("\n")

def SEARCH(PIECES=[]):
  
  if len(PIECES) == 6: 
    if (PIECES[0][0][2] == 1 and PIECES[0][0][0] <= PIECES[0][1][0] 
                             and PIECES[0][0][1] <= PIECES[0][1][1]):
      yield tuple(PIECES)
  
  else:
    
    BOARD = [[[1 for z in range(3)] for j in range(4)] for i in range(4)]
    BOARD[1][1][1] = 0
    
    for piece in PIECES:
      for x,y,z in piece: 
        BOARD[x][y][z] = 0
    
    for i in range(4):
      for j in range(3):
        for k in (-1,1):

          NEW = PIECE(len(PIECES),(i,j,k),(i,j+1,k))
          if all(0<=x<=3 and 0<=y<=3 and BOARD[x][y][z] for x,y,z in NEW):
            yield from SEARCH([NEW]+PIECES)

          NEW = PIECE(len(PIECES),(i,j+1,k),(i,j,k))
          if all(0<=x<=3 and 0<=y<=3 and BOARD[x][y][z] for x,y,z in NEW):
            yield from SEARCH([NEW]+PIECES)

          NEW = PIECE(len(PIECES),(j,i,k),(j+1,i,k))
          if all(0<=x<=3 and 0<=y<=3 and BOARD[x][y][z] for x,y,z in NEW):
            yield from SEARCH([NEW]+PIECES)

          NEW = PIECE(len(PIECES),(j+1,i,k),(j,i,k))
          if all(0<=x<=3 and 0<=y<=3 and BOARD[x][y][z] for x,y,z in NEW):
            yield from SEARCH([NEW]+PIECES)

if __name__ == "__main__":
  
  SOLUTIONS = defaultdict(list)
  for PIECES in SEARCH(): SOLUTIONS[(PIECES[0],)].append(PIECES)
  
  for KEY in sorted(SOLUTIONS.keys()):
    DRAW(KEY)
    for solution in SOLUTIONS[KEY]: DRAW(solution)
