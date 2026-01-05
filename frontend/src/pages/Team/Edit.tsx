import { useFormik } from 'formik';
import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { GetAll } from '../../Hooks/useCompany';
import { Edit as EditTeam } from "../../Hooks/useTeam";
import Loading from '../../components/Button/Loading';
import { SelectInput } from '../../components/Input/Select';
import { Input } from '../../components/Input/Text';
import EditModal from '../../components/Modal/Edit';
import { reloadAfterChange } from '../../utils/reload';

const Edit = (props: any) => {
    const [t] = useTranslation();
    const mutation: any = EditTeam(props.data.id);
    const [modal, setModal] = useState(false);

    const formik = useFormik({
        initialValues: {
            company: props?.data?.company,
            category: props?.data?.category,
            description: props?.data?.description,
        },
        onSubmit: async (values: any, { resetForm }) => {
            const changedValues = Object.keys(values).reduce((acc: any, key) => {
                if (values[key] !== formik.initialValues[key]) {
                    acc[key] = values[key];
                }
                return acc;
            }, {});

            if (Object.keys(changedValues).length === 0) {
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
                                    names={["category","description"]}
                                    labels={["category","description"]}
                                    formik={formik}
                                    type='text'
                                />

                                <Loading mutation={mutation.isLoading} title={t('Edit This Team')} />
                            </form>
                        </div>
                    </>
                }
            />
        </>
    );
};

export default Edit;
