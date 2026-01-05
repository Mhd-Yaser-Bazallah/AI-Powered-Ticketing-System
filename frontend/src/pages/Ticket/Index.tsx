import { useEffect, useState, useRef } from "react";
import { ReactSortable } from "react-sortablejs";
import { APIInstance } from "../../services/APIs/Ticket";
import TicketCard from "../../components/TicketCard/TicketCard";
import toast from "react-hot-toast";
import StatusModal from "../../components/Modal/Status";
import { SelectInput } from "../../components/Input/Select";
import { useLocation } from "react-router-dom";

const KanbanBoard = ({
  fakeTickets,
  onTicketUpdate,
}: {
  fakeTickets: any[];
  onTicketUpdate?: (ticket: any) => void;
}) => {
 
  useEffect(() => {
    console.log("Received Tickets in KanbanBoard:", fakeTickets);
  }, [fakeTickets]);
  
  const userId = sessionStorage.getItem("id");
  const company_id = sessionStorage.getItem("company_id") ?? 1;

  const [columns, setColumns] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const columnsRef = useRef(columns);

  useEffect(() => {
    const fetchWorkflow = async () => {
      try {
        const response = await APIInstance.WorkFlowBoard(Number(company_id));
        const steps = response?.data?.steps || [];

        const formattedSteps = steps.map((step: any) => ({
          id: step.id,
          name: step.name,
          tasks: fakeTickets.filter((ticket) => ticket.status === step.name),
        }));

        setColumns(formattedSteps);
        columnsRef.current = formattedSteps;
      } catch (error) {
        console.error("Error fetching workflow:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchWorkflow();
  }, [fakeTickets, company_id]);

  useEffect(() => {
    columnsRef.current = columns;
  }, [columns]);
  const handleDrag = async (
    draggedTicket: any,
    fromColumnId: number,
    toColumnId: number
  ) => {
    const prevState = [...columnsRef.current];

    const fromIndex = prevState.findIndex((col) => col.id === fromColumnId);
    const toIndex = prevState.findIndex((col) => col.id === toColumnId);

    if (toIndex !== fromIndex + 1) {
      toast.error("not allowed to move");

      setColumns([...prevState]);
      columnsRef.current = [...prevState];
      console.log(prevState);
      return false;
    }

    const toColumn = prevState[toIndex];
    const toStatus = toColumn?.name;
    if (!toStatus) return false;

    const updatedFromTasks = prevState[fromIndex].tasks.filter(
      (task: any) => task.id !== draggedTicket.id
    );

    const existsInToColumn = prevState[toIndex].tasks.some(
      (task: any) => task.id === draggedTicket.id
    );

    const updatedToTasks = existsInToColumn
      ? prevState[toIndex].tasks
      : [...prevState[toIndex].tasks, { ...draggedTicket, status: toStatus }];

    const newColumns = prevState.map((col) => {
      if (col.id === fromColumnId) return { ...col, tasks: updatedFromTasks };
      if (col.id === toColumnId) return { ...col, tasks: updatedToTasks };
      return col;
    });

    setColumns(newColumns);
    columnsRef.current = newColumns;

    try {
      const res = await APIInstance.MoveTicket(draggedTicket.id, {
        user_id: userId,
        status: toStatus,
      });
      toast.success(res?.message || "تم النقل");
      return true;
    } catch (err: any) {
      setColumns(prevState);
      columnsRef.current = prevState;
      toast.error(err?.response?.data?.message || err.message || "فشل في النقل");
      return false;
    }
  };

  if (loading) return <div>جاري التحميل...</div>;

  return (
    <>
      {sessionStorage.getItem('role') !== 'client' ?
        <div className="grid sm:grid-cols-5 gap-5 pb-2 px-2">
          {columns?.map((column, colIndex) => (
            <div
              key={column.id}
              data-group={column.id}
              className="panel bg-neutral-100 shadow-lg h-[600px] overflow-auto flex-none"
            >
              <h4 className="text-lg font-semibold text-center text-[#0b1111] mb-5">
                {column.name}
              </h4>
              <ReactSortable
                list={column.tasks}
                setList={(newList) => {
                  const updatedColumns = [...columns];
                  updatedColumns[colIndex].tasks = newList;
                  setColumns(updatedColumns);
                  columnsRef.current = updatedColumns;
                }}
                animation={200}
                group={{ name: "shared", pull: true, put: true }}
                ghostClass="sortable-ghost"
                dragClass="sortable-drag"
                className="min-h-[150px] space-y-3 px-2"
                onMove={(evt, originalEvent) => {
                  const fromCol = evt.from.closest("[data-group]");
                  const toCol = evt.to.closest("[data-group]");

                  const fromColId = Number(fromCol?.getAttribute("data-group"));
                  const toColId = Number(toCol?.getAttribute("data-group"));

                  const fromIndex = columnsRef.current.findIndex((col) => col.id === fromColId);
                  const toIndex = columnsRef.current.findIndex((col) => col.id === toColId);

                  if (toIndex !== fromIndex + 1) {
                    return false;
                  }

                  return true;
                }}
                onEnd={async (evt) => {
                  if (!evt.from || !evt.to) return;

                  const fromColId = Number(evt.from.closest("[data-group]")?.getAttribute("data-group"));
                  const toColId = Number(evt.to.closest("[data-group]")?.getAttribute("data-group"));

                  const itemEl = evt.item;
                  const draggedId = Number(itemEl?.getAttribute("data-id"));

                  const draggedTicket = columnsRef.current
                    .flatMap((col) => col.tasks)
                    .find((task) => task.id === draggedId);

                  if (draggedTicket) {
                    await handleDrag(draggedTicket, fromColId, toColId);
                  }
                }}
              >
                {column.tasks.map((task: any) => (
                  <div key={task.id} data-id={task.id}>
                    <TicketCard ticket={task} onTicketUpdate={onTicketUpdate} />
                  </div>
                ))}
              </ReactSortable>
            </div>
          ))}
        </div>
        :
        <>
          <h4 className="text-[#3C9B94] font-serif text-lg text-center mb-4 border-b-2 border-[#3C9B94] pb-2 dark:border-yellow-600 dark:text-white">
            Tickets
          </h4>
          <div className="w-full bg-white p-5 rounded-lg mt-2 shadow-lg grid sm:grid-cols-4 gap-5">
            {columns?.map((project) => (
              project.tasks.map((task: any) => (
                <TicketCard key={task.id} ticket={task} onTicketUpdate={onTicketUpdate} />
              ))
            ))}
          </div>
        </>

      }



    </>
  );
};

export default KanbanBoard;
