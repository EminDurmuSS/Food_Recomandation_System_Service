# backend/core/utils.py

UNKNOWN_PLACEHOLDER = 'Unknown'

def create_node_label(label):
    if isinstance(label, str):
        return label.replace(" ", "_").replace("-", "_").replace(">", "").replace("<", "less_than_").strip().lower()
    return str(label)
