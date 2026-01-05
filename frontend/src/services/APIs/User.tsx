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

    async Add(data: any) {
        try {
            let result: any = await MainMethod.addPostRequest(`users/create`, data)
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
