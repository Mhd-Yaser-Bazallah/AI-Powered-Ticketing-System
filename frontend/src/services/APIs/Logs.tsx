import BackendError from "../Error/Error";
import { MainMethod } from "./Main";
export default class Api {

    async Get(id:any,pageNumber: number) {
        try {
            let result: any = await MainMethod.getRequest(`ticket-log/cmopany_log/${id}?page=${pageNumber}`)
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status, e.response.data).errorMessage();
            return message;
        }
    }
}
export let APIInstance = new Api();
