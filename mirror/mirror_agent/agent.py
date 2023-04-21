from mirror.mirror_agent.agents.ChatConversationalWithTools import build_agent as ChatConversationalWithTools

def load_mirror_agent(mirror_name, architecture, tools, data_path, voice_out, voice_id):
    """Loads the mirror agent from the given architecture and data path.

    Args:
        name (str): Name of the mirror agent.
        architecture (str): Name of the mirror agent architecture.
        data_path (str): Path to the data.
        voice_out (bool): Boolean flag to use text-to-speech on Mirror output.
        voice_id (str): Voice ID to use for text-to-speech on Mirror output.

    Returns:
        MirrorAgent: Mirror agent, which can be any Agent that conforms to the langchain
            Agent interface.
    """
    agent_map = {
        "default": ChatConversationalWithTools,
    }
    if architecture in agent_map:
        return agent_map[architecture](mirror_name, tools, data_path, voice_out, voice_id)
    else:
        raise ValueError(f"Architecture not supported: {architecture}\nSupported Architectures: {agent_map.keys}\n")