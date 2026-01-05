import { PropsWithChildren, Suspense, useEffect, useState } from 'react';
import { Toaster } from 'react-hot-toast';
import { useDispatch, useSelector } from 'react-redux';
import { Navigate, useNavigate } from 'react-router-dom';
import App from '../../App';
import Portals from '../../components/Portals';
import { IRootState } from '../../store';
import { toggleSidebar } from '../../store/themeConfigSlice';
import Header from './Header';
import Sidebar from './Sidebar';
import { Get } from '../../Hooks/useProfile';
import Loading from '../Splash/SplashScreen';
import { DrawerAi } from '../drawer/DrawerAi';

const DefaultLayout = ({ children }: PropsWithChildren) => {
    const navigate = useNavigate();
    const themeConfig = useSelector((state: IRootState) => state.themeConfig);
    const dispatch = useDispatch();

    const [showLoader, setShowLoader] = useState(true);
    const [showTopButton, setShowTopButton] = useState(false);

    const goToTop = () => {
        document.body.scrollTop = 0;
        document.documentElement.scrollTop = 0;
    };

    const onScrollHandler = () => {
        if (document.body.scrollTop > 50 || document.documentElement.scrollTop > 50) {
            setShowTopButton(true);
        } else {
            setShowTopButton(false);
        }
    };

    useEffect(() => {
        window.addEventListener('scroll', onScrollHandler);
        const screenLoader = document.getElementsByClassName('screen_loader');
        if (screenLoader?.length) {
            screenLoader[0].classList.add('animate__fadeOut');
            setTimeout(() => {
                setShowLoader(false);
            }, 200);
        }

        return () => {
            window.removeEventListener('scroll', onScrollHandler);
        };
    }, []);


    const getme = Get(sessionStorage?.getItem('id'))
    sessionStorage.setItem('company_id', getme?.data?.data?.company_id)
    sessionStorage.setItem('team_id', getme?.data?.data?.team_id)
    if (sessionStorage.getItem('token') == null || sessionStorage.getItem('token') === undefined) {
        return <Navigate to="/" />;
    } else
        return (
            <>
                {getme.isLoading ? <Loading /> :
                    <App>
                        <Toaster position="top-center" reverseOrder={true} />
                        <div className="relative">
                            <div className={`${(!themeConfig.sidebar && 'hidden') || ''} fixed inset-0 bg-[black]/60 z-50 lg:hidden`} onClick={() => dispatch(toggleSidebar())}></div>

                            <div className="fixed bottom-6 ltr:right-6 rtl:left-6 z-50">
                                {showTopButton && (
                                    <button type="button" className="btn btn-outline-primary rounded-full p-2 animate-pulse bg-[#fafafa] dark:bg-[#060818] dark:hover:bg-primary" onClick={goToTop}>
                                        <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="1.5">
                                            <path strokeLinecap="round" strokeLinejoin="round" d="M8 7l4-4m0 0l4 4m-4-4v18" />
                                        </svg>
                                    </button>
                                )}
                            </div>
                            <div className={`navbar-sticky main-container text-black dark:text-white-dark min-h-screen`}>
                                <Sidebar />
                                <div className="main-content flex flex-col min-h-screen">
                                    <Header />
                                    <Suspense>
                                        <div className={`animate__fadeIn bg-[#faf7f8] p-6 animate__animated`}>
                                            {children}
                                            <DrawerAi />
                                            </div>
                                    </Suspense>
                                    <Portals />
                                </div>
                            </div>
                        </div>
                    </App>

                }
   
            </>

        );
};

export default DefaultLayout;
