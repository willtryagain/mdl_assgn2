# **REPORT**

**Team - 31**

**Members**

- Aman Atman(2020121006)
- Aryan Dubey(2019113014)


## Task 1

### West

The dominant strategy is to move RIGHT. It could be because he can&#39;t hit and shooting probability is low and he might run out of arrows. He stays when MM is ready sometimes. He shoots only when he has 3 arrows probably because he might run out of arrows as he can&#39;t gather or craft.

### North

He tends to CRAFT when he has under 3 arrows and at least 1 material. Otherwise the dominant action is to move DOWN. It could be because staying here won&#39;t end the game.

### East

He HITs when having zero arrows, or MM has high health values. He will SHOOT when the arrows are sufficient to kill MM because of its higher accuracy.

### South

The dominant strategy is to move UP. He stays only when MM is in the ready state and has low health. It may be because he knows the game will be over soon so the penalty received on being attacked outweighs the cost of staying.

### Center

He always moves RIGHT. It could be because of having higher accuracy of hitting and shooting.

It takes 75 iterations to converge.

### Simulation

<ul> 
<li>(W,0,0,D,100):RIGHT=[-32.363]

He goes to (C,0,0,D,100) or (C,0,0,R,100).

Let us choose (C,0,0,D,100):RIGHT=[-27.391]

He goes to (E,0,0,D,100) or (E,0,0,R,100)

Let us choose (E,0,0,D,100):HIT=[-22.414]

He goes to (E,0,0,D,50) or (E,0,0,D,100) or (E,0,0,R,50) or (E,0,0,R,100)

Let us choose (E,0,0,D,50):HIT=[6.994]

He goes to (E,0,0,R,50) or (E,0,0,D,50) or (E,0,0,D,0) or (E,0,0,R,0)

Let us choose (E,0,0,R,50):HIT=[-15.503]

He goes to (E,0,0,D,75) or (E,0,0,R,50) or (E,0,0,R,0)

Let us choose (E,0,0,D,75):HIT=[-15.503]

He goes to (E,0,0,D,25) or (E,0,0,D,75) or (E,0,0,R,25) or (E,0,0,R,75)

Let us choose (E,0,0,D,25):HIT=[16.965]

He goes to (E,0,0,D,0) and the game ends.

<li> (C, 2, 0, R, 100)

(C,2,0,R,100):RIGHT=[-27.391]

He could go to (E,2,0,R,100) or (E,2,0,D,100)

Let us choose (E,2,0,R,100):HIT=[-22.414]

He could go to (E,2,0,D,50) or (E,2,0,D,100) or (E,2,0,R,50) or (E,2,0,R,100)

Let us choose (E,2,0,R,50):HIT=[-15.503]

He could go to (E,2,0,D,75) or (E,2,0,R,50) or (E,2,0,R,0)

Let us choose (E,2,0,D,75):HIT =[-15.503]

He could go to (E,2,0,D,25) or (E,2,0,D,75) or (E,2,0,R,25) or (E,2,0,R,75)

Let us choose (E,2,0,D,25):HIT=[16.965]

He goes to (E,2,0,D,0) game ends
</ul>

## Task 2

### Case 1:

Identical to Task 1. It is because IJ never chose the LEFT action in EAST state.

### Case 2:

When the step cost of STAY action is changed to 0,it takes very long time to converge.We observe that there is a very large increase in the number of iterations it took to converge. So as reflected in our trace files the instance of stay action is increasing as the penalty is getting removed.Here it stays in the west forever.

It converges in 1611 iterations

### Case 3:

Converges in 8 iterations

West

He goes right unless he has got enough arrows and MM has low health. It is because of the low accuracy of shooting.

North

He always goes down. He can then immediately hit or possibly shoot MM. It could because the agent is now myopic and less concerned about future rewards.

West

He goes right unless he has got enough arrows and MM has low health. It is because of the low accuracy of shooting.

North

He always goes down. He can immediately then hit or possibly shoot MM. It is because the agent is now myopic and less concerned about future rewards.

East

He hits whenever MM is in the ready state. It could be because MM receives more damage by hitting and the game ends faster.

South

He always goes up. Similar to the north state.

Center

He hits most of the time. SHOOT action is chosen when MM has low health and is in dormant state.