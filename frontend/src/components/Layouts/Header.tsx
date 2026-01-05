import { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useDispatch, useSelector } from 'react-redux';
import { Link, Navigate, useLocation, useNavigate } from 'react-router-dom';
import NoImage from "../../assets/NoImage.png";
import { IRootState } from '../../store';
import { toggleSidebar } from '../../store/themeConfigSlice';
import Dropdown from '../Dropdown';
import IconLogout from '../Icon/IconLogout';
import IconMenu from '../Icon/IconMenu';
import Logout from '../Modal/Logout';
import { AuthInstance } from '../../services/APIs/Auth';
import {Notification} from './Notification';

const Header = () => {
    const location = useLocation();
    
    const [modal, setModal] = useState(false);
    useEffect(() => {
        const selector = document.querySelector('ul.horizontal-menu a[href="' + window.location.pathname + '"]');
        if (selector) {
            selector.classList.add('active');
            const all: any = document.querySelectorAll('ul.horizontal-menu .nav-link.active');
            for (let i = 0; i < all.length; i++) {
                all[0]?.classList.remove('active');
            }
            const ul: any = selector.closest('ul.sub-menu');
            if (ul) {
                let ele: any = ul.closest('li.menu').querySelectorAll('.nav-link');
                if (ele) {
                    ele = ele[0];
                    setTimeout(() => {
                        ele?.classList.add('active');
                    });
                }
            }
        }
    }, [location]);


    const themeConfig = useSelector((state: IRootState) => state.themeConfig);
    const dispatch = useDispatch();


    const { t } = useTranslation();
    const [photo]: any = useState(NoImage)
    const navigate = useNavigate()

    const logout = async () => {
        AuthInstance.Logout()
        await navigate('/')
        sessionStorage.clear()

    }
  
    return (
        <>
            <header className={`z-40 ${themeConfig.menu === 'horizontal' ? 'dark' : ''}`}>
                <div className="shadow-sm">
                    <div className="relative bg-white flex w-full items-center px-5 py-2.5 dark:bg-black">
                        <div className="horizontal-logo flex lg:hidden justify-between items-center ltr:mr-2 rtl:ml-2">
                            <Link to="/" className="main-logo flex items-center shrink-0">
                                {/* <img className="w-8 ltr:-ml-1 rtl:-mr-1 inline" src={Logo} alt="logo" /> */}
                                <span className="text-2xl ltr:ml-1.5 rtl:mr-1.5  font-semibold  align-middle hidden md:inline dark:text-white-light transition-all duration-300">AI Ticketing</span>
                            </Link>
                            <button
                                type="button"
                                className="collapse-icon flex-none dark:text-[#d0d2d6] hover:text-primary dark:hover:text-primary flex lg:hidden ltr:ml-2 rtl:mr-2 p-2 rounded-full bg-white-light/40 dark:bg-dark/40 hover:bg-white-light/90 dark:hover:bg-dark/60"
                                onClick={() => {
                                    dispatch(toggleSidebar());
                                }}
                            >
                                <IconMenu className="w-5 h-5" />
                            </button>
                        </div>

                        <div className="ltr:mr-2 rtl:ml-2 hidden sm:block"></div>
                        <div className="sm:flex-1 ltr:sm:ml-0 ltr:ml-auto sm:rtl:mr-0 rtl:mr-auto flex items-center space-x-1.5 lg:space-x-2 rtl:space-x-reverse dark:text-[#d0d2d6]">
                            <div className="sm:ltr:mr-auto sm:rtl:ml-auto"></div>
                            <Notification/>

                            <div className="dropdown shrink-0 flex">
                                <Dropdown
                                    offset={[0, 8]}
                                    placement={'bottom-end'}
                                    btnClassName="relative group block"
                                    button={<img className="w-9 h-9 rounded-full object-cover saturate-50 group-hover:saturate-100"
                                        src={photo}
                                    />}
                                >
                                    <ul className="text-dark dark:text-white-dark !py-0 w-[230px] font-semibold dark:text-white-light/90">
                                        <li>
                                            <div className="flex items-center px-4 py-4">
                                                <img className="rounded-md w-10 h-10 object-cover" src={photo} alt="userProfile" />
                                                <div className="ltr:pl-4 rtl:pr-4 truncate">
                                                </div>
                                            </div>
                                        </li>
                                        <li className="border-t border-white-light dark:border-white-light/10 cursor-pointer" onClick={() => logout()}>
                                            <a className="text-danger !py-3">
                                                <IconLogout className="w-4.5 h-4.5 ltr:mr-2 rtl:ml-2 rotate-90 shrink-0" />
                                                {t('Logout')}
                                            </a>
                                        </li>
                                    </ul>
                                </Dropdown>
                            </div>
                        </div>
                    </div>
                </div>
            </header>
            {modal && <Logout modal={modal} setModal={setModal} />}
        </>
    );
};

export default Header;
