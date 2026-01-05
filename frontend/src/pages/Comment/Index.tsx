import React, { useState } from "react";
import DetailsModal from "../../components/Modal/Details";
import { APIInstance } from "../../services/APIs/Comment";
import Add from "./Add";
import IconMessagesDot from "../../components/Icon/IconMessagesDot";

const Index = (props: any) => {
    const [modal, setModal] = useState(false);
    const [comments, setComments] = useState<any[]>([]);
    const [isLoading, setIsLoading] = useState(false);

    const fetchComments = async () => {
        setIsLoading(true);
        try {
            const response = await APIInstance.Get(props.data.id);
            setComments(response?.data || []);
        } catch (error) {
            console.error("Failed to fetch comments:", error);
        } finally {
            setIsLoading(false);
        }
    };

    const handleOpenModal = () => {
        setModal(true);
        fetchComments(); // Fetch comments when the modal opens
    };

    const handleCloseModal = () => {
        setModal(false);
    };

    // Callback to add a new comment to the list
    const handleAddComment = (newComment: any) => {
        setComments((prevComments) => [newComment, ...prevComments]);
    };

    return (
        <>
            {/* Trigger Button */}
            <button
                onClick={handleOpenModal}
                type="button"
                className="btn btn-outline-info rounded-lg border-none"
            >
               <IconMessagesDot className="hover:text-white" /> 
            </button>
            {/* Comments Modal */}
            <DetailsModal
                setModal={handleCloseModal}
                modal={modal}
                form={
                    <div className="flex flex-col w-full">
                        {isLoading ? (
                            <div className="text-center text-gray-500">Loading comments...</div>
                        ) : (
                            <>
                                {/* Comments List */}
                                <div className="space-y-6 max-h-[400px] overflow-y-auto pr-2">
                                    {comments.map((comment: any) => (
                                        <div
                                            key={comment.id}
                                            className="flex items-start space-x-4 bg-gray-50 p-4 rounded-lg shadow-md"
                                        >
                                            {/* User Avatar */}
                                            <div className="w-12 h-12 rounded-full bg-blue-500 text-white flex items-center justify-center font-bold text-lg">
                                                {comment.username?.charAt(0) || "U"}
                                            </div>

                                            {/* Comment Details */}
                                            <div className="flex-1">
                                                <div className="flex justify-between items-center">
                                                    <h3 className="font-medium text-gray-900">
                                                        {comment.username || "Unknown User"}
                                                    </h3>
                                                    <span className="text-xs text-gray-500">
                                                        {new Date(comment.created_at).toLocaleDateString()}
                                                    </span>
                                                </div>
                                                <p className="text-gray-700 mt-2">{comment.description}</p>
                                            </div>
                                        </div>
                                    ))}
                                </div>

                                {/* Add New Comment */}
                                <div className="mt-6">
                                    <Add data={props} onAddComment={handleAddComment} />
                                </div>
                            </>
                        )}
                    </div>
                }
            />
        </>
    );
};

export default Index;
