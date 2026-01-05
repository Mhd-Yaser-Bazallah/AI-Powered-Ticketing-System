import { useFormik } from 'formik';
import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Add as AddTicket } from "../../Hooks/useTicket";
import Loading from '../../components/Button/Loading';
import { Input } from '../../components/Input/Text';
import AddModal from '../../components/Modal/Add';
import {
    TicketInitialValues,
    TicketSchema,
} from '../../validation/Ticket';
import { APIInstance } from '../../services/APIs/Ticket';
import { TextArea } from '../../components/Input/TextArea';
import { reloadAfterChange } from '../../utils/reload';


const Add = () => {
    const [t] = useTranslation();
    const mutation = AddTicket();
    const [modal, setModal] = useState(false);
    const handleSubmit = async (values: any, { resetForm }: any) => {
        mutation.mutate(values, {
            onSuccess: async (res) => {
                if (res?.status === 201) {
                    setModal(false);
                    resetForm();
                    let id: any = sessionStorage.getItem('id')
                    setTimeout(() => reloadAfterChange(), 400);
                }
            },
        });
    };
    const initialCompany = sessionStorage?.getItem('company_id') || '';
    const initialClient = sessionStorage?.getItem('id') || '';
    const formik = useFormik({
        initialValues: {
            ...TicketInitialValues,
            company: initialCompany,
            client: initialClient,
        },
        onSubmit: handleSubmit,
    });

    return (
        <>
            <AddModal
                modal={modal}
                setModal={setModal}
                title={t('Add New Ticket')}
                form={
                    <div className='mx-auto w-full max-w-[440px]'>
                        <form onSubmit={formik.handleSubmit} className='grid w-full gap-3'>
                            <Input
                                names={["title"]}
                                labels={["title"]}
                                formik={formik}
                                type='text'
                            />
                            <TextArea
                                name="description"
                                label={t('description')} // Label for the text area
                                formik={formik}
                                placeholder={t('Enter your comment here...')}
                            />
                            <Loading mutation={mutation.isLoading} title={t('Create New Ticket')} />
                        </form>
                    </div>
                }
            />
        </>
    );
};

export default Add;
