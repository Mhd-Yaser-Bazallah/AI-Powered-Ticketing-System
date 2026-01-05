import BackendError from "../Error/Error";
import { MainMethod } from "./Main";
export default class Api {

    async Get(id: any) {
        try {
            let result: any = await MainMethod.getRequest(`notification/${id}`)
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status, e.response.data).errorMessage();
            return message;
        }
    }
    async MakeRead(noti_id:any,data: any) {
        try {
            let result: any = await MainMethod.addPostRequest(`notification/${noti_id}/read`, data)
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status, e.response.data).errorMessage();
            return message;
        }
    }
    async MakeAllRead(data: any) {
        try {
            let result: any = await MainMethod.addPostRequest(`notification/read/all`, data)
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status, e.response.data).errorMessage();
            return message;
        }
    }
}
export let APIInstance = new Api();
