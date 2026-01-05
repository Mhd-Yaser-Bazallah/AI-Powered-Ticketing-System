import { Dialog, Transition } from '@headlessui/react';
import { Fragment, useState } from 'react';
import IconTrashLines from '../Icon/IconTrashLines';
import IconX from '../Icon/IconX';
import Delete_request from '../Request/Delete_request';

const Modal = ({ title, query_name, label_of_button, id ,query_title }: any) => {
    const [modalOpen, setModalOpen] = useState(false);
    return (
        <>
            <div>
                <button onClick={(e: any) => {
                    e.preventDefault()
                    setModalOpen(true)
                }} type="button" className="btn btn-outline-danger  rounded-lg   border-none">
                    Delete
                </button>
                <Transition appear show={modalOpen} as={Fragment}>
                    <Dialog as="div" open={modalOpen} onClose={() => setModalOpen(false)}>
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
                        <div id="slideIn_down_modal" className="fixed inset-0 z-[999] overflow-y-auto bg-[black]/60">
                            <div className="flex min-h-screen items-start justify-center px-4">
                                <Dialog.Panel className="panel animate__animated animate__slideInDown my-8 w-full max-w-lg overflow-hidden rounded-lg border-0 p-0 text-black dark:text-white-dark">
                                    <div className="flex items-center justify-between bg-[#fbfbfb] px-5 py-3 dark:bg-[#121c2c]">
                                        <h5 className="text-lg font-bold">{title}</h5>
                                        <button onClick={() => setModalOpen(false)} type="button" className="text-white-dark hover:text-dark">
                                            <IconX />
                                        </button>
                                    </div>
                                    <div className="p-5">
                                        <div className="flex items-center p-3.5 rounded text-danger bg-danger-light dark:bg-danger-dark-light">
                                            <span className="ltr:pr-2 rtl:pl-2">Are you sure you want to {title}?</span>
                                        </div>
                                        <div className="mt-8 flex items-center justify-end">
                                            <button type="button" className="btn btn-outline-dark" onClick={() => setModalOpen(false)}>
                                                Cancel
                                            </button>
                                            <Delete_request query_name={query_name} query_title={query_title} setModalState={setModalOpen} label_of_button={label_of_button} id={id} />
                                        </div>
                                    </div>
                                </Dialog.Panel>
                            </div>
                        </div>
                    </Dialog>
                </Transition>
            </div>
        </>
    );
};

export default Modal;
