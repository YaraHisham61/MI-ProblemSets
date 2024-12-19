# This file contains the options that you should modify to solve Question 2

# IMPORTANT NOTE:
# Comment your code explaining why you chose the values you chose.
# Uncommented code will be penalized.

def question2_1():
    #TODO: Choose options that would lead to the desired results 
    return {
        # Just using the same noise value as lecture example
        "noise": 0.2,

        #To encoure the agent to prioritize reaching the near terminal state (+1) quickly
        # while still considering the long-term risk of the -10 row.
        "discount_factor": 0.9,

        # '''Living reward -ve will make the agent want to end the game quickly
        # so it will risk moving beside -10 row to reach the terminal state faster
        # But if we choose a too large -ve number the agent wont care about the -10 row
        # so I'll choose a small negative number relative to the -10 reward'''

        "living_reward": -3.5
    }

def question2_2():
    #TODO: Choose options that would lead to the desired results
    return {
        # Just using the same noise value as lecture example
        "noise": 0.2,

        #To get to the near terminal state faster just make the future rewards effect less significant
        "discount_factor": 0.2, 

        # '''Making the living reward +ve will make the agent want to stay in 
        # the environment for longer so it will move away from the -10 row
        # But if we choose a too large +ve number the agent will stay in 
        # the environment forever so I'll choose a small positive number'''
        "living_reward": 0.2
    }

def question2_3():
    #TODO: Choose options that would lead to the desired results
    return {
        # Just using the same noise value as lecture example
        "noise": 0.2,
        # We don't want the agent to end quiclky so we'll set the discount factor to 1
        "discount_factor": 1,

        # '''Making the living reward -ve will make the agent want to end the game quickly
        # Setting it to -2.5 strikes a balance making the agent prioritize the shortest dangerous
        # path to the terminal state (+10), even though it involves passing close to the row of -10 states.'''
        "living_reward": -2.5
    }

def question2_4():
    #TODO: Choose options that would lead to the desired results
        return {
        # Just using the same noise value as lecture example
        "noise": 0.2,
        
        # We don't want the agent to end quiclky so we'll set the discount factor to 1
        "discount_factor": 1,

        # '''Just like in question2_3 , I'll make the living reward a small negative number
        # but I'll make it larger than the living reward in question2_3 to make the agent
        # avoid moving next to -10 row'''
        "living_reward": -0.3
    }

def question2_5():
    #TODO: Choose options that would lead to the desired results
    return {
        #Even with a large positive living reward, the agent can unintentionally enter a terminal state due to stochastic movement.
        "noise": 0,
        # The discount factor will make the effect of the living reward less significant so I'll leave it at 1
        "discount_factor": 1,
        # To make the agent continue forever in the environment, I'll make the living reward a large positive number
        "living_reward": 100
    }

def question2_6():
    #TODO: Choose options that would lead to the desired results
    return {
        #To ensure the agent follows the shortest path to a terminal state without being delayed by stochastic movements.
        "noise": 0,
        # The discount factor will make the effect of the living reward less significant so I'll leave it at 1
        "discount_factor": 1,
        # To make the agent want to reach any terminal state quickly even if it's -10 just make the reward of living is a large negative number
        "living_reward": -100
    }