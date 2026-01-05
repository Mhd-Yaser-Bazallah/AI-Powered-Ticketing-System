import { useMutation, useQuery, useQueryClient } from 'react-query';
import { APIInstance } from '../services/APIs/Profile';
import Swal from 'sweetalert2';
import { useNavigate } from 'react-router-dom';

const Get = (id: any) => {
    return useQuery({
        queryKey: ['me', id],
        queryFn: async () => await APIInstance.Get(id),
        refetchOnWindowFocus: false,
    });
};

const Edit = () => {
    const queryClient = useQueryClient();
    return useMutation({
        mutationKey: [`EditUser`],
        mutationFn: async (values) => await APIInstance.Edit(values),
        onSuccess: async (res) => {
            if (res?.status === 200) {
                queryClient.invalidateQueries({ queryKey: [`me`] });
            }
        },
    });
};

const Delete = () => {
    const queryClient = useQueryClient();
    const navigate = useNavigate();

    return useMutation({
        mutationKey: [`DeleteUser`],
        mutationFn: async (id) => await APIInstance.Delete(id),
        onSuccess: async () => {
            queryClient.invalidateQueries({ queryKey: [`AllUser`] });
            sessionStorage.clear();
            await navigate('/');
        },
    });
};

export { Get, Edit, Delete };
