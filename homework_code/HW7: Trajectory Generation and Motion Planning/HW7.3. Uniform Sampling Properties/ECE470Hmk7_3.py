# AUTHOR: Ralph Balita
import numpy as np

# ========== QUESTION: ==========
# The schematic of a configuration space with several rectangular obstacles (black shapes) can be seen above.
# Imagine we are creating a sampling-based motion planner, and we are using the following algorithm to choose samples. 
# First, our algorithm chooses a random sample point in the configuration space, uniformly at random from C = [0, 10] x [0, 10]. 
# Then, the algorithm checks if the sample point is inside of an obstacle, and discards it if so. 
# If the point is not inside an obstacle, the algorithm uses the random sample to grow the planner's roadmap/tree.


# ====== Enter INPUT HERE =======
hallway = np.array([[3, 3], [6, 3], [6, 4], [3, 4]])
obs1 = np.array([[0, 0], [6, 0], [6, 3], [0, 3]])
obs2 = np.array([[3, 4], [9, 4], [9, 7], [3, 7]])

# =========== ANSWER ============
# Using this sampling approach, as the number of samples we choose approaches infinity, 
# what fraction of these samples would we expect to be in the yellow highlighted region (the "hallway")?

# ============ CODE =============
