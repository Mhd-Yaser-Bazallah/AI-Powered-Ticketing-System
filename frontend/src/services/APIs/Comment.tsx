import BackendError from "../Error/Error";
import { MainMethod } from "./Main";
export default class Api {

    async Get(id:any) {
        try {
            let result: any = await MainMethod.getRequest(`comments/commentsTicket/${id}`)
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status, e.response.data).errorMessage();
            return message;
        }
    }

    async Add(data: any) {
        try {
            let result: any = await MainMethod.addPostRequest(`comments/create`, data)
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status, e.response.data).errorMessage();
            return message;
        }
    }
    async Delete(id: any) {
        try {
            let result: any = await MainMethod.deleteRequest(`users/delete`, id, {})
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status, e.response.data).errorMessage();
            return message;
        }
    }
    async Edit(id: any, data: any) {
        try {
            let result: any = await MainMethod.putRequest(`users/update`, id, data)
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status, e.response.data).errorMessage();
            return message;
        }
    }
}
export let APIInstance = new Api();
