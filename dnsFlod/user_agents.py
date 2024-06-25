# user_agents.py

import random

def get_random_user_agent():
    with open('user-agents.txt', 'r') as f:
                user_agents = [line.strip() for line in f.readlines() if line.strip()]
    return random.choice(user_agents)
