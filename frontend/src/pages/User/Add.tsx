import { useFormik } from 'formik';
import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { GetAll } from '../../Hooks/useCompany';
import { Add as AddUser } from "../../Hooks/useUser";
import Loading from '../../components/Button/Loading';
import { SelectInput } from '../../components/Input/Select';
import { Input } from '../../components/Input/Text';
import AddModal from '../../components/Modal/Add';
import {
    UserInitialValues,
    UserSchema,
} from '../../validation/User';
import { reloadAfterChange } from '../../utils/reload';


const Add = () => {
    const [t] = useTranslation();
    const mutation = AddUser();
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
        initialValues: UserInitialValues,
        validationSchema: UserSchema,
        onSubmit: handleSubmit,
    });

    const GetComoany = GetAll()

    return (
        <>
            <AddModal
                modal={modal}
                setModal={setModal}
                title={t('Add New User')}
                form={
                    <div className='mx-auto w-full max-w-[440px]'>
                        <form onSubmit={formik.handleSubmit} className='grid w-full gap-3'>
                            <Input
                                names={["username"]}
                                labels={["User Name"]}
                                formik={formik}
                                type='text'
                            />
                            <Input
                                names={["phone_number"]}
                                labels={["phone_number"]}
                                formik={formik}
                                type='number'
                            />
                            <Input
                                names={["email"]}
                                labels={["Email"]}
                                formik={formik}
                                type='email'
                            />
                            <Input
                                names={["password"]}
                                labels={["password"]}
                                formik={formik}
                                type='password'
                            />
                            <SelectInput name="company_id" options={GetComoany?.data?.data || []} displayFields={['name', "", ""]} formik={formik} label="Company" />
                            <Loading mutation={mutation.isLoading} title={t('Create New User')} />
                        </form>
                    </div>
                }
            />
        </>
    );
};

export default Add;
