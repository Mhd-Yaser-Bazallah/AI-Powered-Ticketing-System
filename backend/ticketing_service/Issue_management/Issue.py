from .States import state_mapping

class Issue:
    def __init__(self, state_name: str):
        if state_name not in state_mapping:
            raise ValueError(f"Invalid state: {state_name}")
        self.current_state_name = state_name

    def change_state(self) -> str:
       
        try:
            current_state = state_mapping[self.current_state_name]
            next_state_name = current_state.get_next_state()
            return next_state_name
        except Exception as e:
            raise
