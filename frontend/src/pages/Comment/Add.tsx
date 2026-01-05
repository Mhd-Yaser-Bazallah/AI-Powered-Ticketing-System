import { useFormik } from 'formik';
import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Add as AddComment } from "../../Hooks/useComment";
import Loading from '../../components/Button/Loading';
import { TextArea } from '../../components/Input/TextArea'; // New TextArea component
import AddModal from '../../components/Modal/Add';
import { CommentInitialValues, CommentSchema } from '../../validation/Comment';
import { APIInstance } from '../../services/APIs/Comment';
import { reloadAfterChange } from '../../utils/reload';

const Add = (props: any) => {
    const [t] = useTranslation();
    const [ticket_id] = useState(props?.data?.data?.id ? props?.data?.data?.id : null);
    const mutation = AddComment();
    const [modal, setModal] = useState(false);

    const handleSubmit = async (values: any, { resetForm }: any) => {
        mutation.mutate(values, {
            onSuccess: async (res) => {
                if (res?.status === 201) {
                    setModal(false);
                    resetForm();

                    // Fetch the new comment and pass it to the parent
                    const newComment = res?.data; // Adjust based on your API response
                    props.onAddComment(newComment);
                    setTimeout(() => reloadAfterChange(), 400);
                }
            },
        });
    };

    const formik = useFormik({
        initialValues: {
            ...CommentInitialValues,
            ticket: props?.data?.data?.id,
            user: sessionStorage.getItem('id'),
        },
        validationSchema: CommentSchema,
        onSubmit: handleSubmit,
    });

    return (
        <div className="mx-auto w-full max-w-[440px]">
            <form onSubmit={formik.handleSubmit} className="grid w-full gap-3">
                <TextArea
                    name="description"
                    label={t('')} // Label for the text area
                    formik={formik}
                    placeholder={t('Enter your comment here...')}
                />
                <Loading mutation={mutation.isLoading} title={t('Create New Comment')} />
            </form>
        </div>
    );
};

export default Add;

