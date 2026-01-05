import React, { useState } from 'react';
import Status from '../../../components/Modal/Status';
import { useFormik } from 'formik';
import toast from 'react-hot-toast';
import { APIInstance } from '../../../services/APIs/Company';

interface DefaultProps {
    item: any;
}

const Default: React.FC<DefaultProps> = (props) => {
    const [modal, setModal] = useState(false);

    const formik = useFormik({
        initialValues: {
            company: props.item?.id,
            created_by: sessionStorage.getItem("id"),
        },
        onSubmit: async (values) => {
            toast.promise(APIInstance.AddWorkflowDefault(values), {
                loading: 'Saving...',
                success: 'Workflow added successfully!',
                error: 'Failed to add workflow',
            });
            setModal(false);
        },
    });

    return (
        <>
            <button
                onClick={() => setModal(true)}
                className="bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600"
            >
                Set Default
            </button>

            <Status modal={modal} setModal={setModal}>
                <form onSubmit={formik.handleSubmit}>
                    <div className="flex justify-end mt-4">
                        <button
                            type="submit"
                            className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
                        >
                            Confirm
                        </button>
                    </div>
                </form>
            </Status>
        </>
    );
};

export default Default;
