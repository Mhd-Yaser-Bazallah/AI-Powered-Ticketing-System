import axios from 'axios';
import { BASEURL, MainMethod } from './Main';
import BackendError from '../Error/Error';
import { useNavigate } from 'react-router-dom';
export default class Auth {
    async login(data: any) {
        try {
            let result: any = await MainMethod.loginRequest(data)
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status, e.response.data.error).errorMessage();
            return message;
        }
    }

    async Signup(data: any) {
        try {
            let result: any = await MainMethod.SignupRequest(data)
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status, e.response.data).errorMessage();
            return message;
        }
    }
    async Logout() {
        try {
            let result: any = await MainMethod.logoutRequest()
            return result
        } catch (e: any) {
            let message = new BackendError(e.response.status, e.response.data).errorMessage();
            return message;
        }
    }

    async MakeCheckForEmail(data: any) {
        try {
            let result: any = await MainMethod.addPostRequest(`company/company_email`, data)
            return result
        } catch (e: any) {
            console.log(e);
            
            let message = new BackendError(e.response.status, e.response.data).errorMessage();
            return message;
        }
    }
}
export const AuthInstance = new Auth();
