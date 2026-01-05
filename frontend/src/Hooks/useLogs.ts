import { useMutation, useQuery, useQueryClient } from 'react-query';
import { APIInstance } from '../services/APIs/Logs';
import Swal from 'sweetalert2';

const Get = (id: any, page: any) => {
    return useQuery({
        queryKey: ['AllUser', id, page],
        queryFn: async () => await APIInstance.Get(id, page),
        refetchOnWindowFocus: false,
    });
};

export { Get };
