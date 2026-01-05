import { useMutation, useQuery, useQueryClient } from 'react-query';
import { APIInstance } from '../services/APIs/Company';
import Swal from 'sweetalert2';
import { reloadAfterChange } from '../utils/reload';

const Get = (page: any) => {
    return useQuery({
        queryKey: ['AllCompany', page],
        queryFn: async () => await APIInstance.Get(page),
        refetchOnWindowFocus: false,
    });
};
const GetAll = () => {
    return useQuery({
        queryKey: ['company'],
        queryFn: async () => await APIInstance.GetAll(),
        refetchOnWindowFocus: false,
    });
};

const ChangeStatusAssign = () => {
    const queryClient = useQueryClient();
    return useMutation({
        mutationKey: ['toggle_auto_assign'],
        mutationFn: async (Id) => await APIInstance.toggle_auto_assign(Id),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: [`AllCompany`] });
            setTimeout(() => reloadAfterChange(), 400);
        },
    });
};
const ChangeStatusCategorize = () => {
    const queryClient = useQueryClient();
    return useMutation({
        mutationKey: ['toggle_auto_categorize'],
        mutationFn: async (Id) => await APIInstance.toggle_auto_categorize(Id),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: [`AllCompany`] });
            setTimeout(() => reloadAfterChange(), 400);
        },
    });
};
const ChangeStatusPrioritize = () => {
    const queryClient = useQueryClient();
    return useMutation({
        mutationKey: ['toggle_auto_prioritize'],
        mutationFn: async (Id) => await APIInstance.toggle_auto_prioritize(Id),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: [`AllCompany`] });
            setTimeout(() => reloadAfterChange(), 400);
        },
    });
};

const Add = () => {
    const queryClient = useQueryClient();
    return useMutation({
        mutationKey: [`AddCompany`],
        mutationFn: async (values) => await APIInstance.Add(values),
        onSuccess: async (res) => {
            if (res?.status === 201) {
                queryClient.invalidateQueries({ queryKey: [`AllCompany`] });
                await Swal.fire({
                    title: res?.data?.message || 'Company added successfully!',
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
        mutationKey: [`EditCompany`, id],
        mutationFn: async (values) => await APIInstance.Edit(id, values),
        onSuccess: async (res) => {
            if (res?.status === 200) {
                queryClient.invalidateQueries({ queryKey: [`AllCompany`] });
                await Swal.fire({
                    title: res?.data?.message || 'Company edited successfully!',
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
        mutationKey: [`DeleteCompany`],
        mutationFn: async (id) => await APIInstance.Delete(id),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: [`AllCompany`] });
            setTimeout(() => reloadAfterChange(), 400);
        },
    });
};

export { GetAll, Add, Get, Delete, Edit, ChangeStatusAssign, ChangeStatusCategorize, ChangeStatusPrioritize };
