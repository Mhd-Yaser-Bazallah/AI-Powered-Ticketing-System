import axios from 'axios';
export const BASEURL = import.meta.env.VITE_BASEURL;
import Cookies from 'js-cookie';
export default class Main {
    loginRequest(data: object) {
        return axios.post(`${BASEURL}authentication/login`, data, { withCredentials: true });
    }
    logoutRequest() {
        return axios.post(`${BASEURL}authentication/logout`, {}, {
            withCredentials: true,

        });
    }
    SignupRequest(data: object) {
        return axios.post(`${BASEURL}authentication/register`, data, { withCredentials: true });
    }

    getRequest = async (url: string) => {
        return await axios.get(BASEURL + `${url}`, {
            withCredentials: true,
            headers: {
                Authorization: 'jwt=' + sessionStorage.getItem('token'),
                'Content-Type': 'application/json',
            }
        });
    };
    getRequestFile = async (url: string) => {
        return await axios.get(BASEURL + `${url}`, {
            responseType: "blob" ,
            withCredentials: true,
            headers: {
                Authorization: 'jwt=' + sessionStorage.getItem('token'),
                'Content-Type': 'application/json',
            },
            
        });
    };
    getNotiRequest = async (url: string ,data:any) => {
        return await axios.get(BASEURL + `${url}`, {
            withCredentials: true,
            headers: {
                Authorization: 'jwt=' + sessionStorage.getItem('token'),
                'Content-Type': 'application/json',
            },
            data
        });
    };

    addPostRequest = async (url: string, data: any) => {
        return await axios.post(BASEURL + `${url}`, data, {
            withCredentials: true,
            headers: {
                Authorization: 'jwt=' + sessionStorage.getItem('token'),
                'Content-Type': 'application/json',
            }
        });
    };
    putRequest = async (url: string, id: any, data: any) => {
        return await axios.put(BASEURL + `${url}/${id}`, data, {
            withCredentials: true,
            headers: {
                Authorization: 'jwt=' + sessionStorage.getItem('token'),
                'Content-Type': 'application/json',
            }
        });
    };
    putRequestForEditProfile = async (url: string, data: any) => {
        return await axios.put(BASEURL + `${url}`, data, {
            withCredentials: true,
            headers: {
                Authorization: 'jwt=' + sessionStorage.getItem('token'),
                'Content-Type': 'application/json',
            }
        });
    };

    deleteRequest = async (url: string, id: any, data: any) => {
        return await axios.delete(BASEURL + `${url}/${id}`, {
            withCredentials: true,
            headers: {
                Authorization: 'jwt=' + sessionStorage.getItem('token'),
                'Content-Type': 'application/json',
            }
        });
    };


}

export let MainMethod = new Main();

