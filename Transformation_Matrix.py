import numpy as np
import sys
from math import pi
from scipy.linalg import expm, sinm, cosm

# for UR3 Robot
def Get_MS():
    
    # omega (angular vel) (direction of rotation)
    # w = 0,0,0 if prismatic joint
    # w = x,y,z if revolute joint
    w_1 = np.array([0,0,1]).T
    w_2 = np.array([0,0,0]).T
    w_3 = np.array([0,1,0]).T
    w_4 = np.array([0,0,-1]).T
    w_5 = np.array([-1,0,0]).T
    
#==============================================
# IF YOU WOULD LIKE TO USE (q), UNCOMMENT 
# THIS SECTION AND COMMENT OUT THE (v) SECTION
#==============================================    
#     q_1 = np.array([-0.150, 0.150, 0.162]).T
#     q_2 = np.array([-0.150, 0.270, 0.162]).T
#     q_3 = np.array([ 0.094, 0.270, 0.162]).T
#     q_4 = np.array([ 0.307, 0.177, 0.162]).T
#     q_5 = np.array([ 0.307, 0.260, 0.162]).T
#     q_6 = np.array([ 0.390, 0.260, 0.162]).T

#     v_1 = np.cross(w_1, (-1*q_1))
#     v_2 = np.cross(w_2, (-1*q_2))
#     v_3 = np.cross(w_3, (-1*q_3))
#     v_4 = np.cross(w_4, (-1*q_4))
#     v_5 = np.cross(w_5, (-1*q_5))
#     v_6 = np.cross(w_6, (-1*q_6))
#=============================================
   
    # v (linear velocity) (
    # v = x(1),y(1),z(1) in direction of prismatic
    # v = w x (-q) if revolute joint, q = center of space frame (to) -> center of joint
    v_1 = np.array([-2,0,0]).T
    v_2 = np.array([-1,0,0]).T
    v_3 = np.array([2,0,0]).T
    v_4 = np.array([0,0,0]).T
    v_5 = np.array([0,6,-4]).T

    # screw matrices using get_S
    S_1 = get_S(w_1.T,v_1.T)
    S_2 = get_S(w_2.T,v_2.T)
    S_3 = get_S(w_3.T,v_3.T)
    S_4 = get_S(w_4.T,v_4.T)
    S_5 = get_S(w_5.T,v_5.T)
    
    S = np.array([S_1,S_2,S_3,S_4,S_5])

    M = np.array([[0, 0, 1, 0],
                  [0, -1, 0, -6],
                  [1, 0, 0, -6],
                  [0, 0, 0, 1]])

    return M, S

def get_S(w, v):
    return np.array([[      0, -1*w[2],    w[1], v[0]],
                     [   w[2],       0, -1*w[0], v[1]],
                     [-1*w[1],    w[0],       0, v[2]],
                     [      0,       0,       0,    0]])

def main():
    
    # given set of theta angles, one can find the transformation matrix by the following algo
    theta = np.array([[0.59, 0.02, 0.39, 0.36, -0.53]]).T
    
    M,S = Get_MS()
    T = M
    
    # idx 4-0, step by -1
    for i in range(4, -1, -1):
        T = np.matmul(expm(S[i]*theta[i]), T)
        
    print(str(T) + "\n")

if __name__ == "__main__":
    main() 
