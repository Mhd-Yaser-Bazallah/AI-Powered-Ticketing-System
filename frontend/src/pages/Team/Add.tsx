import { useFormik } from 'formik';
import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { GetAll } from '../../Hooks/useCompany';
import { Add as AddTeam } from "../../Hooks/useTeam";
import Loading from '../../components/Button/Loading';
import { SelectInput } from '../../components/Input/Select';
import { Input } from '../../components/Input/Text';
import AddModal from '../../components/Modal/Add';
import {
    TeamInitialValues,
    TeamSchema,
} from '../../validation/Team';
import { reloadAfterChange } from '../../utils/reload';


const Add = () => {
    const [t] = useTranslation();
    const mutation = AddTeam();
    const [modal, setModal] = useState(false);
    const handleSubmit = async (values: any, { resetForm }: any) => {
        mutation.mutate(values, {
            onSuccess: async (res) => {
                if (res?.status === 201) {
                    setModal(false);
                    resetForm();
                    setTimeout(() => reloadAfterChange(), 400);
                }
            },
        });
    };

    const formik = useFormik({
        initialValues: {...TeamInitialValues,company:sessionStorage.getItem('company_id')},
        validationSchema: TeamSchema,
        onSubmit: handleSubmit,
    });

    return (
        <>
            <AddModal
                modal={modal}
                setModal={setModal}
                title={t('Add New Team')}
                form={
                    <div className='mx-auto w-full max-w-[440px]'>
                        <form onSubmit={formik.handleSubmit} className='grid w-full gap-3'>
                            <Input
                                names={["category", "description"]}
                                labels={["category", "description"]}
                                formik={formik}
                                type='text'
                            />

                            <Loading mutation={mutation.isLoading} title={t('Create New Team')} />
                        </form>
                    </div>
                }
            />
        </>
    );
};

export default Add;
