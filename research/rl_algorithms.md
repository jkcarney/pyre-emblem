# Enviornment

> "god punished me by giving an important RL component the name 'environment' when i cannot f****** spell enviornment to save my life"
> 
-me, 2022

---

In the context of reinforcement learning and Finite Markov Decision Processes, (MDPs) the **environment** is defined as the thing that interacts with an agent and is comprised of everything outside said agent. The agent and the enviornment interact continually; the agent selects an action, the enviornment responds and presents a new situation to the agent. The enviornment also gives rise to rewards, which the agent seeks to maximize over time through its actions. <sub>[1]</sub>

We need to translate our environment, the Fire Emblem game, to a universal environment that allows other RL frameworks to interact with it. Luckily, OpenAI created [OpenAI Gym](https://github.com/openai/gym), which is supported by many RL frameworks (Tensorforce, Pytorch, etc) We will be using Gym to adapt our environment

---

There are a few components of the environment that we need to keep track of that constitutes the environment of a FE game:

1. **The Map**: the tile map is core to the game. It tells units where they can stand, where they can walk, as well as stat bonuses while standing in certain tiles. While the tilemap itself does not keep track of all the units, units know where they are on the tile map (their x and y coordinates)
2. **The Blue Team**: in a Fire Emblem game, this may also be called the Player Team (which I'll just call blue team for simplification). This is the player controlled Units. This team loses either if the turn limit is reached, or any of their "teriminal units" dies. 
3. **The Red Team**: in a Fire Emblem game, this would be called the Enemy Team. This is the game controlled Units, typically controlled by an enemy AI. The AI in FE games is weak however; it does not learn and follows easily exploitable patterns. This team loses when all of their units die.
4. **The turn count**: a "Turn" is defined as both sides moving all their units (within their separate 'phases'). The turn count is important because there will be a turn limit implemented; if the turn limit goes over some constant (probably 100), then the game is an automatic loss for the blue team. 
5. **Misc**: The game also keeps track of misc things, such as which unit is next to act, which phase we are currently on (blue or red), and whether or not the blue or red team encountered their win condition. 




### References

---

[1] - Richard S. Sutton and Andrew G. Barto. 2018. Reinforcement Learning: An Introduction. A Bradford Book, Cambridge, MA, USA.