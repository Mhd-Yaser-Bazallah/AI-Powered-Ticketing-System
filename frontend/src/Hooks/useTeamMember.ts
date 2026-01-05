import { useMutation, useQuery, useQueryClient } from 'react-query';
import { APIInstance } from '../services/APIs/TeamMember';
import Swal from 'sweetalert2';
import { reloadAfterChange } from '../utils/reload';

const Get = (page: any, id: any) => {
    return useQuery({
        queryKey: ['AllTeamMember', page, id],
        queryFn: async () => await APIInstance.Get(id, page),
        refetchOnWindowFocus: false,
    });
};

const GetAll = ( id: any) => {
    return useQuery({
        queryKey: ['AllTeamMembers',id],
        queryFn: async () => await APIInstance.GetALl(id),
        refetchOnWindowFocus: false,
    });
};

const Add = () => {
    const queryClient = useQueryClient();
    return useMutation({
        mutationKey: [`AddTeamMember`],
        mutationFn: async (values) => await APIInstance.Add(values),
        onSuccess: async (res) => {
            if (res?.status === 201) {
                queryClient.invalidateQueries({ queryKey: [`AllTeamMember`] });
                await Swal.fire({
                    title: res?.data?.message || 'TeamMember added successfully!',
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

const AddMemberToTeam = (id: any) => {
    const queryClient = useQueryClient();
    return useMutation({
        mutationKey: [`AddMember`, id],
        mutationFn: async (values) => await APIInstance.AddMemberToTeam(id, values),
        onSuccess: async (res) => {
            if (res?.status === 201) {
                queryClient.invalidateQueries({ queryKey: [`AllTeamMember`] });
                await Swal.fire({
                    title: res?.data?.message || 'TeamMember added successfully!',
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
const ChangeStatus = () => {
    const queryClient = useQueryClient();
    return useMutation({
        mutationKey: ['MakeRead'],
        mutationFn: async (Id) => await APIInstance.ChangeStatus(Id, {}),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: [`AllTeamMember`] });
            setTimeout(() => reloadAfterChange(), 400);
        },
    });
};
const changeStatusMutationToDeActivate = () => {
    const queryClient = useQueryClient();
    return useMutation({
        mutationKey: ['MakeRead'],
        mutationFn: async (Id) => await APIInstance.changeStatusMutationToDeActivate(Id, {}),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: [`AllTeamMember`] });
            setTimeout(() => reloadAfterChange(), 400);
        },
    });
};

export { Add, Get, ChangeStatus ,AddMemberToTeam  ,changeStatusMutationToDeActivate ,GetAll};
