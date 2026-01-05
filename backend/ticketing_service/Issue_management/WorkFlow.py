                                                     


class WorkFlow:     
    state_map = {
        "open": "Assign to Team",
        "Assign to Team": "Assign to Member",
        "Assign to Member": "In Progress",
        "In Progress": "Done",               
    }
    
    state_class_map = {
        "open": "OpenState",
        "Assign to Team": "AssignToTeamState",
        "Assign to Member": "AssignToMemberState",
        "In Progress": "InProgressState",
        "Done": "DoneState",
    }

    def next_state(self, current_state):  
        return self.state_map.get(current_state)

    def get_state_class(self, state):
        return self.state_class_map.get(state)
