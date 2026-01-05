import { PropsWithChildren, useEffect, useState } from 'react';
import { Toaster } from 'react-hot-toast';
import App from '../../App';
import Loading from '../Splash/SplashScreen';
import { DrawerAi } from '../drawer/DrawerAi';
const BlankLayout = ({ children }: PropsWithChildren) => {
    const [isLoad, setLoad] = useState(true);
    useEffect(() => {
        const timer = setTimeout(() => {
            setLoad(false);
        }, 3000);
        return () => clearTimeout(timer);
    }, []);

    return (
        <>
            {isLoad ? (
                <Loading />
            ) : (
                <App>
                    <Toaster />
                    <div className="text-black dark:text-white-dark min-h-screen">{children}           
                          <DrawerAi /></div>
                </App>
            )}
        </>
    );
};

export default BlankLayout;
