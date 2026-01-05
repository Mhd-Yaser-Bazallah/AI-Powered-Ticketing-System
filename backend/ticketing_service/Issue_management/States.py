from abc import ABC, abstractmethod
from .WorkFlow import WorkFlow

class IState(ABC):
    @abstractmethod
    def get_next_state(self) -> str:
        pass



class OpenState(IState):
    def get_next_state(self) -> str:
        return "Assign to Team"




class AssignToTeamState(IState):
    def get_next_state(self) -> str:
        return "Assign to Member"



class AssignToMemberState(IState):
    def get_next_state(self) -> str:
        return "In Progress"



class InProgressState(IState):
    def get_next_state(self) -> str:
        return "Done"



class DoneState(IState):
    def get_next_state(self) -> str:
        raise Exception("Done is the final state. No further states.")



state_mapping = {
    "open": OpenState(),
    "Assign to Team": AssignToTeamState(),
    "Assign to Member": AssignToMemberState(),
    "In Progress": InProgressState(),
    "Done": DoneState(),
}



