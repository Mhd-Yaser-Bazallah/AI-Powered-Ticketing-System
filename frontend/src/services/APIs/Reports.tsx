import BackendError from "../Error/Error";
import { MainMethod } from "./Main";
export default class Api {

    async Get(id: any) {
        try {
            let result: any = await MainMethod.getRequest(`analysis/analysis/${id}`)
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status, e.response.data).errorMessage();
            return message;
        }
    }


    async GetReportingTicketsStatus() {
        try {
            let result: any = await MainMethod.getRequest(`reporting/tickets/status`)
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status, e.response.data).errorMessage();
            return message;
        }
    }

    async GetReportingTicketsPriority() {
        try {
            let result: any = await MainMethod.getRequest(`reporting/tickets/priority`)
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status, e.response.data).errorMessage();
            return message;
        }
    }

    async GetReportingTeamsPerformance() {
        try {
            let result: any = await MainMethod.getRequest(`reporting/teams/performance`)
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status, e.response.data).errorMessage();
            return message;
        }
    }

    async GetReportingCompaniesTickets() {
        try {
            let result: any = await MainMethod.getRequest(`reporting/companies/tickets`)
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status, e.response.data).errorMessage();
            return message;
        }
    }
   
}
export let APIInstance = new Api();
