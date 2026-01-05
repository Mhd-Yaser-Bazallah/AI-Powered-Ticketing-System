import BackendError from "../Error/Error";
import { MainMethod } from "./Main";
export default class Api {

    async Get(pageNumber: number ,id:any) {
        try {
            let result: any = await MainMethod.getRequest(`team/List-members/${id}?page=${pageNumber}`)
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status, e.response.data).errorMessage();
            return message;
        }
    }
    async GetALl(id:any) {
        try {
            let result: any = await MainMethod.getRequest(`team/List-members/${id}`)
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status, e.response.data).errorMessage();
            return message;
        }
    }

    async Add(data: any) {
        try {
            let result: any = await MainMethod.addPostRequest(`team/createMember`, data)
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status, e.response.data).errorMessage();
            return message;
        }
    }
    async AddMemberToTeam(id:any,data: any) {
        try {
            let result: any = await MainMethod.addPostRequest(`team/add-user/${id}`, data)
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status, e.response.data).errorMessage();
            return message;
        }
    }

    async ChangeStatus(id: any, data: any) {
        try {
            let result: any = await MainMethod.putRequest(`team/activate`,id , data)
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status, e.response.data).errorMessage();
            return message;
        }}
    async changeStatusMutationToDeActivate(id: any, data: any) {
        try {
            let result: any = await MainMethod.putRequest(`team/deactivate`,id , data)
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status, e.response.data).errorMessage();
            return message;
        }}
}
export let APIInstance = new Api();
