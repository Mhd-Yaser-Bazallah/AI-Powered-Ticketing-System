import { lazy } from 'react';
const Login = lazy(() => import('../pages/Auth/Login'));
const User = lazy(() => import('../pages/User/Index'));
const Ticket = lazy(() => import('../pages/Ticket/Ticket'));
const File = lazy(() => import('../pages/File/Index'));
const Company = lazy(() => import('../pages/Company/Index'));
const Report = lazy(() => import('../pages/Reports/Index'));
const Team = lazy(() => import('../pages/Team/Index'));
const Comment = lazy(() => import('../pages/Comment/Index'));
const TeamMembers = lazy(() => import('../pages/TeamMember/Index'));
const Profile = lazy(() => import('../pages/Profile/Index'));
const Logs = lazy(() => import('../pages/ActivityLog/Index'));
const PageNotFound = lazy(() => import('../pages/404/Index'));

const routes = [
    {
        path: '/', element: <Login />, layout: 'blank',
    },
    {
        path: '/profile',
        element: <Profile />,
        layout: 'default',
    },
    {
        path: '/user',
        element: <User />,
        layout: 'default',
    },
    {
        path: '/reporting',
        element: <Report />,
        layout: 'default',
    },
    {
        path: '/file',
        element: <File  />,
        layout: 'default',
    },
    {
        path: '/ticket',
        element: <Ticket />,
        layout: 'default',
    },
    {
        path: '/comments/:id',
        element: <Comment />,
        layout: 'default',
    },
    {
        path: '/logs',
        element: <Logs />,
        layout: 'default',
    },
    {
        path: '/team-ticket',
        element: <Ticket />,
        layout: 'default',
    },
    {
        path: '/Company',
        element: <Company />,
        layout: 'default',
    },
    {
        path: '/team',
        element: <Team />,
        layout: 'default',
    },
    {
        path: '/team-members',
        element: <TeamMembers />,
        layout: 'default',
    },
    {
        path: '/*', element: <PageNotFound />, layout: 'blank',
    },
];

export { routes };
