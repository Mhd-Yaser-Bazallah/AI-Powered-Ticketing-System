import * as yup from 'yup';

const TeamMemberSchema = yup.object({
    email: yup.string().required('هذا الحقل مطلوب'),
    password: yup.string().required('هذا الحقل مطلوب'),
    username: yup.string().required('هذا الحقل مطلوب'),
    phone_number: yup.string().required('هذا الحقل مطلوب'),
});

const TeamMemberInitialValues = {
    username: '',
    password: '',
    phone_number: '',
    email: '',
};
const TeamMemberToSchema = yup.object({
    team_id: yup.string().required('هذا الحقل مطلوب'),
});

const TeamMemberToInitialValues = {
    team_id: '',
};

export { TeamMemberSchema, TeamMemberInitialValues, TeamMemberToInitialValues, TeamMemberToSchema };
