import { useMutation, useQuery, useQueryClient } from 'react-query';
import { APIInstance } from '../services/APIs/Ticket';
import Swal from 'sweetalert2';
import { reloadAfterChange } from '../utils/reload';

const GetUserTicket = (id: number) => {
    return useQuery({
        queryKey: ['userTicket', id],
        queryFn: async () => await APIInstance.UserTicket(id),
        refetchOnWindowFocus: false,
    });
};
const GetSTMTicket = (id: number) => {
    return useQuery({
        queryKey: ['STMTicket', id],
        queryFn: async () => await APIInstance.STMTicket(id),
        refetchOnWindowFocus: false,
    });
};
const GetMTicket = (id: number) => {
    return useQuery({
        queryKey: ['STMTicket', id],
        queryFn: async () => await APIInstance.MemberTicket(id),
        refetchOnWindowFocus: false,
    });
};

const Add = () => {
    const queryClient = useQueryClient();
    return useMutation({
        mutationKey: [`AddTicket`],
        mutationFn: async (values) => await APIInstance.Add(values),
        onSuccess: async (res) => {
            if (res?.status === 201) {
                queryClient.invalidateQueries({ queryKey: [`AllTicket`] });
                await Swal.fire({
                    title: res?.data?.message || 'Ticket added successfully!',
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
const AssginToTicket = (id: number) => {
    const queryClient = useQueryClient();
    return useMutation({
        mutationKey: [`AssginTicketToTeam`],
        mutationFn: async (values) => await APIInstance.AssginToTeam(id, values),
        onSuccess: async (res) => {
            if (res?.status === 201) {
                queryClient.invalidateQueries({ queryKey: [`STMTicket`] });
                await Swal.fire({
                    title: res?.data?.message || 'Ticket Assgined successfully!',
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
const AssginToTicketIntoProgress = (id: number) => {
    const queryClient = useQueryClient();
    return useMutation({
        mutationKey: [`AssginTicketToInProgress`],
        mutationFn: async (values) => await APIInstance.AssginToInProgress(id, values),
        onSuccess: async (res) => {
            if (res?.status === 201) {
                queryClient.invalidateQueries({ queryKey: [`STMTicket`] });
                await Swal.fire({
                    title: res?.data?.message || 'Ticket Assgined successfully!',
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
const AssginToTicketIntoDone = (id: number) => {
    const queryClient = useQueryClient();
    return useMutation({
        mutationKey: [`AssginTicketToInDone`],
        mutationFn: async (values) => await APIInstance.AssginToInDone(id, values),
        onSuccess: async (res) => {
            if (res?.status === 201) {
                queryClient.invalidateQueries({ queryKey: [`STMTicket`] });
                await Swal.fire({
                    title: res?.data?.message || 'Ticket Assgined successfully!',
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

const AssginToMe = (id: number , userID:any) => {
    const queryClient = useQueryClient();
    return useMutation({
        mutationKey: [`AssginTicketToInDone`],
        mutationFn: async (values) => await APIInstance.AssginToMe(id, userID),
        onSuccess: async (res) => {
            if (res?.status === 201) {
                queryClient.invalidateQueries({ queryKey: [`STMTicket`] });
                await Swal.fire({
                    title: res?.data?.message || 'Ticket Assgined successfully!',
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
        mutationKey: [`EditTicket`, id],
        mutationFn: async (values) => await APIInstance.Edit(id, values),
        onSuccess: async (res) => {
            if (res?.status === 200) {
                queryClient.invalidateQueries({ queryKey: [`AllTicket`] });
                await Swal.fire({
                    title: res?.data?.message || 'Ticket edited successfully!',
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
        mutationKey: [`DeleteTicket`],
        mutationFn: async (id) => await APIInstance.Delete(id),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: [`AllTicket`] });
            setTimeout(() => reloadAfterChange(), 400);
        },
    });
};

export { AssginToTicket,Edit,Delete, AssginToMe, GetMTicket, AssginToTicketIntoDone, AssginToTicketIntoProgress, GetUserTicket, Add, GetSTMTicket };
