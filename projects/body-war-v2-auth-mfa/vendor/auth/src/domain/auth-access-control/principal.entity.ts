export type PrincipalStatus = "ACTIVE" | "DISABLED";
export type SubjectType = "user" | "service" | "automation";

export type Principal = {
  id: string;
  subjectType: SubjectType;
  status: PrincipalStatus;
  roleKeys: string[];
  directPermissions: string[];
};

export type PrincipalCredential = {
  principal: Principal;
  credentialHash: string;
};

export type CreatePrincipalInput = {
  id?: string;
  identifier: string;
  subjectType: SubjectType;
  roleKeys: string[];
  directPermissions: string[];
  credentialHash: string;
};
