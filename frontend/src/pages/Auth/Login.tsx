import { useState } from 'react';
import img1 from "../../assets/onboardingLogin.webp";
import img2 from "../../assets/onboardingReg.webp";
import LoginForm from './Form';
import SignUpForm from './Signup';
import { DrawerAi } from '../../components/drawer/DrawerAi';

const Login = () => {
    const [isFlipped, setIsFlipped] = useState(false);

    const handleFlip = () => setIsFlipped(!isFlipped);

    return (
        <div className="relative">
            <div className={`card-container ${isFlipped ? 'flipped' : ''}`}>
                {/* Front Side (Login) */}
                <div className="w-full card-front">
                    <div className="flex bg-white h-[100vh]">
                        <div className="flex items-center px-8 text-center lg:text-left md:px-12 lg:w-1/2">
                            <div>
                                <h2 className="text-3xl font-semibold text-gray-800 md:text-4xl">
                                    Welcome Back <span className="text-[#13436A]">Login</span>
                                </h2>
                                <p className="mt-2 mb-5 text-center text-sm text-gray-500 md:text-base">
                                    Please login to access your account.
                                </p>
                                <LoginForm />
                                <button
                                    onClick={handleFlip}
                                    className="px-4 py-3 text-xs w-full font-semibold text-gray-200 bg-gray-900 rounded hover:bg-gray-800 mt-6"
                                >
                                    Go to Register
                                </button>
                            </div>
                        </div>
                        <div className="hidden lg:block lg:w-full" style={{ clipPath: 'polygon(10% 0, 100% 0%, 100% 100%, 0 100%)' }}>
                            <div className="object-cover h-full" style={{ backgroundImage: `url(${img1})`, backgroundSize: "100% 100%", backgroundRepeat: "no-repeat" }}>
                                <div className="h-full bg-black opacity-25"></div>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Back Side (Register) */}
                <div className="w-full card-back">
                    <div className="flex bg-white h-[100vh]">
                        <div className="flex items-center px-8 text-center lg:text-left md:px-12 lg:w-1/2">
                            <div>
                                <h2 className="text-3xl font-semibold text-gray-800 md:text-4xl">
                                    Join Us <span className="text-[#13436A]">Register</span>
                                </h2>
                                <p className="mt-2 text-sm text-gray-500 md:text-base">
                                    Create an account to enjoy all the features.
                                </p>
                                <SignUpForm setIsFlipped={setIsFlipped} />
                                <button
                                    onClick={handleFlip}
                                    className="px-4 py-3 w-full text-xs font-semibold text-gray-200 bg-gray-900 rounded hover:bg-gray-800 mt-6"
                                >
                                    Go to Login
                                </button>
                            </div>
                        </div>
                        <div className="hidden lg:block lg:w-full" style={{ clipPath: 'polygon(10% 0, 100% 0%, 100% 100%, 0 100%)' }}>
                            <div className="object-cover h-full" style={{ backgroundImage: `url(${img2})`, backgroundSize: "100% 100%", backgroundRepeat: "no-repeat" }}>
                                <div className="h-full bg-black opacity-25"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Login;
