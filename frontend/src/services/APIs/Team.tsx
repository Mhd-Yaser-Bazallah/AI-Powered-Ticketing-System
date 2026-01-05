import BackendError from "../Error/Error";
import { MainMethod } from "./Main";
export default class Api {

    async Get(pageNumber: number) {
        try {
            let result: any = await MainMethod.getRequest(`team/List?page=${pageNumber}`)
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status,e.response.data).errorMessage();
            return message;
        }
    }
    async GetAll(company_id:string) {
        try {
            let result: any = await MainMethod.getRequest(`team/team/${company_id}`)
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status,e.response.data).errorMessage();
            return message;
        }
    }

    async Add(data: any) {
        try {
            let result: any = await MainMethod.addPostRequest(`team/create`, data)
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status,e.response.data).errorMessage();
            return message;
        }
    }
    async Delete(id: any) {
        try {
            let result: any = await MainMethod.deleteRequest(`team/delete`, id, {})
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status,e.response.data).errorMessage();
            return message;
        }
    }
    async Edit(id: any, data: any) {
        try {
            let result: any = await MainMethod.putRequest(`team/update`, id, data)
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status,e.response.data).errorMessage();
            return message;
        }
    }
}
export let APIInstance = new Api();
