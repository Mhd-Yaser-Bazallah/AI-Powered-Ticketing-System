import { useFormik } from 'formik';
import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { GetAll } from '../../Hooks/useCompany';
import { Add as AddTeamMember } from "../../Hooks/useTeamMember";
import Loading from '../../components/Button/Loading';
import { SelectInput } from '../../components/Input/Select';
import { Input } from '../../components/Input/Text';
import AddModal from '../../components/Modal/Add';
import {
    TeamMemberInitialValues,
    TeamMemberSchema,
} from '../../validation/TeamMember';
import { reloadAfterChange } from '../../utils/reload';


const Add = () => {
    const [t] = useTranslation();
    const mutation = AddTeamMember();
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
        initialValues: {...TeamMemberInitialValues,company_id:sessionStorage.getItem('company_id')},
        validationSchema: TeamMemberSchema,
        onSubmit: handleSubmit,
    });

    const GetComoany = GetAll()

    return (
        <>
            <AddModal
                modal={modal}
                setModal={setModal}
                title={t('Add New TeamMember')}
                form={
                    <div className='mx-auto w-full max-w-[440px]'>
                        <form onSubmit={formik.handleSubmit} className='grid w-full gap-3'>
                            <Input
                                names={["username"]}
                                labels={["Name"]}
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
                            <Loading mutation={mutation.isLoading} title={t('Create New Team Member')} />
                        </form>
                    </div>
                }
            />
        </>
    );
};

export default Add;
