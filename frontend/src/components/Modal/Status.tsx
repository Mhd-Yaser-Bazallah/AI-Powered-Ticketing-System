import { Dialog, Transition } from "@headlessui/react";
import { Fragment } from "react";
import IconX from "../Icon/IconX";

interface StatusProps {
    modal: boolean;
    setModal: (value: boolean) => void;
    children?: React.ReactNode;
    title?:string
    sectitle?:string
}

const Status: React.FC<StatusProps> = ({ modal, setModal, children  ,title ,sectitle}) => {
    return (
        <Transition appear show={modal} as={Fragment}>
            <Dialog as="div" open={modal} onClose={() => setModal(false)}>
                <Transition.Child
                    as={Fragment}
                    enter="ease-out duration-300"
                    enterFrom="opacity-0"
                    enterTo="opacity-100"
                    leave="ease-in duration-200"
                    leaveFrom="opacity-100"
                    leaveTo="opacity-0"
                >
                    <div className="fixed inset-0" />
                </Transition.Child>
                <div className="fixed inset-0 z-[999] overflow-y-auto bg-[black]/60">
                    <div className="flex min-h-screen items-center justify-center px-4">
                        <Transition.Child
                            as={Fragment}
                            enter="ease-out duration-300"
                            enterFrom="opacity-0 scale-95"
                            enterTo="opacity-100 scale-100"
                            leave="ease-in duration-200"
                            leaveFrom="opacity-100 scale-100"
                            leaveTo="opacity-0 scale-95"
                        >
                            <Dialog.Panel className="panel my-8 w-full max-w-lg overflow-hidden rounded-lg border-0 p-0 text-black dark:text-white-dark">
                                <div className="flex items-center justify-between bg-[#fbfbfb] px-5 py-3 dark:bg-[#121c2c]">
                                    <div className="text-lg font-bold">{title ? title : 'Status Change'}</div>
                                    <button
                                        type="button"
                                        className="text-white-dark hover:text-dark"
                                        onClick={() => setModal(false)}
                                    >
                                        <IconX />
                                    </button>
                                </div>
                                <div className="p-5">
                                    <div className="flex items-center p-3.5 rounded text-warning bg-warning-light dark:bg-warning-dark-light">
                                        <span className="ltr:pr-2 rtl:pl-2">
                                            {sectitle? sectitle :'Do you want to change the status?'}
                                            
                                        </span>
                                    </div>
                                    {children}
                                </div>
                            </Dialog.Panel>
                        </Transition.Child>
                    </div>
                </div>
            </Dialog>
        </Transition>
    );
};

export default Status;
