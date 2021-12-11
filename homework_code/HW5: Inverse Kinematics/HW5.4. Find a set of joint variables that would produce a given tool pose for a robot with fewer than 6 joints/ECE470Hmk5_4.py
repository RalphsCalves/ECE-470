# AUTHOR: Ralph Balita
import numpy as np

# ========== QUESTION: ==========
# The schematic of a robot with 2 joints (in the zero position) is shown above. 
# Frame 0 is fixed to the base. Frame 1 is fixed to the tool. 
# The homogeneous transformation matrix  and the matrix of spatial screw axes [S]
# that describe the forward kinematics of the robot are as follows. Find a set of joint variables [theta]
# that would result in the given pose T_01

# ====== Enter INPUT HERE =======
T_1in0 = np.array([[0.26720625, 0.95606020, 0.12062220, -1.68603432], 
                   [-0.96363936, 0.26510464, 0.03344717, -0.46751817], 
                   [0.00000000, -0.12517359, 0.99213486, 5.98426971], 
                   [0.00000000, 0.00000000, 0.00000000, 1.00000000]])
M = np.array([[0.00000000, 1.00000000, 0.00000000, -2.00000000], 
              [-1.00000000, 0.00000000, 0.00000000, 0.00000000], 
              [0.00000000, 0.00000000, 1.00000000, 6.00000000], 
              [0.00000000, 0.00000000, 0.00000000, 1.00000000]])
S = np.array([[0.00000000, 0.00000000], [0.00000000, 1.00000000], 
              [1.00000000, 0.00000000], [0.00000000, -4.00000000], 
              [0.00000000, 0.00000000], [0.00000000, -2.00000000]])

# =========== ANSWER ============
# Find a set of joint variables theta that would result in the given pose T_01
# Your answer will be marked correct if and only if the spatial twist required to 
# align the pose produced by  with the given pose in one second has norm less than 0.01.

# ============ CODE =============
