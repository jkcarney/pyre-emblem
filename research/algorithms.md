# Algorithm Justification

The Pyre Emblem agents utilize a mixture of reinforcement learning and search heuristics to play Fire Emblem. This document looks to explain and justify why certain algorithms are used within the source code. Many of these will be found in the `unit.py` source file, which acts as an agent and data member within the game.

---

## Reinforcement Learning

To determine action selection (Wait, Item, Attack), the agent utilizes Q-Learning and a Q-Table. This Q-Table is filled out by playing ~100,000 games against a "dumb" AI that is hard coded and does not learn (in order to best simulate the Fire Emblem environment)

### Reward Table

The environment gives the agent rewards after each action. The rewards are on a per-unit basis. (This table is subject to change. A lot.)

| Description | Reward | Notes
| --- | --- | --- 
| Dying (non-terminal) | -50.0 | Death of a nonterminal unit is extremely bad
| Dying (terminal) | -75.0 | Death of a terminal unit is worse; it causes the episode to immediately ends.
| Killing an enemy | 5.0 | Killing an enemy advances the objective (kill all enemies)
| Unit chooses Wait | 0.5 | Although waiting does not advance the objective in most cases, not dying is still good (and at that point we can rely on the heuristic to place the unit best)
| Healing self with Item | See note | Reward is directly proportional to how much healing the user obtained from using their item. For example, if Oswin at 20 / 25 HP uses a vulnerary (heals 10 HP), Oswin will receive a reward of 5. If Hector at 3 / 25 HP uses an elixer (full heal), Hector will receive a reward of 22. 

### State-Action Space Representation

Q-Learning is the collection of state-action pairs. We can view this as a table with different dimensions for each state-action pair possible. 

**Action Space** -> The agent can either Wait, use an Item, or Attack. Therefore our action space is simply [0, 3)

```python 
self.action_space = np.array([3])
```

**State Space** -> The agent looks at two dimensions as it's state. (subject to change)

- E : How many enemy units could attack this unit if they wanted to. This is a range [0 to 10)
- N : This unit's health percentage in increments of 10% encoded as an integer. For example, 91% - 100% HP is 9, 81% - 90% is 8, etc. This is also in range [0 to 10) 

```python 
self.state_space = np.array([10, 10])
```

The Q-Table is simply the concatenation of these dimensions:

```python
self.q_table = np.zeros(np.concatenate((self.state_space, self.action_space)))  # [10, 10, 3]
```

### Q-Learning

Agents learn with greedy-Q. <sub>[1]</sub> This means they do not consider previous actions when updating their table's q-values. This is subject to change; this approach was simply chosen for now because it is easy to implement.

| Parameter | Description |
| ----- | ----- |
| a | The action we took |
| s<sub>t</sub> | The state we were in BEFORE we took action *a* |
| s<sub>t + 1</sub> | The state we were in AFTER we took action *a* (next state)|
| R | The reward the agent received from the environment |
| α | Tunable hyperparameter alpha; learning rate |
| γ | Tunable hyperparameter gamma; decay rate | 
| Q(s<sub>t</sub>, a) | The q-value given state we were in and action we took |
| max(Q(s<sub>t + 1</sub>)) | The highest Q-Value given next state (this is what makes it Q-Learning as opposed to something like sarsa) |

<b><p align="center">Q(s<sub>t</sub>, a) = Q(s<sub>t</sub>, a) + α[R + γ max(Q(s<sub>t + 1</sub>)) - Q(s<sub>t</sub>, a)]</b>

---

## Heuristics

### Combat Heuristics 

Once an agent has determined they wish to attack and have moved to a tile that maximizes a movement heuristic, we need to determine which target to attack. 

We define the "attacker" as the unit who is initiating combat. This is the unit that is seeking to maximize the heuristic. 

| Attacker Stats | Defender Stats | Values Range | Description |
| ---- | ---- | ---- | ---- |
| h<sub>a</sub> | h<sub>d</sub> | [0.0 - 1.0] | The percent chance for the unit to hit the other unit with their attack. |
| m<sub>a</sub> | m<sub>d</sub> | an int | How much damage this unit will do to the other unit if their attack lands |
| c<sub>a</sub> | c<sub>d</sub> | [0.0 - 1.0] | The percent chance for the unit deal a critical hit (x3 might) |
| d<sub>a</sub> | d<sub>d</sub> | 1 (True) or 0 (False) | Whether or not the unit will hit the other unit twice or not.  |

| Hyperparameter | Value Range | Description |
| ----- | ----- | ----- |
| τ (tau) | [0.0 - 1.0] | How much do we value the defender's combat stats compared to the attackers. Values closer to 0.0 mean we do not care at all what the enemy's combat stats are against us (agent is aggressive and greedy at the potential expense of their own health). Values closer to 1.0 mean we value enemy combat stats exactly the same as we value our own (agent is conservative and very cautious about enemy attack stats).

Given these parameters, the heuristic for combat is:


<b><p align="center">H<sub>a,d</sub> = (d<sub>a</sub> + 1) (m<sub>a</sub>h<sub>a</sub> + m<sub>a</sub>c<sub>a</sub>) - τ [(d<sub>a</sub> + 1) (m<sub>d</sub>h<sub>d</sub> + m<sub>d</sub>c<sub>d</sub>)]</p></b>

### Movement Heuristics 

Once an action has been determined from the Q-Table, we need to determine which tile to move to based on some heuristic

Which tile to move to cannot be a part of the reinforcement learning process, and must instead be a heuristic. There are a few reasons for this:

- If we were to consider the tiles to move to as part of the action set, our action space would grow exponentially. For example, if we consider the max size of the game can have a tile map of size 30 x 30, and 30 x 30 tiles we can execute our action on, then the size of our action space would grow to 30<sup>4</sup> * 3 (2,430,000). Multiply that by the state space (10 * 10 = 100) to get 2,430,000 * 100 = 243,000,000 state-action pairs. This is a massive problem in a few ways:
  - Memory considerations; A test of this with NumPy, creating a 2,430,000 * 100 matrix of floats (ignoring how long this operation takes, which was a while), is roughly ***10 GB*** in size. Also consider this is a q-table on a per unit basis. 
  - Sampling size; Filling a 2,430,000 * 100 matrix with q-values would take an infeasible amount of computational power and time. There are not enough simulations you could do to fill up the matrix with values in a reasonable manner before learning occurs.
- Besides all this, *there is nothing to learn from the grid anyways*. The grid changes randomly on a per game basis, so getting a good reward from tile 2,4 and choosing attack on tile 2,5 in one game doesn't mean you will get the same reward for choosing the same action the next game; the tiles you're standing on may be completely different; the unit you're attacking may be completely different, which would lead to massively inconsistent rewards and confusion with learning. 

Because of this, it's much better to use reinforcement learning for action selection and pure heuristics for target/tile selection. 

What is interesting about the movement heuristic is that it can change depending on the HP percent of the unit. If they're at low HP, a tile that is close to the enemy must be way less valuable than a tile that is farther away from the enemy. The formula must reflect this in some way. 

| Variable | Values Range | Description |
| --- | ---- | ---- |
| e<sub>d<sub>c</sub></sub>| a positive int | The manhattan distance of the closest enemy unit at the current tile the unit is standing at|
| e<sub>d<sub>xy</sub></sub>| a positive int | The manhattan distance of the closest enemy unit at the x, y coordinate we are executing the heuristic for|
| h | [0.0, 1.0] | The percentage of the current unit's HP |
| d<sub>xy</sub> | a positive int | The defense granted to this unit at tile x, y |
| a<sub>xy</sub> | [0.0, 1.0] | Avoidance granted to this unit at tile x, y |

| Hyperparameter | Value Range | Description |
| ----- | ----- | ----- |
| Ζ (zeta) | [0.0 - 1.0] | A threshold that is considered "low" HP percentage for the unit
| φ (phi) | an int | How much the unit values tiles that grant terrain bonuses

Given these parameters, the heuristic for tiles is:


<b><p align="center">H<sub>x,y</sub> = (e<sub>d<sub>c</sub></sub> - e<sub>d<sub>xy</sub></sub>)(h - Z) + φd<sub>xy</sub>a<sub>xy</sub>

### References

---

[1] - Richard S. Sutton and Andrew G. Barto. 2018. Reinforcement Learning: An Introduction. A Bradford Book, Cambridge, MA, USA.
