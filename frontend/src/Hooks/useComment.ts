import { useMutation, useQuery, useQueryClient } from 'react-query';
import { APIInstance } from '../services/APIs/Comment';
import Swal from 'sweetalert2';
import { reloadAfterChange } from '../utils/reload';

const Get = (id: any) => {
    return useQuery({
        queryKey: ['AllComment', id],
        queryFn: async () => await APIInstance.Get(id),
        refetchOnWindowFocus: false,
    });
};

const Add = () => {
    const queryClient = useQueryClient();
    return useMutation({
        mutationKey: [`AddComment`],
        mutationFn: async (values) => await APIInstance.Add(values),
        onSuccess: async (res) => {
            if (res?.status === 201) {
                queryClient.invalidateQueries({ queryKey: [`AllComment`] });
                await Swal.fire({
                    title: res?.data?.message || 'Comment added successfully!',
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
        mutationKey: [`EditComment`, id],
        mutationFn: async (values) => await APIInstance.Edit(id, values),
        onSuccess: async (res) => {
            if (res?.status === 200) {
                queryClient.invalidateQueries({ queryKey: [`AllComment`] });
                await Swal.fire({
                    title: res?.data?.message || 'Comment edited successfully!',
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
        mutationKey: [`DeleteComment`],
        mutationFn: async (id) => await APIInstance.Delete(id),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: [`AllComment`] });
            setTimeout(() => reloadAfterChange(), 400);
        },
    });
};

export { Add, Get, Delete, Edit };
