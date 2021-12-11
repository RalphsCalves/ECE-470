# AUTHOR: Ralph Balita
import numpy as np

# ========== QUESTION: ==========
# The schematic of a robot with 9 joints (in the zero position) is shown above. 
# Frame 0 is fixed to the base. Frame 1 is fixed to the tool. 
# The homogeneous transformation matrix  and the matrix of spatial screw axes [S]
# that describe the forward kinematics of the robot are as follows. Find a set of joint variables [theta]
# that would result in the given pose T_01

# ====== Enter INPUT HERE =======
import numpy as np

T_1in0 = np.array([[-0.84860403, -0.34524434, 0.40084603, -1.72632555], 
                   [0.11809387, 0.61495903, 0.77966610, -3.51742397], 
                   [-0.51567920, 0.70896526, -0.48108547, -1.43368217], 
                   [0.00000000, 0.00000000, 0.00000000, 1.00000000]])
M = np.array([[-1.00000000, 0.00000000, 0.00000000, 0.00000000], 
              [0.00000000, 0.00000000, 1.00000000, -4.00000000], 
              [0.00000000, 1.00000000, 0.00000000, -4.00000000], 
              [0.00000000, 0.00000000, 0.00000000, 1.00000000]])
S = np.array([[-1.00000000, -1.00000000, 0.00000000, 0.00000000, 0.00000000,  0.00000000, 0.00000000, 0.00000000, 0.00000000], 
              [0.00000000, 0.00000000, 0.00000000, 1.00000000, 0.00000000, -1.00000000,  0.00000000, 0.00000000, 0.00000000], 
              [0.00000000, 0.00000000, -1.00000000, 0.00000000, 0.00000000, 0.00000000,  0.00000000, 0.00000000, 0.00000000], 
              [0.00000000, 0.00000000, 0.00000000, 4.00000000, 0.00000000, -6.00000000,  0.00000000, -1.00000000, 0.00000000], 
              [0.00000000, 2.00000000, 0.00000000, 0.00000000, -1.00000000, 0.00000000,  -1.00000000, 0.00000000, 0.00000000], 
              [2.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000, 0.00000000,  0.00000000, 0.00000000, 1.00000000]])

# =========== ANSWER ============
# Find a set of joint variables theta that would result in the given pose T_01
# Your answer will be marked correct if and only if the spatial twist required to 
# align the pose produced by  with the given pose in one second has norm less than 0.01.

# ============ CODE =============
