import { useMutation, useQuery, useQueryClient } from 'react-query';
import { APIInstance } from '../services/APIs/User';
import Swal from 'sweetalert2';
import { reloadAfterChange } from '../utils/reload';

const Get = (page: any) => {
    return useQuery({
        queryKey: ['AllUser', page],
        queryFn: async () => await APIInstance.Get(page),
        refetchOnWindowFocus: false,
    });
};

const Add = () => {
    const queryClient = useQueryClient();
    return useMutation({
        mutationKey: [`AddUser`],
        mutationFn: async (values) => await APIInstance.Add(values),
        onSuccess: async (res) => {
            if (res?.status === 201) {
                queryClient.invalidateQueries({ queryKey: [`AllUser`] });
                await Swal.fire({
                    title: res?.data?.message || 'User added successfully!',
                    icon: 'success',
                    showClass: {
                        popup: `
                            animate__animated
                            animate__fadeInUp
                            animate__faster
                        `,
                    },
                    hideClass: {
                        popup: `
                            animate__animated
                            animate__fadeOutDown
                            animate__faster
                        `,
                    },
                });
                setTimeout(() => reloadAfterChange(), 400);
            }
        },
    });
};

const Edit = (id: number) => {
    const queryClient = useQueryClient();
    return useMutation({
        mutationKey: [`EditUser`, id],
        mutationFn: async (values) => await APIInstance.Edit(id, values),
        onSuccess: async (res) => {
            if (res?.status === 200) {
                queryClient.invalidateQueries({ queryKey: [`AllUser`] });
                await Swal.fire({
                    title: res?.data?.message || 'User edited successfully!',
                    icon: 'success',
                    showClass: {
                        popup: `
                            animate__animated
                            animate__fadeInUp
                            animate__faster
                        `,
                    },
                    hideClass: {
                        popup: `
                            animate__animated
                            animate__fadeOutDown
                            animate__faster
                        `,
                    },
                });
                setTimeout(() => reloadAfterChange(), 400);
            }
        },
    });
};

const Delete = () => {
    const queryClient = useQueryClient();
    return useMutation({
        mutationKey: [`DeleteUser`],
        mutationFn: async (id) => await APIInstance.Delete(id),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: [`AllUser`] });
            setTimeout(() => reloadAfterChange(), 400);
        },
    });
};

export { Add, Get, Delete, Edit };
