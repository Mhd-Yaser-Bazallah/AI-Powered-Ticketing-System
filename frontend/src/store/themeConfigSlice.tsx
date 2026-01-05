import { createSlice } from '@reduxjs/toolkit';
import i18next from 'i18next';
import themeConfig from '../theme.config';

const defaultState = {
    isDarkMode: false,
    mainLayout: 'app',
    theme: 'light',
    layout: 'full',
    rtlClass: 'ltr',
    locale: 'en',
    sidebar: false,
    pageTitle: '',
    languageList: [{ code: 'en', name: 'English' }],
    semidark: false,
};

const initialState = {
    menu: localStorage.getItem('menu') || themeConfig.menu,
    rtlClass: localStorage.getItem('rtlClass') || themeConfig.rtlClass,
    locale: localStorage.getItem('i18nextLng') || themeConfig.locale,
    isDarkMode: false,
    sidebar: localStorage.getItem('sidebar') || defaultState.sidebar,
    languageList: [{ code: 'en', name: 'English' },],
};

const themeConfigSlice = createSlice({
    name: 'auth',
    initialState: initialState,
    reducers: {
        toggleRTL(state, { payload }) {
            payload = payload || state.rtlClass; // rtl, ltr
            localStorage.setItem('rtlClass', 'ltr');
        },
        toggleSidebar(state) {
            state.sidebar = !state.sidebar;
        },
        setPageTitle(state, { payload }) {
            document.title = `${payload} | ${i18next.t('Book Any Van Admin Panel')}`;
        },
    },
});

export const { toggleRTL, toggleSidebar, setPageTitle } = themeConfigSlice.actions;

export default themeConfigSlice.reducer;
