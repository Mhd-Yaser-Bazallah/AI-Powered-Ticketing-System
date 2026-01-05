import BackendError from "../Error/Error";
import { MainMethod } from "./Main";
export default class Api {

    async Get(pageNumber: number) {
        try {
            let result: any = await MainMethod.getRequest(`company/List?page=${pageNumber}`)
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status,e.response.data).errorMessage();
            return message;
        }
    }

    async GetAll() {
        try {
            let result: any = await MainMethod.getRequest(`company/company`)
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status,e.response.data).errorMessage();
            return message;
        }
    }

    async Add(data: any) {
        try {
            let result: any = await MainMethod.addPostRequest(`company/create`, data)
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status,e.response.data).errorMessage();
            return message;
        }
    }


    async Delete(id: any) {
        try {
            let result: any = await MainMethod.deleteRequest(`company/delete`, id, {})
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status,e.response.data).errorMessage();
            return message;
        }
    }
    async Edit(id: any, data: any) {
        try {
            let result: any = await MainMethod.putRequest(`company/update`, id, data)
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status,e.response.data).errorMessage();
            return message;
        }
    }


    async AddWorkflowDefault(data: any) {
        try {
            let result: any = await MainMethod.addPostRequest(`workflow/create-default-company`, data)
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status,e.response.data).errorMessage();
            return message;
        }
    }

    async AddWorkflow(data: any) {
        try {
            let result: any = await MainMethod.addPostRequest(`workflow/create`, data)
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status,e.response.data).errorMessage();
            return message;
        }
    }
    async toggle_auto_assign(id: any) {
        try {
            let result: any = await MainMethod.addPostRequest(`company/toggle_auto_assign/${id}/`, {})
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status,e.response.data).errorMessage();
            return message;
        }
    }
    async toggle_auto_categorize(id: any) {
        try {
            let result: any = await MainMethod.addPostRequest(`company/toggle_auto_categorize/${id}/`, {})
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status,e.response.data).errorMessage();
            return message;
        }
    }
    async toggle_auto_prioritize(id: any) {
        try {
            let result: any = await MainMethod.addPostRequest(`company/toggle_auto_prioritize/${id}/`, {})
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status,e.response.data).errorMessage();
            return message;
        }
    }
}
export let APIInstance = new Api();
