import * as yup from 'yup';
import Ticket from '../pages/Ticket/Ticket';

const CommentSchema = yup.object({
    ticket: yup.string().required('هذا الحقل مطلوب'),
    user: yup.string().required('هذا الحقل مطلوب'),
    description: yup.string().required('هذا الحقل مطلوب'),
});

const CommentInitialValues = {
    ticket: '',
    user: '',
    description: '',
};

export { CommentSchema, CommentInitialValues };
