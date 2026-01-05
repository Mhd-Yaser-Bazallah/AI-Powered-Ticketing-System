import { useFormik } from 'formik';
import { useState } from 'react';
import toast from 'react-hot-toast';
import IconLoader from '../Icon/IconLoader';
import { reloadAfterChange } from '../../utils/reload';

export const Delete_request = ({ query_name, id, label_of_button, setModalState,query_title }: any) => {
    const [isLoading, setIsLoading] = useState(false);
    const mutation = query_name(query_title);
    const formik = useFormik({
        initialValues: {},
        onSubmit: async (e: any) => {
            setIsLoading(true);
            try {
                await mutation.mutateAsync(id).then((res: any) => {
                    toast.success(res?.data?.message);
                    setTimeout(() => reloadAfterChange(), 400);
                });
            } finally {
                setIsLoading(false);
                setModalState(false);
            }
        },
    });
    return (
        <form onSubmit={formik.handleSubmit} className="ltr:ml-4 rtl:mr-4">
            <button type="submit" className="btn btn-danger bg-danger" disabled={isLoading}>
                {isLoading ? <IconLoader className="text-white animate-spin" /> : label_of_button}
            </button>
        </form>
    );
};

export default Delete_request;
