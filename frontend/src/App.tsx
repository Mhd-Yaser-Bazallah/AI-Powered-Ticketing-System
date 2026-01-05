import { PropsWithChildren, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import store, { IRootState } from './store';
import { toggleRTL } from './store/themeConfigSlice';

function App({ children }: PropsWithChildren) {
    const themeConfig = useSelector((state: IRootState) => state.themeConfig);
    const dispatch = useDispatch();

    useEffect(() => {
        dispatch(toggleRTL(localStorage.getItem('rtlClass') || themeConfig.rtlClass));
    }, [dispatch, themeConfig.menu, themeConfig.rtlClass, themeConfig.locale]);

    return (
        <div
            className={`${(store.getState().themeConfig.sidebar && 'toggle-sidebar') || ''} ${themeConfig.menu} ${themeConfig.rtlClass
                } main-section antialiased relative font-nunito text-sm font-normal`}
        >
            {children}
        </div>
    );
}

export default App;
