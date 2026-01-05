import React, { useEffect, useState } from "react";
import { useFormik } from "formik";
import { useLocation } from "react-router-dom";
import toast from "react-hot-toast";

import { GetAll as AllTeams } from "../../Hooks/useTeam";
import {
  AssginToMe,
  AssginToTicket,
  Delete as Delete_request,
  Edit as EditTicket,
} from "../../Hooks/useTicket";

import Loading from "../../components/Button/Loading";
import { SelectInput } from "../../components/Input/Select";
import Delete from "../../components/Modal/Delete";
import StatusModal from "../../components/Modal/Status";
import Index from "../../pages/Comment/Index";
import Details from "../../pages/Ticket/Details";
import Edit from "../../pages/Ticket/Edit";
import IconUserPlus from "../Icon/IconUserPlus";
import { APIInstance } from "../../services/APIs/Ticket";
import { canViewSolutionSteps } from "../../utils/permissions";
import { reloadAfterChange } from "../../utils/reload";

/* -------------------------------------------------------
   Reusable Button (Tailwind) for consistent action styling
-------------------------------------------------------- */
type ActionBtnProps = {
  label: string;
  onClick?: () => void;
  icon?: React.ReactNode;
  variant?: "primary" | "danger" | "secondary" | "ghost";
  title?: string;
  full?: boolean;
  type?: "button" | "submit";
  disabled?: boolean;
};

const ActionBtn = ({
  label,
  onClick,
  icon,
  variant = "primary",
  title,
  full = true,
  type = "button",
  disabled,
}: ActionBtnProps) => {
  const base =
    "inline-flex items-center justify-center gap-2 rounded-xl px-3 py-2 text-sm font-semibold transition " +
    "focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed";

  const variants: Record<string, string> = {
    primary: "bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-300 shadow-sm",
    danger: "bg-red-600 text-white hover:bg-red-700 focus:ring-red-300 shadow-sm",
    secondary:
      "bg-gray-100 text-gray-800 hover:bg-gray-200 focus:ring-gray-300 border border-gray-200",
    ghost:
      "bg-transparent text-blue-700 hover:bg-blue-50 focus:ring-blue-200 border border-blue-100",
  };

  return (
    <button
      type={type}
      title={title}
      onClick={onClick}
      disabled={disabled}
      className={`${base} ${variants[variant]} ${full ? "w-full" : ""}`}
    >
      {icon ? <span className="text-base">{icon}</span> : null}
      <span className="truncate">{label}</span>
    </button>
  );
};

const TicketCard = ({ ticket, onTicketUpdate }: any) => {
  const [isModalOpen, setModalOpen] = useState<boolean>(false);
  const [isModalOpenForCategory, setModalOpenForCategory] = useState<boolean>(false);
  const [isModalOpenForPriority, setModalOpenForPriority] = useState<boolean>(false);
  const [isModalOpenToMe, setModalOpenToMe] = useState<boolean>(false);
  const [selectedTicket, setSelectedTicket] = useState<any>(null);
  const [selectedTicketToMe, setSelectedTicketToMe] = useState<any>(null);
  const [isSolutionExpanded, setIsSolutionExpanded] = useState<boolean>(false);
  const [solutionSteps, setSolutionSteps] = useState<any>(undefined);
  const [isFetchingSteps, setIsFetchingSteps] = useState<boolean>(false);
  const [hasFetchedSteps, setHasFetchedSteps] = useState<boolean>(false);
  const [isSolveModalOpen, setIsSolveModalOpen] = useState<boolean>(false);
  const [solveStepsText, setSolveStepsText] = useState<string>("");
  const [isSolving, setIsSolving] = useState<boolean>(false);
  const [ticketState, setTicketState] = useState<any>(ticket);

  const location = useLocation();
  const userRole = sessionStorage.getItem("role");
  const isSupportTeamMember = userRole === "support_team_member";
  const isSupportTeamManager = userRole === "support_team_manager";
  const canShowSolutionSteps = canViewSolutionSteps(userRole);
  const ticketData = ticketState || ticket;

  const cleanStepText = (text: string) =>
    text.replace(/\s*\[source_type:.*?\]\s*[.,;:]?\s*$/g, "");
  const extractRawSteps = (ticketData: any) => {
    if (!ticketData || !Object.prototype.hasOwnProperty.call(ticketData, "solution_steps")) {
      return undefined;
    }
    const rawSteps = ticketData.solution_steps;
    if (rawSteps && typeof rawSteps === "object" && !Array.isArray(rawSteps)) {
      if ("steps" in rawSteps) {
        return (rawSteps as any).steps ?? null;
      }
      return null;
    }
    return rawSteps;
  };
  const extractHumanSteps = (ticketData: any) => {
    if (!ticketData || !Object.prototype.hasOwnProperty.call(ticketData, "human_solution_steps")) {
      return undefined;
    }
    const rawSteps = ticketData.human_solution_steps;
    if (rawSteps && typeof rawSteps === "object" && !Array.isArray(rawSteps)) {
      if ("steps" in rawSteps) {
        return (rawSteps as any).steps ?? null;
      }
      return null;
    }
    return rawSteps;
  };

  const normalizeSteps = (rawSteps: any) => {
    if (!Array.isArray(rawSteps)) return [];
    const mapped = rawSteps
      .map((step, index) => {
        if (typeof step === "string") {
          return { order: index + 1, text: step };
        }
        if (step && typeof step === "object") {
          const text = typeof step.text === "string" ? step.text : "";
          const order = typeof step.order === "number" ? step.order : index + 1;
          return { order, text };
        }
        return { order: index + 1, text: "" };
      })
      .filter((item) => item.text.trim().length > 0);

    return mapped.sort((a, b) => a.order - b.order);
  };

  useEffect(() => {
    setTicketState(ticket);
  }, [ticket]);

  useEffect(() => {
    setSolutionSteps(extractRawSteps(ticket));
    setIsSolutionExpanded(false);
    setIsFetchingSteps(false);
    setHasFetchedSteps(false);
  }, [ticket?.id]);

  const teamData = isSupportTeamManager ? AllTeams(sessionStorage.getItem("company_id")) : null;

  const assignTOTeamMutation = AssginToTicket(ticketData?.id);
  const assignToMe = isSupportTeamMember
    ? AssginToMe(selectedTicketToMe?.id, { user_id: sessionStorage.getItem("id") })
    : null;

  const editMutation: any = isSupportTeamManager ? EditTicket(ticketData?.id) : null;

  const normalizedSteps = normalizeSteps(solutionSteps);
  const humanSolutionSteps = extractHumanSteps(ticketData);
  const normalizedHumanSteps = normalizeSteps(humanSolutionSteps);
  const hasNoSolutionSteps =
    (solutionSteps === null || (Array.isArray(solutionSteps) && solutionSteps.length === 0)) &&
    (humanSolutionSteps === null || (Array.isArray(humanSolutionSteps) && humanSolutionSteps.length === 0));

  const handleToggleSolutionSteps = async () => {
    if (!canShowSolutionSteps) return;
    if (isSolutionExpanded) {
      setIsSolutionExpanded(false);
      return;
    }

    if (solutionSteps === undefined && ticketData?.id && !hasFetchedSteps && !isFetchingSteps) {
      setIsFetchingSteps(true);
      try {
        const response = await APIInstance.TicketDetails(ticketData.id);
        const ticketData = response?.data?.data ?? response?.data ?? response;
        setSolutionSteps(extractRawSteps(ticketData) ?? null);
        setHasFetchedSteps(true);
      } catch (error) {
        console.error("Error fetching ticket details:", error);
      } finally {
        setIsFetchingSteps(false);
      }
    }

    setIsSolutionExpanded(true);
  };

  const buildStepsFromText = (text: string) =>
    text
      .split("\n")
      .map((line) => line.trim())
      .filter((line) => line.length > 0);

  const stepsToMultilineText = (steps: any) => {
    const normalized = normalizeSteps(steps);
    return normalized.map((step) => step.text).join("\n");
  };

  const handleOpenSolveModal = () => {
    setSolveStepsText(stepsToMultilineText(humanSolutionSteps));
    setIsSolveModalOpen(true);
  };

  const handleSolveSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!ticketData?.id) return;

    const steps = buildStepsFromText(solveStepsText);
    if (steps.length === 0) {
      toast.error("Please enter at least one solution step.");
      return;
    }

    setIsSolving(true);
    try {
      const response = await APIInstance.SolveTicket(ticketData.id, { steps });
      const payload = response?.data?.data ?? response?.data ?? response;
      const updatedStatus = payload?.status ?? ticketData.status;
      const updatedHumanSteps = payload?.human_solution_steps ?? steps;
      const updatedTicket = {
        ...ticketData,
        status: updatedStatus,
        human_solution_steps: updatedHumanSteps,
      };

      setTicketState(updatedTicket);
      onTicketUpdate?.(updatedTicket);
      setIsSolveModalOpen(false);
      toast.success(payload?.message || "Ticket solved successfully!");
      setTimeout(() => reloadAfterChange(), 400);
    } catch (error: any) {
      toast.error(
        error?.response?.data?.message || error?.message || "Failed to solve the ticket."
      );
    } finally {
      setIsSolving(false);
    }
  };

  const formik = useFormik({
    initialValues: { team_id: "" },
    onSubmit: (values: any) => {
      assignTOTeamMutation.mutate(values);
      formik.resetForm();
      setModalOpen(false);
    },
  });

  return (
    <>
      {/* Card */}
      <div className="bg-white rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition p-4 relative overflow-hidden">
        {/* left accent */}
        <div className="absolute left-0 top-0 h-full w-1.5 bg-blue-600" />

        <div className="pl-2">
          {/* Header */}
          <div className="flex justify-between items-start gap-3">
            <div className="min-w-0">
              <h3 className="font-semibold text-gray-900 text-sm truncate">{ticketData.title}</h3>
              <p className="text-xs text-gray-500 mt-1">status: {ticketData.status}</p>
            </div>
            <Index data={ticketData} />
          </div>

          <div className="h-[1px] bg-gray-200 my-3" />

          {/* Info */}
          <div className="space-y-1">
            <p className="text-sm text-gray-600">team: {ticketData.team_name}</p>
            <p className="text-sm text-gray-600">priority: {ticketData.priority}</p>
            <p className="text-sm text-gray-600">category: {ticketData.category}</p>
          </div>

          <div className="h-[1px] bg-gray-200 my-3" />

          {/* Actions */}
          <div className="mt-3 grid grid-cols-1 text-center gap-2">
            {/* Client actions */}
            {userRole === "client" && (
              <>
                <div className=" flex  justify-center">
                  <Edit data={ticketData} />
                  <Delete
                    id={ticketData?.id}
                    query_name={Delete_request}
                    label_of_button="Delete Ticket"
                    title="Delete this Ticket"
                  />
                </div>

              </>
            )}

            {/* Assign actions */}
            {location.pathname === "/ticket" && isSupportTeamManager && (
          
              <ActionBtn
                label="Assign User"
                variant="ghost"
                icon={<IconUserPlus />}
                onClick={() => {
                  setSelectedTicket(ticketData);
                  setModalOpen(true);
                }}
                title="Assign ticket to a user"
              />
            ) }
            {location.pathname === "/ticket" && userRole === "support_team_member" && (
          
             <ActionBtn
                label="Assign to Me"
                variant="ghost"
                icon={<IconUserPlus />}
                onClick={() => {
                  setSelectedTicketToMe(ticketData);
                  setModalOpenToMe(true);
                }}
                title="Assign ticket to me"
              />
            ) }
 
            {/* Details component stays as-is */}
            <div className="col-span-1 flex justify-center text-center">
              <Details data={ticketData} />
            </div>

            {canShowSolutionSteps && (
              <div className="col-span-1 w-full text-left">
                <ActionBtn
                  label={isSolutionExpanded ? "Hide solution steps" : "Show solution steps"}
                  variant="secondary"
                  onClick={handleToggleSolutionSteps}
                  disabled={(!isSolutionExpanded && hasNoSolutionSteps) || isFetchingSteps}
                  title="Toggle solution steps"
                />
                {hasNoSolutionSteps && (
                  <p className="mt-1 text-xs text-gray-500">No solution available yet.</p>
                )}
                {isSolutionExpanded && (normalizedHumanSteps.length > 0 || normalizedSteps.length > 0) && (
                  <div className="mt-2 rounded-lg border border-gray-200 bg-gray-50 p-3">
                    {normalizedHumanSteps.length > 0 && (
                      <div>
                        <p className="text-xs font-semibold uppercase tracking-wide text-gray-500">
                          Human solution
                        </p>
                        <ol className="list-decimal pl-5 space-y-2 text-sm text-gray-700 leading-relaxed break-words mt-2">
                          {normalizedHumanSteps.map((step, index) => (
                            <li key={`${ticketData?.id ?? "ticket"}-human-solution-${index}`}>
                              {cleanStepText(step.text)}
                            </li>
                          ))}
                        </ol>
                      </div>
                    )}
                    {normalizedSteps.length > 0 && (
                      <div className={normalizedHumanSteps.length > 0 ? "mt-3" : ""}>
                        <p className="text-xs font-semibold uppercase tracking-wide text-gray-500">
                          Solution steps
                        </p>
                        <ol className="list-decimal pl-5 space-y-2 text-sm text-gray-700 leading-relaxed break-words mt-2">
                          {normalizedSteps.map((step, index) => (
                            <li key={`${ticketData?.id ?? "ticket"}-solution-${index}`}>
                              {cleanStepText(step.text)}
                            </li>
                          ))}
                        </ol>
                      </div>
                    )}
                  </div>
                )}
                <div className="mt-2">
                  <ActionBtn
                    label="Solve"
                    variant="primary"
                    onClick={handleOpenSolveModal}
                    title="Solve ticket"
                  />
                </div>
              </div>
            )}

            {/* Manager actions */}
            {isSupportTeamManager && (
              <>
                <ActionBtn
                  label="Edit Priority"
                  variant="danger"
                  onClick={() => setModalOpenForPriority(true)}
                  title="Change ticket priority"
                />
                <ActionBtn
                  label="Edit Category"
                  variant="secondary"
                  onClick={() => setModalOpenForCategory(true)}
                  title="Change ticket category"
                />
              </>
            )}
          </div>
        </div>
      </div>

      {/* Assign to Team Modal */}
      {isSupportTeamManager && isModalOpen && selectedTicket && (
        <StatusModal modal={isModalOpen} setModal={setModalOpen}>
          <form onSubmit={formik.handleSubmit}>
            <SelectInput
              name="team_id"
              options={teamData?.data?.data || []}
              displayFields={["category"]}
              formik={formik}
              label="Assign To Team"
            />
            <div className="flex justify-end mt-4">
              <Loading mutation={assignTOTeamMutation.isLoading} title="Assign" />
            </div>
          </form>
        </StatusModal>
      )}

      {canShowSolutionSteps && isSolveModalOpen && (
        <StatusModal
          title="Solve ticket"
          sectitle="Add solution steps to solve this ticket"
          modal={isSolveModalOpen}
          setModal={setIsSolveModalOpen}
        >
          <form onSubmit={handleSolveSubmit} className="mt-4">
            <label htmlFor={`solve-steps-${ticketData?.id}`} className="block text-sm font-semibold text-gray-700">
              Steps (one per line)
            </label>
            <textarea
              id={`solve-steps-${ticketData?.id}`}
              rows={5}
              className="mt-2 w-full rounded-md border border-gray-300 p-2 text-sm shadow-sm focus:border-blue-500 focus:ring-blue-500"
              placeholder="Step 1&#10;Step 2&#10;Step 3"
              value={solveStepsText}
              onChange={(event) => setSolveStepsText(event.target.value)}
              disabled={isSolving}
            />
            <div className="flex justify-end mt-4">
              <Loading mutation={isSolving} title="Submit solution" />
            </div>
          </form>
        </StatusModal>
      )}

      {/* Assign to Me Modal */}
      {isSupportTeamMember && isModalOpenToMe && selectedTicketToMe && (
        <StatusModal modal={isModalOpenToMe} setModal={setModalOpenToMe}>
          <form
            onSubmit={(e) => {
              e.preventDefault();
              if (assignToMe) {
                assignToMe.mutate(undefined, {
                  onSuccess: () => {
                    setModalOpenToMe(false);
                    setTimeout(() => reloadAfterChange(), 400);
                  },
                });
              }
            }}
          >
            <p className="text-gray-700 mb-4">
              Are you sure you want to assign this ticket to yourself?
            </p>
            <div className="flex justify-end mt-4">
              <Loading mutation={assignToMe?.isLoading} title="Assign to Me" />
            </div>
          </form>
        </StatusModal>
      )}

      {/* Priority Modal */}
      {isSupportTeamManager && isModalOpenForPriority && (
        <StatusModal
          title="Priority change"
          sectitle="Do you want to change the Priority"
          modal={isModalOpenForPriority}
          setModal={setModalOpenForPriority}
        >
          <form
            onSubmit={(e) => {
              e.preventDefault();
              const value = (e.target as any).priority.value;
              editMutation?.mutate(
                { priority: value },
                {
                  onSuccess: () => {
                    setModalOpenForPriority(false);
                    toast.success("Priority updated successfully!");
                    setTimeout(() => reloadAfterChange(), 400);
                  },
                  onError: () => toast.error("Failed to update priority"),
                }
              );
            }}
          >
            <SelectInput
              displayFields={["label"]}
              formik={formik}
              name="priority"
              options={[
                { value: "high", label: "High" },
                { value: "medium", label: "Medium" },
                { value: "low", label: "Low" },
              ]}
              label="Change Priority"
            />
            <div className="flex justify-end mt-4">
              <Loading mutation={assignToMe?.isLoading} title="Update priority" />
            </div>
          </form>
        </StatusModal>
      )}

      {/* Category Modal */}
      {isSupportTeamManager && isModalOpenForCategory && (
        <StatusModal
          title="Category change"
          sectitle="Do you want to change the category"
          modal={isModalOpenForCategory}
          setModal={setModalOpenForCategory}
        >
          <form
            onSubmit={(e) => {
              e.preventDefault();
              const value = (e.target as any).category.value;
              editMutation?.mutate(
                { category: value },
                {
                  onSuccess: () => {
                    setModalOpenForCategory(false);
                    toast.success("Category updated successfully!");
                    setTimeout(() => reloadAfterChange(), 400);
                  },
                  onError: () => toast.error("Failed to update priority"),
                }
              );
            }}
          >
            <SelectInput
              displayFields={["label"]}
              formik={formik}
              name="category"
              options={[
                { value: "request", label: "Request" },
                { value: "complaint", label: "Complaint" },
                { value: "feedback", label: "Feedback" },
              ]}
              label="Change Category"
            />
            <div className="flex justify-end mt-4">
              <Loading mutation={assignToMe?.isLoading} title="Update Category" />
            </div>
          </form>
        </StatusModal>
      )}
    </>
  );
};

export default TicketCard;
