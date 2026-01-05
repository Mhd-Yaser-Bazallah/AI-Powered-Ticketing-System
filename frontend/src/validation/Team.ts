import * as yup from 'yup';

const TeamSchema = yup.object({
    category: yup.string().required('هذا الحقل مطلوب'),
    description: yup.string().required('هذا الحقل مطلوب'),
});

const TeamInitialValues = {
    category: '',
    description: '',
};

export { TeamSchema, TeamInitialValues };
