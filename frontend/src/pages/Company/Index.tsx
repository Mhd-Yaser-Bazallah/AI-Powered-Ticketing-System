import { useState } from "react";
import moment from "moment";
import toast from "react-hot-toast";
import { Delete as Delete_request, Get } from "../../Hooks/useCompany";
import { ChangeStatusAssign, ChangeStatusCategorize, ChangeStatusPrioritize } from "../../Hooks/useCompany";
import Delete from "../../components/Modal/Delete";
import Pagination from "../../components/Pagination/Pagination";
import { default as ButtonSkeleton } from '../../components/Skeleton/Button';
import { default as TableSkeleton } from '../../components/Skeleton/Table';
import Table from "../../components/Table";
import Add from "./Add";
import Edit from "./Edit";
import Default from "./Workflow/Default";
import Customize from "./Workflow/Customize";

const Index = () => {
    const [page, setPage] = useState(1);
    const Companys: any = Get(page);


    const [localAssign, setLocalAssign] = useState<{ [key: number]: boolean }>({});
    const [localCategorize, setLocalCategorize] = useState<{ [key: number]: boolean }>({});
    const [localPrioritize, setLocalPrioritize] = useState<{ [key: number]: boolean }>({});


    const assignMutation = ChangeStatusAssign();
    const categorizeMutation = ChangeStatusCategorize();
    const prioritizeMutation = ChangeStatusPrioritize();


    const handleToggle = (id: number, type: "assign" | "categorize" | "prioritize", newValue: boolean) => {

        if (type === "assign") setLocalAssign(prev => ({ ...prev, [id]: newValue }));
        if (type === "categorize") setLocalCategorize(prev => ({ ...prev, [id]: newValue }));
        if (type === "prioritize") setLocalPrioritize(prev => ({ ...prev, [id]: newValue }));


        const mutation: any =
            type === "assign"
                ? assignMutation
                : type === "categorize"
                    ? categorizeMutation
                    : prioritizeMutation;


        toast.promise(
            mutation.mutateAsync(id),
            {
                loading: 'Saving...',
                success: () => <b>Status updated!</b>,
                error: () => {

                    if (type === "assign") setLocalAssign(prev => ({ ...prev, [id]: !newValue }));
                    if (type === "categorize") setLocalCategorize(prev => ({ ...prev, [id]: !newValue }));
                    if (type === "prioritize") setLocalPrioritize(prev => ({ ...prev, [id]: !newValue }));
                    return <b>Could not update status.</b>;
                },
            }
        );
    };

    return (
        <>
            {Companys.isLoading && (
                <>
                    <ButtonSkeleton />
                    <TableSkeleton />
                </>
            )}
            {!Companys.isLoading && (
                <>
                    <Add />
                    <h4 className="text-[#3C9B94] font-serif text-lg text-center mb-4 border-b-2 border-[#3C9B94] pb-2 dark:border-yellow-600 dark:text-white">
                        Companies
                    </h4>

                    <Table
                        header={[
                            "id",
                            "Company Name",
                            "Email",
                            "Address",
                            "Work Flow",
                            "Auto Assign",
                            "Auto Categorize",
                            "Auto Prioritize",
                            "Created at",
                            "Actions"
                        ]}
                        body={
                            Companys?.data?.data?.results?.length === 0 ? (
                                <tr>
                                    <td colSpan={10} className="text-center">
                                        No Companies found
                                    </td>
                                </tr>
                            ) : (
                                Companys?.data?.data?.results?.map((item: any) => (
                                    <tr key={item.id}>
                                        <td>{item.id}</td>
                                        <td>{item.name}</td>
                                        <td>{item.email}</td>
                                        <td>{item.address}</td>


                                        <td className="flex justify-center items-center gap-2">
                                            <Default item={item} />
                                            <Customize item={item} />
                                        </td>


                                        <td className="text-center">
                                            <label className="w-12 h-6 relative inline-block">
                                                <input
                                                    type="checkbox"
                                                    className="absolute w-full h-full opacity-0 z-10 cursor-pointer peer"
                                                    checked={
                                                        localAssign[item.id] !== undefined
                                                            ? localAssign[item.id]
                                                            : item.auto_assign
                                                    }
                                                    onChange={(e) =>
                                                        handleToggle(item.id, "assign", e.target.checked)
                                                    }
                                                />
                                                <span className="outline_checkbox border-2 border-[#ebedf2] dark:border-white-dark block h-full rounded-full before:absolute before:left-1 before:bg-[#ebedf2] dark:before:bg-white-dark before:bottom-1 before:w-4 before:h-4 before:rounded-full peer-checked:before:left-7 peer-checked:border-success-400 peer-checked:before:bg-success-400 before:transition-all before:duration-300"></span>
                                            </label>
                                        </td>


                                        <td className="text-center">
                                            <label className="w-12 h-6 relative inline-block">
                                                <input
                                                    type="checkbox"
                                                    className="absolute w-full h-full opacity-0 z-10 cursor-pointer peer"
                                                    checked={
                                                        localCategorize[item.id] !== undefined
                                                            ? localCategorize[item.id]
                                                            : item.auto_categorize
                                                    }
                                                    onChange={(e) =>
                                                        handleToggle(item.id, "categorize", e.target.checked)
                                                    }
                                                />
                                                <span className="outline_checkbox border-2 border-[#ebedf2] dark:border-white-dark block h-full rounded-full before:absolute before:left-1 before:bg-[#ebedf2] dark:before:bg-white-dark before:bottom-1 before:w-4 before:h-4 before:rounded-full peer-checked:before:left-7 peer-checked:border-success-400 peer-checked:before:bg-success-400 before:transition-all before:duration-300"></span>
                                            </label>
                                        </td>


                                        <td className="text-center">
                                            <label className="w-12 h-6 relative inline-block">
                                                <input
                                                    type="checkbox"
                                                    className="absolute w-full h-full opacity-0 z-10 cursor-pointer peer"
                                                    checked={
                                                        localPrioritize[item.id] !== undefined
                                                            ? localPrioritize[item.id]
                                                            : item.auto_prioritize
                                                    }
                                                    onChange={(e) =>
                                                        handleToggle(item.id, "prioritize", e.target.checked)
                                                    }
                                                />
                                                <span className="outline_checkbox border-2 border-[#ebedf2] dark:border-white-dark block h-full rounded-full before:absolute before:left-1 before:bg-[#ebedf2] dark:before:bg-white-dark before:bottom-1 before:w-4 before:h-4 before:rounded-full peer-checked:before:left-7 peer-checked:border-success-400 peer-checked:before:bg-success-400 before:transition-all before:duration-300"></span>
                                            </label>
                                        </td>

                                        <td>{moment(item.created_at).format("YY-MM-DD")}</td>


                                        <td className="flex justify-center items-center gap-2">
                                            <Edit data={item} />
                                            <Delete
                                                id={item.id}
                                                query_name={Delete_request}
                                                label_of_button="Delete"
                                                title="delete this Company!"
                                            />
                                        </td>
                                    </tr>
                                ))
                            )
                        }
                    />
                </>
            )}
            <div className="mt-2">
                <Pagination
                    totalPages={Companys?.data?.data?.total_pages}
                    currentPage={page}
                    onPageChange={setPage}
                />
            </div>
        </>
    );
};

export default Index;
