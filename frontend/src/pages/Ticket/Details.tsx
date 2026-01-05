import React, { useState } from 'react';
import moment from 'moment';
import IconMessagesDot from '../../components/Icon/IconMessagesDot';
import DetailsModal from '../../components/Modal/Details';
import IconMenuApps from '../../components/Icon/Menu/IconMenuApps';
import IconDroplet from '../../components/Icon/IconDroplet';

const Details = (props: any) => {
    const [modal, setModal] = useState(false);
    const data = props?.data || {};

    const handleOpenModal = () => setModal(true);
    const handleCloseModal = () => setModal(false);

    return (
        <>
            {/* Trigger Button */}
            <button
                onClick={handleOpenModal}
                type="button"
                className="btn btn-outline-success rounded-lg border-none"
            >
                Details
            </button>

            {/* Details Modal */}
            <DetailsModal
                setModal={handleCloseModal}
                modal={modal}
                form={
                    <div className="bg-gradient-to-r from-blue-50 to-white p-8  w-full rounded-lg ">
                        {/* Title Section */}
                        <div className="border-b pb-4 mb-6">
                            <h2 className="text-3xl font-extrabold text-blue-800">
                                Ticket Details
                            </h2>
                            <p className="text-sm text-gray-500">
                                Created on {moment(data.created_at).format('YYYY-MM-DD HH:mm')}
                            </p>
                        </div>

                        {/* Information Grid */}
                        <div className="grid grid-cols-2 gap-6">
                            {/* Category */}
                            <div className="flex flex-col">
                                <span className="text-sm font-medium text-gray-600">Category</span>
                                <span className="text-lg font-semibold text-gray-800">
                                    {data.category || 'N/A'}
                                </span>
                            </div>

                            {/* Priority */}
                            <div className="flex flex-col">
                                <span className="text-sm font-medium text-gray-600">Priority</span>
                                <span
                                    className={`text-lg font-semibold ${data.priority === 'high'
                                        ? 'text-red-600'
                                        : data.priority === 'medium'
                                            ? 'text-yellow-600'
                                            : 'text-green-600'
                                        }`}
                                >
                                    {data.priority || 'N/A'}
                                </span>
                            </div>

                            {/* Status */}
                            <div className="flex flex-col">
                                <span className="text-sm font-medium text-gray-600">Status</span>
                                <span
                                    className={`text-lg font-semibold ${data.status === 'open'
                                        ? 'text-blue-600'
                                        : 'text-gray-600'
                                        }`}
                                >
                                    {data.status || 'N/A'}
                                </span>
                            </div>

                            {/* Client */}
                            <div className="flex flex-col">
                                <span className="text-sm font-medium text-gray-600">Client</span>
                                <span className="text-lg font-semibold text-gray-800">
                                    {data.client || 'N/A'}
                                </span>
                            </div>

                            {/* Company */}
                            <div className="flex flex-col">
                                <span className="text-sm font-medium text-gray-600">Company</span>
                                <span className="text-lg font-semibold text-gray-800">
                                    {data.company || 'N/A'}
                                </span>
                            </div>
                        </div>

                        {/* Description */}
                        <div className="mt-6">
                            <h3 className="text-xl font-bold text-gray-700">Description</h3>
                            <p className="text-gray-600 mt-2 leading-relaxed">
                                {data.description || 'No description provided.'}
                            </p>
                        </div>

                        {/* Title */}
                        <div className="mt-4">
                            <h3 className="text-xl font-bold text-gray-700">Title</h3>
                            <p className="text-gray-600 mt-2 leading-relaxed">{data.title || 'N/A'}</p>
                        </div>

                    </div>
                }
            />
        </>
    );
};

export default Details;
