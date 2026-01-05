import { useState } from "react";
import { Delete as Delete_request, Get } from "../../Hooks/useUser";
import Delete from "../../components/Modal/Delete";
import Pagination from "../../components/Pagination/Pagination";
import { default as ButtonSkeleton } from '../../components/Skeleton/Button';
import { default as TableSkeleton } from '../../components/Skeleton/Table';
import Table from "../../components/Table";
import Add from "./Add";
import Edit from "./Edit";
import moment from "moment";
const Index = () => {
    const [page, setPage] = useState(1)
    const Users: any = Get(page);
    return (
        <>
            {Users.isLoading && (
                <>
                    <ButtonSkeleton />
                    <TableSkeleton />
                </>
            )}
            {!Users.isLoading && (
                <>
                    <Add />
                    <h4 className="text-[#3C9B94] font-serif text-lg text-center mb-4 border-b-2 border-[#3C9B94] pb-2 dark:border-yellow-600 dark:text-white">
                        Users
                    </h4>
                    <Table
                        header={[
                            "id",
                            "User Name",
                            "Email",
                            "Role",
                            "Phone Number",
                            "Created at",
                        ]}
                        body={
                            Users?.data?.data?.results?.length === 0 ? (
                                <tr>
                                    <td colSpan={7} className="text-center">
                                        No Users found
                                    </td>
                                </tr>
                            ) : (
                                Users?.data?.data?.results?.map((item: any) => {
                                    return (
                                        <tr key={item.id}>
                                            <td>{item.id}</td>
                                            <td>{item.username}</td>
                                            <td>{item.email}</td>
                                            <td>{item.role}</td>
                                            <td>{item.phone_number}</td>
                                            <td>{moment(item.created_at).format('YY-MM-DD')}</td>
                                            <td className="flex justify-center">
                                            </td>
                                            <div className="flex justify-center ">
                                                <td className="flex justify-center items-center">
                                                    <Edit data={item} />
                                                </td>
                                                <td className="flex justify-center items-center">
                                                    <Delete id={item?.id} query_name={Delete_request} label_of_button="Delete" title="delete this User!" />
                                                </td>
                                            </div>
                                        </tr>
                                    );
                                })
                            )
                        }
                    />
                </>
            )}
            <div className="mt-2">
                <Pagination totalPages={Users?.data?.data?.total_pages} currentPage={page} onPageChange={setPage} />
            </div>
        </>
    );
}
export default Index;
