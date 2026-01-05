import { useMutation } from 'react-query';
import { useNavigate } from 'react-router-dom';
import Swal from 'sweetalert2';
import { AuthInstance } from '../services/APIs/Auth';
import { Signup as SignupType } from '../types/Signup';

const Signup = () => {
    const navigate = useNavigate();
    return useMutation({
        mutationKey: 'login',
        mutationFn: async (values: SignupType) => await AuthInstance.Signup(values),
        onSuccess: async (res) => {
            if (res?.status === 200)
            {
            }
        },
    });
};

export { Signup };
