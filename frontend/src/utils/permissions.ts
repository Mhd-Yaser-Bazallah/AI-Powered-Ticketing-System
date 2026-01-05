const SOLUTION_STEP_ROLES = new Set(["support_team_manager", "support_team_member"]);

export const canViewSolutionSteps = (role?: string | null) =>
  typeof role === "string" && SOLUTION_STEP_ROLES.has(role);
