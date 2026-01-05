import React, { useEffect, useState } from "react";
import KanbanBoard from "./Index";
import { APIInstance } from "../../services/APIs/Ticket";
import AddTicketButton from "./Add";
import { useLocation } from "react-router-dom";

const Ticket: React.FC = () => {
    const [tickets, setTickets] = useState<any[]>([]);
    const location = useLocation();
    const handleTicketUpdate = (updatedTicket: any) => {
        if (!updatedTicket?.id) return;
        setTickets((prevTickets) =>
            prevTickets.map((ticket) =>
                ticket.id === updatedTicket.id ? { ...ticket, ...updatedTicket } : ticket
            )
        );
    };
    const fetchTickets = async () => {
        const userId: any = sessionStorage.getItem("id");
        const companyId: any = sessionStorage.getItem("company_id");
        const userRole: any = sessionStorage.getItem("role");
        const teamID: any = sessionStorage.getItem('team_id')
        if (!userId || !userRole) return;

        try {
            let fetchedTickets;

            switch (userRole) {
                case "client":
                    fetchedTickets = await APIInstance.UserTicket(userId);
                    break;

                case "support_team_manager":
                    fetchedTickets = await APIInstance.STMTicket(companyId);
                    break;

                case "support_team_member":
                    if (location.pathname === "/team-ticket") {
                        fetchedTickets = await APIInstance.TTicket(teamID);
                    } else {
                        fetchedTickets = await APIInstance.MemberTicket(userId);
                    }
                    break;
                default:
                    console.warn("Unhandled user role:", userRole);
                    return;
            }

            if (fetchedTickets) {
                setTickets(fetchedTickets?.data?.results || []);
            }
            console.log(fetchedTickets);
        } catch (error) {
            console.error("Error fetching tickets:", error);
        }
    };
    
    useEffect(() => {
        fetchTickets();
    }, [location]);

    return (
        <div>
            {sessionStorage.getItem("role") === "client" && <AddTicketButton />}
            <KanbanBoard fakeTickets={tickets} onTicketUpdate={handleTicketUpdate} />
        </div>
    );
};

export default Ticket;
