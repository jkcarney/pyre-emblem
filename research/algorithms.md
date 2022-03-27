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

Agents learn with greedy-Q. This means they do not consider previous actions when updating their table's q-values. This is subject to change; this approach was simply chosen for now because it is easy to implement.

| Parameter | Description |
| ----- | ----- |
| a | The action we took |
| s<sub>t</sub> | The state we were in BEFORE we took action *a* |
| s<sub>t + 1</sub> | The state we were in AFTER we took action *a* (next state)|
| R | The reward the agent received from the environment |
| α | Tunable hyperparameter alpha; learning rate |
| γ | Tunable hyperparameter gamma; decay rate | 
| Q(s<sub>t</sub>, a) | The q-value given state we were in and action we took |
| max(Q(s<sub>t + 1</sub>, )) | The highest Q-Value given next state (this is what makes it Q-Learning as opposed to something like sarsa) |

<b><p align="center">Q(s,a) = Q(s,a) + α[R + γ max(Q(s<sub>t + 1</sub>, )) - Q(s,a)]</p></b>

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
| d<sub>a</sub> | d<sub>d</sub> | 1 (True) or 1/2 (False) | Whether or not the unit will hit the other unit twice or not.  |

| Hyperparameter | Value Range | Description |
| ----- | ----- | ----- |
| τ (tau) | [0.0 - 1.0] | How much do we value the defender's combat stats compared to the attackers. Values closer to 0.0 mean we do not care at all what the enemy's combat stats are against us (agent is aggressive and greedy at the potential expense of their own health). Values closer to 1.0 mean we value enemy combat stats exactly the same as we value our own (agent is conservative and very cautious about enemy attack stats).

Given these parameters, the heuristic for combat is:


<b><p align="center">H<sub>a,d</sub> = 2d<sub>a</sub>(m<sub>a</sub>h<sub>a</sub> + m<sub>a</sub>c<sub>a</sub>) - τ[2d<sub>d</sub>(m<sub>d</sub>h<sub>d</sub> + m<sub>d</sub>c<sub>d</sub>)]</p></b>
