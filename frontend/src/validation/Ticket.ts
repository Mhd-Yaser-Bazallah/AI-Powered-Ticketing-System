import * as yup from 'yup';

const TicketSchema = yup.object({
    description: yup.string().required('هذا الحقل مطلوب'),
    title: yup.string().required('هذا الحقل مطلوب'),
});

const TicketInitialValues = {
    description: '',
    title: '',
    company: '',
    client: '',
};

export { TicketSchema, TicketInitialValues };
