import * as yup from 'yup';

const UserSchema = yup.object({
    company_id: yup.string().required('هذا الحقل مطلوب'),
    email: yup.string().required('هذا الحقل مطلوب'),
    password: yup.string().required('هذا الحقل مطلوب'),
    username: yup.string().required('هذا الحقل مطلوب'),
    phone_number: yup.string().required('هذا الحقل مطلوب'),
});

const UserInitialValues = {
    username: '',
    password: '',
    company_id: '',
    phone_number: '',
    email: '',
};

export { UserSchema, UserInitialValues };
