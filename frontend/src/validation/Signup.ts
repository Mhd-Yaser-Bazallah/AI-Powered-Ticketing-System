import * as yup from 'yup';

const SignupSchema = yup.object({
    email: yup
        .string()
        .required('This field is required.')
        .matches(/@[^.]*\./, 'Please enter a valid email'),
    password: yup.string().required('This field is required.').min(6, 'Must contain at least 8 characters.'),
    username: yup.string().required('This field is required.'),
    phone_number: yup.string().required('This field is required.'),
});

const SignupInitialValues = {
    email: '',
    password: '',
    username: '',
    company_id: sessionStorage.getItem('company_id'),
    phone_number: '',
};

export { SignupSchema, SignupInitialValues };
