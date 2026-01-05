import { useMutation, useQuery, useQueryClient } from 'react-query';
import { APIInstance } from '../services/APIs/Team';
import Swal from 'sweetalert2';
import { reloadAfterChange } from '../utils/reload';

const Get = (page: any) => {
    return useQuery({
        queryKey: ['AllTeam', page],
        queryFn: async () => await APIInstance.Get(page),
        refetchOnWindowFocus: false,
    });
};

const GetAll = (company_id:any) => {
    return useQuery({
        queryKey: ['Team'],
        queryFn: async () => await APIInstance.GetAll(company_id),
        refetchOnWindowFocus: false,
    });
};

const Add = () => {
    const queryClient = useQueryClient();
    return useMutation({
        mutationKey: [`AddTeam`],
        mutationFn: async (values) => await APIInstance.Add(values),
        onSuccess: async (res) => {
            if (res?.status === 201) {
                queryClient.invalidateQueries({ queryKey: [`AllTeam`] });
                await Swal.fire({
                    title: res?.data?.message || 'Team added successfully!',
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
        mutationKey: [`EditTeam`, id],
        mutationFn: async (values) => await APIInstance.Edit(id, values),
        onSuccess: async (res) => {
            if (res?.status === 200) {
                queryClient.invalidateQueries({ queryKey: [`AllTeam`] });
                await Swal.fire({
                    title: res?.data?.message || 'Team edited successfully!',
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
        mutationKey: [`DeleteTeam`],
        mutationFn: async (id) => await APIInstance.Delete(id),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: [`AllTeam`] });
            setTimeout(() => reloadAfterChange(), 400);
        },
    });
};

export { Add, Get, Delete, Edit,GetAll };
