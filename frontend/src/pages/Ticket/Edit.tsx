import { useFormik } from 'formik';
import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { GetAll } from '../../Hooks/useTeam';
import { Edit as EditTicket } from "../../Hooks/useTicket";
import Loading from '../../components/Button/Loading';
import { SelectInput } from '../../components/Input/Select';
import AddModal from '../../components/Modal/Add';

import { Input } from '../../components/Input/Text';
import EditModal from '../../components/Modal/Edit';
import { reloadAfterChange } from '../../utils/reload';
const Edit = (props: any) => {
    const [t] = useTranslation();
    const mutation = EditTicket(props?.data?.id);
    const [modal, setModal] = useState(false);
    const handleSubmit = async (values: any, { resetForm }: any) => {
        mutation.mutate(values, {
            onSuccess: async (res) => {
                if (res?.status === 200) {
                    setModal(false);
                    resetForm();
                    setTimeout(() => reloadAfterChange(), 400);
                }
            },
        });
    };
    const formik = useFormik({
        initialValues: {
            description: props?.data?.description || '',
            title: props?.data?.title || ''
        },
        onSubmit: handleSubmit,
    });
    return (
        <>
            <EditModal
                modal={modal}
                setModal={setModal}
                title={"Edit"}
                form={
                    <div className='mx-auto w-full max-w-[440px]'>
                        <form onSubmit={formik.handleSubmit} className='grid w-full gap-3'>
                            <Input
                                names={["description", "title"]}
                                labels={["description", "title"]}
                                formik={formik}
                                type='text'
                            />
                            <Loading mutation={mutation.isLoading} title={'Edit'} />
                        </form>
                    </div>
                }
            />
        </>
    );
};

export default Edit;
