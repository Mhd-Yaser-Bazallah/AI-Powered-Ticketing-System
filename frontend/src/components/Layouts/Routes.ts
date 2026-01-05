import IconBolt from '../Icon/IconBolt';
import IconChartSquare from '../Icon/IconChartSquare';
import IconPaperclip from '../Icon/IconPaperclip';
import IconUser from '../Icon/IconUser';
import IconUserPlus from '../Icon/IconUserPlus';

export const Routes = [
    { route: 'user', label: 'User', icon: IconUser, roles: ['admin'] },
    { route: 'profile', label: 'Profile', icon: IconChartSquare, roles: ['admin', 'client', 'support_team_manager' ,"support_team_member"] },
    { route: 'ticket', label: 'Ticket', icon: IconBolt, roles: ['client', 'support_team_manager' ,"support_team_member"] },
    { route: 'team-ticket', label: 'My Team Ticket', icon: IconBolt, roles: ["support_team_member"] },
    { route: 'company', label: 'Company', icon: IconChartSquare, roles: ['admin'] },
    { route: 'team', label: 'Team', icon: IconUserPlus, roles: ['support_team_manager'] },
    { route: 'reporting', label: 'reporting and analysis', icon: IconUserPlus, roles: ['support_team_manager'] },
    { route: 'team-members', label: 'Team Members', icon: IconUserPlus, roles: ['support_team_manager'] },
    { route: 'logs', label: 'Activity Logs', icon: IconPaperclip, roles: ['support_team_manager' ,'support_team_member'] },
    { route: 'file', label: 'File mangment', icon: IconPaperclip, roles: ['support_team_manager' ] },
];
