import BackendError from "../Error/Error";
import { MainMethod } from "./Main";
export default class Api {

    async Get(pageNumber: number) {
        try {
            let result: any = await MainMethod.getRequest(`users/List?page=${pageNumber}`)
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status, e.response.data).errorMessage();
            return message;
        }
    }
    async WorkFlowBoard(company_id: number) {
        try {
            let result: any = await MainMethod.getRequest(`workflow/by-company?company_id=${company_id}`)
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status, e.response.data).errorMessage();
            return message;
        }
    }
    async UserTicket(id: number) {
        try {
            let result: any = await MainMethod.getRequest(`ticket/client-Tickets/${id}`)
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status, e.response.data).errorMessage();
            return message;
        }
    }
    async MemberTicket(id: number) {
        try {
            let result: any = await MainMethod.getRequest(`ticket/assign-user-Tickets/${id}`)
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status, e.response.data).errorMessage();
            return message;
        }
    }
    async STMTicket(id: number) {
        try {
            let result: any = await MainMethod.getRequest(`ticket/company-Tickets/${id}`)
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status, e.response.data).errorMessage();
            return message;
        }
    }
    async TTicket(id: number) {
        try {
            let result: any = await MainMethod.getRequest(`ticket/assign-team-Tickets/${id}`)
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status, e.response.data).errorMessage();
            return message;
        }
    }
    async TicketDetails(id: number) {
        try {
            let result: any = await MainMethod.getRequest(`ticket/${id}`)
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status, e.response.data).errorMessage();
            return message;
        }
    }
    async SolveTicket(id: number, data: any) {
        try {
            let result: any = await MainMethod.addPostRequest(`ticket/${id}/solve`, data)
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status, e.response.data).errorMessage();
            return message;
        }
    }

    async Add(data: any) {
        try {
            let result: any = await MainMethod.addPostRequest(`ticket/create`, data)
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status, e.response.data).errorMessage();
            return message;
        }
    }
    async MoveTicket(id:number,data: any) {
        try {
            let result: any = await MainMethod.addPostRequest(`ticket/${id}/advance-status`, data)
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status, e.response.data).errorMessage();
            return message;
        }
    }
    async AssginToTeam(id:number,data: any) {
        try {
            let result: any = await MainMethod.addPostRequest(`ticket/Assign-Ticket-team/${id}`, data)
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status, e.response.data).errorMessage();
            return message;
        }
    }
    async AssginToInProgress(id:number,data: any) {
        try {
            let result: any = await MainMethod.addPostRequest(`ticket/Ticket-In-Progress/${id}`, {})
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status, e.response.data).errorMessage();
            return message;
        }
    }
    async AssginToInDone(id:number,data: any) {
        try {
            let result: any = await MainMethod.addPostRequest(`ticket/Ticket-To-Done/${id}`, {})
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status, e.response.data).errorMessage();
            return message;
        }
    }
    async AssginToMe(id:number,data: any) {
        try {
            let result: any = await MainMethod.addPostRequest(`ticket/Assign-Ticket-user/${id}`, data)
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status, e.response.data).errorMessage();
            return message;
        }
    }
    async Delete(id: any) {
        try {
            let result: any = await MainMethod.deleteRequest(`ticket/delete`, id, {})
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status, e.response.data).errorMessage();
            return message;
        }
    }
    async Edit(id: any, data: any) {
        try {
            let result: any = await MainMethod.putRequest(`ticket/update`, id, data)
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status, e.response.data).errorMessage();
            return message;
        }
    }
}
export let APIInstance = new Api();
