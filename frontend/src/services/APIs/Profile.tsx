import BackendError from "../Error/Error";
import { MainMethod } from "./Main";
export default class Api {

    async Get(id: string) {
        try {
            let result: any = await MainMethod.getRequest(`users/getme/${id}`)
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status, e.response.data).errorMessage();
            return message;
        }
    }
    async Edit(data: any) {
        try {
            let result: any = await MainMethod.putRequestForEditProfile(`users/account/update`, data)
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status, e.response.data).errorMessage();
            return message;
        }
    }
    async Delete(id: any) {
        try {
            let result: any = await MainMethod.deleteRequest(`users/account/delete`, id, {})
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status, e.response.data).errorMessage();
            return message;
        }
    }
}
export let APIInstance = new Api();
