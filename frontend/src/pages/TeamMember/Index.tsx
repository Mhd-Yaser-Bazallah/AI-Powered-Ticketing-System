import { useState } from "react";
import toast from "react-hot-toast";
import { ChangeStatus, Get, changeStatusMutationToDeActivate } from "../../Hooks/useTeamMember";
import Pagination from "../../components/Pagination/Pagination";
import { default as ButtonSkeleton } from '../../components/Skeleton/Button';
import { default as TableSkeleton } from '../../components/Skeleton/Table';
import Table from "../../components/Table";
import Add from "./Add";
import Edit from "./Edit";
import moment from "moment";
const Index = () => {
    const [page, setPage] = useState(1)
    let company_id =sessionStorage.getItem("company_id")
    const TeamMembers: any = Get(company_id,page);
    const [localStatuses, setLocalStatuses] = useState<{ [key: number]: boolean }>({});
    const changeStatusMutation = ChangeStatus();
    const changeStatusMutationTodeActivate = changeStatusMutationToDeActivate();
    const handleStatusChange = (teamMemId: any, active: boolean) => {
        setLocalStatuses((prevStatuses) => ({
            ...prevStatuses,
            [teamMemId]: active,
        }));

        toast.promise(
            active ? 
                changeStatusMutation.mutateAsync(teamMemId)
                :
                changeStatusMutationTodeActivate.mutateAsync(teamMemId),
            
                {
                loading: 'Saving...',
                success: () => {
                    return <b>Status updated!</b>;
                },
                error: () => {
                    setLocalStatuses((prevStatuses) => ({
                        ...prevStatuses,
                        [teamMemId]: !active,
                    }));
                    return <b>Could not update status.</b>;
                },
            }
        );
    };




    return (
        <>
            {TeamMembers.isLoading && (
                <>
                    <ButtonSkeleton />
                    <TableSkeleton />
                </>
            )}
            {!TeamMembers.isLoading && (
                <>
                    <Add />
                    <h4 className="text-[#3C9B94] font-serif text-lg text-center mb-4 border-b-2 border-[#3C9B94] pb-2 dark:border-yellow-600 dark:text-white">
                        Team Members
                    </h4>
                    <Table
                        header={[
                            "id",
                            "username",
                            "email",
                            "phone number",
                            "team",
                            "Activate",
                            "Created at",
                        ]}
                        body={
                            TeamMembers?.data?.data?.results?.length === 0 ? (
                                <tr>
                                    <td colSpan={8} className="text-center">
                                        No TeamMembers found
                                    </td>
                                </tr>
                            ) : (
                                TeamMembers?.data?.data?.results?.map((item: any) => {
                                    return (
                                        <tr key={item.id}>
                                            <td>{item.id}</td>
                                            <td>{item.username}</td>
                                            <td>{item.email}</td>
                                            <td>{item.phone_number}</td>
                                            <td>{item.team_name}</td>
                                            <div className="flex justify-center ">
                                                <td className="flex justify-center items-center">
                                                    <label className="w-12 h-6 relative">
                                                        <input
                                                            type="checkbox"
                                                            className="custom_switch absolute w-full h-full opacity-0 z-10 cursor-pointer peer"
                                                            checked={localStatuses[item.id] !== undefined ? localStatuses[item.id] : item.active}
                                                            onChange={(e) => handleStatusChange(item.id, e.target.checked)}
                                                        />
                                                        <span className="outline_checkbox border-2 border-[#ebedf2] dark:border-white-dark block h-full rounded-full before:absolute before:left-1 before:bg-[#ebedf2] dark:before:bg-white-dark before:bottom-1 before:w-4 before:h-4 before:rounded-full peer-checked:before:left-7 peer-checked:border-success-400 peer-checked:before:bg-success-400 before:transition-all before:duration-300"></span>
                                                    </label>
                                                </td>
                                            </div>
                                            <td>{moment(item.created_at).format('YY-MM-DD')}</td>
                                            <td>
                                                <Edit data={item} />
                                            </td>
                                           
                                        </tr>
                                    );
                                })
                            )
                        }
                    />
                </>
            )}
            <div className="mt-2">
                <Pagination totalPages={TeamMembers?.data?.data?.total_pages} currentPage={page} onPageChange={setPage} />
            </div>
        </>
    );
}
export default Index;
