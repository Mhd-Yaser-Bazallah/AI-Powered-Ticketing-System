import * as yup from 'yup';

const AssginTicketToTeamSchema = yup.object({
    // team_id: yup.string().required('هذا الحقل مطلوب'),
});

const AssginTicketToTeamInitialValues = {
    team_id: '',
  
};

export { AssginTicketToTeamSchema, AssginTicketToTeamInitialValues };
