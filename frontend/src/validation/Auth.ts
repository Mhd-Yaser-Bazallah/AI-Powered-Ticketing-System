import * as yup from 'yup';

const LoginSchema = yup.object({
    email: yup
        .string()
        .required('This field is required.')
        .matches(/@[^.]*\./, 'Please enter a valid email'),
    password: yup.string().required('This field is required.').min(4, 'Must contain at least 8 characters.'),
});

const LoginInitialValues = {
    email: '',
    password: '',
};

export { LoginSchema, LoginInitialValues };
