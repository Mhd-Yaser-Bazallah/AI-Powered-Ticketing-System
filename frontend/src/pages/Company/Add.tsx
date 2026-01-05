import { useFormik } from 'formik';
import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Add as AddCompany } from "../../Hooks/useCompany";
import Loading from '../../components/Button/Loading';
import { Input } from '../../components/Input/Text';
import AddModal from '../../components/Modal/Add';
import {
    CompanyInitialValues,
    CompanySchema,
} from '../../validation/Company';
import { reloadAfterChange } from '../../utils/reload';


const Add = () => {
    const [t] = useTranslation();
    const mutation = AddCompany();
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
        initialValues: CompanyInitialValues,
        validationSchema: CompanySchema,
        onSubmit: handleSubmit,
    });

    return (
        <>
            <AddModal
                modal={modal}
                setModal={setModal}
                title={t('Add New Company')}
                form={
                    <div className='mx-auto w-full max-w-[440px]'>
                        <form onSubmit={formik.handleSubmit} className='grid w-full gap-3'>
                            <Input
                                names={["name", "address"]}
                                labels={["Name", "Address"]}
                                formik={formik}
                                type='text'
                            />
                            <Input
                                names={["email"]}
                                labels={["Email"]}
                                formik={formik}
                                type='email'
                            />
                            <Loading mutation={mutation.isLoading} title={t('Create New Company')} />
                        </form>
                    </div>
                }
            />
        </>
    );
};

export default Add;
