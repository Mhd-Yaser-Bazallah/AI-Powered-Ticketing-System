import { useFormik } from 'formik';
import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Edit as EditCompany } from "../../Hooks/useCompany";
import Loading from '../../components/Button/Loading';
import { Input } from '../../components/Input/Text';
import EditModal from '../../components/Modal/Edit';
import { reloadAfterChange } from '../../utils/reload';

const Edit = (props: any) => {
    const [t] = useTranslation();
    const mutation: any = EditCompany(props.data.id);
    const [modal, setModal] = useState(false);

    const formik = useFormik({
        initialValues: {
            name: props?.data?.name,
            address: props?.data?.address,
            email: props?.data?.email,
        },
        onSubmit: async (values: any, { resetForm }) => {
            // Detect changed fields
            const changedValues = Object.keys(values).reduce((acc: any, key) => {
                if (values[key] !== formik.initialValues[key]) {
                    acc[key] = values[key];
                }
                return acc;
            }, {});

            if (Object.keys(changedValues).length === 0) {
                // No changes were made
                setModal(false);
                return;
            }

            mutation.mutate(changedValues, {
                onSuccess: async (res: any) => {
                    if (res?.status === 200) {
                        setModal(false);
                        resetForm();
                        setTimeout(() => reloadAfterChange(), 400);
                    }
                },
            });
        },
    });
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
                                <Loading mutation={mutation.isLoading} title={t('Edit This Company')} />
                            </form>
                        </div>
                    </>
                }
            />
        </>
    );
};

export default Edit;
