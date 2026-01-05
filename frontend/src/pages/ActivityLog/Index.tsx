import { useState } from "react";
import { Get } from "../../Hooks/useLogs";
import Delete from "../../components/Modal/Delete";
import Pagination from "../../components/Pagination/Pagination";
import { default as ButtonSkeleton } from '../../components/Skeleton/Button';
import { default as TableSkeleton } from '../../components/Skeleton/Table';
import Table from "../../components/Table";
import moment from "moment";
const Index = () => {
    const [page, setPage] = useState(1)
    let id = sessionStorage.getItem('company_id')
    const Logss: any = Get(id, page);

    return (
        <>
            {Logss.isLoading && (
                <>
                    <ButtonSkeleton />
                    <TableSkeleton />
                </>
            )}
            {!Logss.isLoading && (
                <>
                    <h4 className="text-[#3C9B94] font-serif text-lg text-center mb-4 border-b-2 border-[#3C9B94] pb-2 dark:border-yellow-600 dark:text-white">
                        Logss
                    </h4>
                    <Table
                        header={[
                            "comments",
                            "created_at",
                            "new_status",
                            "previous_status",
                        ]}
                        body={
                            Logss?.data?.data?.results?.length === 0 ? (
                                <tr>
                                    <td colSpan={5} className="text-center">
                                        No Logss found
                                    </td>
                                </tr>
                            ) : (
                                Logss?.data?.data?.results?.map((item: any) => {
                                    return (
                                        <tr key={item.id}>
                                            <td>{item.comments}</td>
                                            <td>{moment(item.created_at).format('YY-MM-DD')}</td>
                                            <td>{item.new_status}</td>
                                            <td>{item.previous_status}</td>
                                            <td className="text-center">{item.action}</td>
                                        </tr>
                                        // <></>
                                    );
                                })
                            )
                        }
                    />
                </>
            )}
            <div className="mt-2">
                <Pagination totalPages={Logss?.data?.data?.total_pages} currentPage={page} onPageChange={setPage} />
            </div>
        </>
    );
}
export default Index;
