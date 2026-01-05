import { useFormik } from 'formik';
import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { GetAll } from '../../Hooks/useTeam';
import { AddMemberToTeam } from "../../Hooks/useTeamMember";
import Loading from '../../components/Button/Loading';
import { SelectInput } from '../../components/Input/Select';
import AddModal from '../../components/Modal/Add';
import {
    TeamMemberToSchema
} from '../../validation/TeamMember';
import { reloadAfterChange } from '../../utils/reload';
const Edit = (props: any) => {
    const [t] = useTranslation();
    const mutation = AddMemberToTeam(props?.data?.id);
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
        initialValues: {
            team_id: props?.data?.team_id || ''
        },
        validationSchema: TeamMemberToSchema,
        onSubmit: handleSubmit,
    });
    const GetTeam = GetAll(sessionStorage.getItem('company_id'))
    return (
        <>
            <AddModal
                modal={modal}
                setModal={setModal}
                title={props?.data?.team_id ? " Edit Team " : " Add Member To Team"}
                form={
                    <div className='mx-auto w-full max-w-[440px]'>
                        <form onSubmit={formik.handleSubmit} className='grid w-full gap-3'>
                            <SelectInput name="team_id" options={GetTeam?.data?.data || []} displayFields={['category', "", ""]} formik={formik} label="Team" />
                            <Loading mutation={mutation.isLoading} title={props?.data?.team_id ? " Edit Team " : " Add Team Member"} />
                        </form>
                    </div>
                }
            />
        </>
    );
};

export default Edit;
