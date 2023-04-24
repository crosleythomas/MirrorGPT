# Imports
import argparse
from interview_agent.agent import InterviewAgent

# Argument Parsing
parser = argparse.ArgumentParser(description='Teach a mirror agent')
parser.add_argument('-n', '--mirror-name', type=str, default='default', help='Name of this mirror')
parser.add_argument('-t', '--topic', type=str, default='food', help='Topic to learn about')
parser.add_argument('-a', '--agent', type=str, default='default', help='Interview Agent type to use')

# Run the agent
if __name__ == '__main__':
    raise NotImplementedError("Coming soon!")
    # args = parser.parse_args()
    # interview_agent = InterviewAgent(
    #     agent=args.agent,
    #     mirror_name=args.mirror_name,
    #     topic=args.topic,
    # )
    # interview_agent.run()
