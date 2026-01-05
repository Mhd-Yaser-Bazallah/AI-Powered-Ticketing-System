import { useFormik } from 'formik';
import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { GetAll } from '../../Hooks/useCompany';
import { Edit as EditUser } from "../../Hooks/useUser";
import Loading from '../../components/Button/Loading';
import { SelectInput } from '../../components/Input/Select';
import { Input } from '../../components/Input/Text';
import EditModal from '../../components/Modal/Edit';
import { reloadAfterChange } from '../../utils/reload';

const Edit = (props: any) => {
    const [t] = useTranslation();
    const mutation: any = EditUser(props.data.id);
    const [modal, setModal] = useState(false);

    const formik = useFormik({
        initialValues: {
            username: props?.data?.username,
            company_id: props?.data?.company_id,
            email: props?.data?.email,
            phone_number: props?.data?.phone_number,
        },
        onSubmit: async (values: any, { resetForm }) => {
            // Detect changes
            const changedValues = Object.keys(values).reduce((acc: any, key) => {
                if (values[key] !== formik.initialValues[key]) {
                    acc[key] = values[key];
                }
                return acc;
            }, {});

            if (Object.keys(changedValues).length === 0) {
                // No changes made, close modal without API call
                setModal(false);
                return;
            }

            mutation.mutate(changedValues, {
                onSuccess: async (res: any) => {
                    if (res?.status === 201) {
                        setModal(false);
                        resetForm();
                        setTimeout(() => reloadAfterChange(), 400);
                    }
                },
            });
        },
    });
    const GetComoany = GetAll()

    return (
        <>
            <EditModal
                modal={modal}
                setModal={setModal}
                form={
                    <>
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
                                <SelectInput name="company_id" options={GetComoany?.data?.data || []} displayFields={['name', "", ""]} formik={formik} label="Company" />

                                <Loading mutation={mutation.isLoading} title={t('Edit This User')} />
                            </form>
                        </div>
                    </>
                }
            />
        </>
    );
};

export default Edit;
