import { Dialog, Transition } from '@headlessui/react';
import { Fragment, useState } from 'react';
import IconPlus from '../../components/Icon/IconPlus';
import IconX from '../Icon/IconX';

const AddModal = ({ form, title, modal, setModal }: any) => {

    return (
        <>
            <div className='w-full flex justify-end'>
                <button type="button" onClick={() => setModal(true)} className="btn  bg-[#3C9B94] hover:bg-[#000] text-white " style={{ textAlign: 'right' }}>
                    <IconPlus className="ltr:mr-2 rtl:ml-2" />
                    {title}
                </button>
            </div>
            <Transition appear show={modal} as={Fragment}>
                <Dialog as="div" open={modal} onClose={() => setModal(false)}>
                    <Transition.Child as={Fragment} enter="ease-out duration-300" enterFrom="opacity-0" enterTo="opacity-100" leave="ease-in duration-200" leaveFrom="opacity-100" leaveTo="opacity-0">
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
                                <Dialog.Panel as="div" className="panel my-8 w-full max-w-lg overflow-hidden rounded-lg border-0 p-0 text-black dark:text-white-dark">
                                    <div className="flex items-center justify-between bg-[#fbfbfb] px-5 py-3 dark:bg-[#121c2c]">
                                        <div className="text-lg font-bold">{title}</div>
                                        <button type="button" className="text-white-dark hover:text-dark" onClick={() => setModal(false)}>
                                            <IconX />
                                        </button>
                                    </div>
                                    <div className="p-5">
                                        <div className="flex items-center p-3.5 rounded  w-full dark:bg-warning-dark-light">
                                            {form}
                                        </div>
                                    </div>
                                </Dialog.Panel>
                            </Transition.Child>
                        </div>
                    </div>
                </Dialog>
                {/*  */}
            </Transition>





        </>
    );
};

export default AddModal;
