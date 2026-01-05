import { useMutation } from 'react-query';
import { useNavigate } from 'react-router-dom';
import Swal from 'sweetalert2';
import { AuthInstance } from '../services/APIs/Auth';
import { Login as LoginType } from '../types/Auth';
import { jwtDecode } from 'jwt-decode';
const useLogin = () => {
    const navigate = useNavigate();
    return useMutation({
        mutationKey: 'login',
        mutationFn: async (values: LoginType) => {
            const response = await AuthInstance.login(values);
            if (!response || response.status !== 200) {
                throw new Error('Login failed');
            }
            return response.data;
        },
        onSuccess: (data) => {
            try {
                sessionStorage.setItem('token', data.token);
                const decoded: any = jwtDecode(data.token);
                const role = decoded.role;
                const id = decoded.user_id;
                sessionStorage.setItem('role', role);
                sessionStorage.setItem('id', id);
                if (role === 'admin') {
                    navigate('/user');
                } else {
                    navigate('/profile' );
                }
            } catch (error) {}
        },
    });
};



export { useLogin };
