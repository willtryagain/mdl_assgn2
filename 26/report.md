# **REPORT**

**Team - 31**

**Members**

- Aman Atman(2020121006)
- Aryan Dubey(2019113014)


## Procedure of making A matrix

Each state is formed by a tuple of 5 elements <pos, mat, arrow, state, health>. 

The ranges of these elements are
- POSITIONS_RANGE = 5
- MATERIALS_RANGE = 3
- ARROWS_RANGE = 4
- MM_STATE_RANGE = 2
- MM_HEALTH_RANGE = 5

Thus total 600 states are possible. We iterate over each state. For each state we go over all possible actions. As self looping is not allowed the A[state][action] will be one. For transitions out of this state we subtract the probability from the states on the other side of transition.   

## Procedure of finding the policy
- ***A*** represents the flow of probabilities of valid actions from each state.
- Reward vector ***R*** represents the expected reward for action-state pair.
- ***X_{ia}*** represents the expected number of times action `a` has is taken in state `i`.
- ***alpha*** holds the initial probabilities of states. We start at the state `(C, 2, 3, R, 100)`.

 The LPP is to 
```
    max(rx) | Ax = alpha, x >= 0
```
After obtaining X using the solver, we iterate over all the states. 
- For each state, we go over all the actions possible in that state.
- We find the action which corresponds to the highest value in ***X***.

## Can there be multiple policies?

Yes there can be multiple policies. It is because different actions could lead to same utility i.e all actions having same value of X can be interchanged. 

- We could permute the order of actions and obtain different policies.

- While could traverse the X in reverse direction to obtain the last optimum action. Currently argmax function reports the first occurence.

### A matrix 
A matrix would not get changed if we only make changes to the way we select best action. However on permuting the actions the A matrix will also get changed.
### R vector
The R vector remains unchanged. This is because the rewards are unchanged. 
### alpha vector
The alpha vector remains unchanged. It is because even on changing the order of processing action the initial assigned probabilities to states won't change. 
### X vector
As it is built for a given action order changing that will also change X. Similar to alpha it would be unaffected if just the order of processing action changes.


