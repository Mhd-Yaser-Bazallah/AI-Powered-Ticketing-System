import * as yup from 'yup';

const CompanySchema = yup.object({
    name: yup.string().required('هذا الحقل مطلوب'),
    email: yup.string().required('هذا الحقل مطلوب'),
    address: yup.string().required('هذا الحقل مطلوب'),
});

const CompanyInitialValues = {
    name: '',
    email: '',
    address: '',
};

export { CompanySchema, CompanyInitialValues };
