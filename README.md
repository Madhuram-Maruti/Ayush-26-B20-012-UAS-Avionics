# Ayush-26-B20-012-UAS-Avionics

1. **Daily Work Log**
	•	Sept 3, 2026: I started out by reading basic Python concepts like variables and lists, and then I searched online with AI tools to understand what path planning means and how the A* algorithm finds paths in a grid. 
	•	Sept 4, 2026: I spent time learning how Python handles data structures like queues and dictionaries, and I studied the simple math behind A* which uses f(n) = g(n) + h(n) to choose the best direction while moving up, down, left, or right. 
	•	Sept 5, 2026: I put together the main Python code with help from AI, and after fixing a read-only file saving error on my Mac Air terminal, I ran all 5 test cases to generate map pictures, terminal logs, and checked how every part works. 
2. **How A* Works**
The A* algorithm is basically like a smart GPS that finds the shortest path through a maze without getting lost, and it decides which step to take next by using a simple score formula:
           Total Score = Steps Taken + Estimated Steps Left
	•	Steps Taken (g): This counts the exact number of steps walked from the starting point, where every step to a neighboring block counts as 1. 
	•	Estimated Steps Left (h): This uses Manhattan distance, which just counts how many grid blocks away the goal is without moving diagonally, giving a fast guess. 
	•	Total Score (f): The algorithm always picks the grid square with the lowest total score, so it moves towards the goal fast instead of guessing randomly. 
3. **What Happened in the 5 Tests**
	•	Test Case 1: The drone found a quick path around the central wall in 14 steps after checking 57 spots. 
	•	Test Case 2: The grid had two open sides around a middle wall, and the code checked both before picking an optimal 12-step path.
	•	Test Case 3: The grid had a narrow gap, and the code successfully squeezed through the opening in 18 steps.
	•	Test Case 4: The map had scattered wall blocks everywhere, but the algorithm maneuvered through the blocks in 30 steps.
	•	Test Case 5: A solid wall completely blocked the target, so the code safely stopped after checking all open spots and reported that no path exists. 
4. **Main Things I Learned**
I learned how Python uses coordinate pairs to move through grids, how priority queues help algorithms pick the smartest path first, and how fixing file paths in Mac terminal lets Python automatically save map images and log reports directly to the Desktop.
